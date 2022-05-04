import tkinter as tk
from tkinter import BOTH, messagebox, filedialog
import re
import pandas as pd
import matplotlib.pyplot as plt
import os
from os.path import expanduser
from pathlib import Path
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



#----------------------------------------------------------------------------------
btn_1_ref_click_flag = False # True if directory selected.
save_flag1 = False
save_flag2 = False # Can save graph if both flag is True.
initial_lst = ["A1", "A2", "A3", "A4", "A5", "A6"]
ylim_lst = [None, None]
save_dir = None
idir = None


#----------------------------------------------------------------------------------
def _destroyWindow():
    root.quit()
    root.destroy()

#---ファイル参照ボタン---------------------------------------------------------------
def btn_1_ref_click():
    global btn_1_ref_click_flag ,idir, readfile, svf, rho, mu, muw
    if btn_1_ref_click_flag == False:
        idir = expanduser("~")
    filetype = [("600ファイル", "fort.600")]
    file_path = filedialog.askopenfilename(filetypes = filetype, initialdir = idir)
    if file_path == "" and btn_1_ref_click_flag == False:
        label_1_ref["text"] = "ファイルが選択されていません"
    elif file_path == "":
        pass
    else:
        label_1_ref["text"] = "ファイルが選択されました"
        label_1_ref["foreground"] = "black"
        readfile = file_path
        idir = Path(file_path).parent
        btn_1_ref_click_flag = True
        btn_pre["state"] = "normal"
        btn_3_max_apply["state"] = "normal"
        btn_3_min_apply["state"] = "normal"
        btn_save_dir["state"] = "normal"

        #---正規表現---------------------------
        p = r'SVFINAL=(.*?),'
        r = re.findall(p, file_path)
        label_1_svf["text"] = svf = f"SVF={r[0]}"

        p = r'RHO=(.*?),'
        r = re.findall(p, file_path)
        label_1_rho["text"] = rho = f"RHO={r[0]}"

        p = r'MU=(.*?),'
        r = re.findall(p, file_path)
        label_1_mu["text"] = mu = f"MU={r[0]}"

        p = r'MUW=(.*?)/'
        r = re.findall(p, file_path)
        label_1_muw["text"] = muw = f"MUW={r[0]}"


#---選択ファイルのパス表示ボタン-----------------------------------------
# def btn_1_ref_detail_click():
#     try:
#         messagebox.showinfo("ファイルパス", file_path)
#     except:
#         messagebox.showwarning("WARNING", "UNKNOWN ERROR")


#----上限と下限が同じ値のときエラー出力---------------------------------------------------------------
def error_min_equal_max(num):
    global ylim_lst
    if ylim_lst[0] == ylim_lst[1]:
        messagebox.showwarning(title="不正な入力", message="上限と下限には異なる値を適用してください.")
        ylim_lst[num] = None

#-----------------------------------------------
def btn_3_max_apply_1_selected():
    selected_index = listbox_max1.curselection()
    data = listbox_max1.get(selected_index)
    return data

def btn_3_max_apply_2_selected():
    selected_index = listbox_max2.curselection()
    data = listbox_max2.get(selected_index)
    return data

#---上限-適用ボタン------------------------------
def btn_3_max_apply_clilck():
    global ylim_lst
    s = ""
    signlst = ["+", "-"]
    label_saved["fg"] = root.cget("background")
    try:
        s += signlst[rdo_3_max_var.get()]
        s += btn_3_max_apply_1_selected()
        s += "e+"
        s += btn_3_max_apply_2_selected()
    except:
        messagebox.showerror("エラー", "選択していない項目があります")
    else:
        if float(s) == ylim_lst[0]:
            messagebox.showwarning(title="不正な入力", message="上限と下限には異なる値を適用してください.")
        else:
            ylim_lst[1] = float(s)
            btn_pre_click(ylim_lst, False)
#-----------------------------------------------

def btn_3_min_apply_1_selected():
    selected_index = listbox_min1.curselection()
    data = listbox_min1.get(selected_index)
    return data

def btn_3_min_apply_2_selected():
    selected_index = listbox_min2.curselection()
    data = listbox_min2.get(selected_index)
    return data

#---下限-適用ボタン------------------------------
def btn_3_min_apply_clilck():
    global ylim_lst
    s = ""
    signlst = ["+", "-"]
    label_saved["fg"] = root.cget("background")
    try:
        s += signlst[rdo_3_min_var.get()]
        s += btn_3_min_apply_1_selected()
        s += "e+"
        s += btn_3_min_apply_2_selected()
    except:
        messagebox.showerror("エラー", "選択していない項目があります")
    else:
        
        if float(s) == ylim_lst[1]:
            messagebox.showwarning(title="不正な入力", message="上限と下限には異なる値を適用してください.")
        else:
            ylim_lst[0] = float(s)
            btn_pre_click(ylim_lst, False)
#------------------------------------------------


#---適応ボタン-グラフ描画-------------------------------------------------
def btn_pre_click(ylim_value, flag):
    global svf, rho, mu, muw, ylim_lst, initial_lst, title, save_flag1, readfile, fig
    label_saved["fg"] = root.cget("background")
    try:
        plt.clf()
        plt.close()
    except:
        pass

    if flag == True:
        ylim_lst = [None, None]

    try:
        title = f"SVFINAL={svf}_RHO={rho}_MU={mu}_MUW={muw}"

        Alist = ["A11", "A12", "A13", "A1",
                "A21", "A22", "A23", "A2",
                "A31", "A32", "A33", "A3",
                "A41", "A42", "A43", "A4",
                "A51", "A52", "A53", "A5",
                "A61", "A62", "A63", "A6",
                "Eaij"]

        df = pd.read_csv(readfile, delim_whitespace=True, header=None, names=Alist)

        fig = plt.figure(figsize=(6.3, 4.7))
        ax = fig.add_subplot(1,1,1)
        ax.scatter(abs(df["Eaij"]), df[initial_lst[rdo_2_var.get()]])

        ax.yaxis.set_major_formatter('{x:.1e}')
        ax.set_xlim(0, 0.030)
        ax.set_ylim(ylim_value)

        ax.set_xlabel("Eaij")
        ax.set_ylabel(initial_lst[rdo_2_var.get()]+" [Pa]")
        ax.set_title("Ea-"+initial_lst[rdo_2_var.get()])

        fig.tight_layout()

        canvas_graph = FigureCanvasTkAgg(fig, root)
        canvas_graph.get_tk_widget().place(x=475, y=13)
    except NameError:
        messagebox.showerror("エラー", "ファイルを選択してください")
    except IndexError:
        messagebox.showerror("エラー", "A1~A6を選択してください")
    else:
        save_flag1 = True
        if save_flag1 and save_flag2:
            btn_save["state"] = "normal"

#---保存先フォルダ選択ボタン------------------------------------------------------------
def btn_save_dir_click():
    global save_dir, idir, save_flag2
    label_saved["fg"] = root.cget("background")
    dir = filedialog.askdirectory(initialdir = Path(idir).parent)
    if dir != "":
        save_dir = dir
        btn_save_dir["fg"] = "black"
        save_flag2 = True
        if save_flag1 and save_flag2:
            btn_save["state"] = "normal"

#---保存ボタン------------------------------
def btn_save_click():
    global title, initial_lst, save_dir, fig
    try:
        save_file_name = save_dir + f"/Eaij-{initial_lst[rdo_2_var.get()]}_{title}.jpg"
        if os.path.isfile(save_file_name):
            messagebox_ask_save = messagebox.askokcancel(title="確認", message="同名ファイルが存在します.\n上書きしますか?")
            if messagebox_ask_save:
                fig.savefig(save_file_name)
                label_saved["fg"] = "black"
        else:
            fig.savefig(save_file_name)
            label_saved["fg"] = "black"
    except:
        messagebox.showwarning("UNKNOWN ERROR", "btn_save_click")

#---------------------------------------------------------------------------------------------
root = tk.Tk()
root_width=1120
root.geometry(f'{root_width}x500')
root.title('GraphMaker 1.0.0')
root.protocol('WM_DELETE_WINDOW', _destroyWindow) 
root.resizable(width=False, height=False)
#---------------------------------------------------------------------------------------------
frame1 = tk.Frame(root, bd=2, relief=tk.GROOVE)
frame1.propagate(False)
frame1.place(x=10, y=10, width=450, height=480)

#--------------------------------------------------------------------------------------------
labelframe_file_ref = tk.LabelFrame(frame1, text="1. ファイル選択", width=410, height=100, bd=5, relief=tk.GROOVE)
labelframe_file_ref.propagate(False)
labelframe_file_ref.place(x=20, y=10)

#----------1-TOP--------------------------------------------------------------------------------
frame1_fileref_top = tk.Frame(labelframe_file_ref)
frame1_fileref_top.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

btn_1_ref = tk.Button(frame1_fileref_top, text='ファイル参照', command=btn_1_ref_click)
btn_1_ref.pack(side=tk.LEFT, padx=5)

label_1_ref = tk.Label(frame1_fileref_top, text="ファイルが選択されていません", foreground="red")
label_1_ref.pack(side=tk.LEFT, padx=10)

# btn_1_ref_detail = tk.Button(frame1_fileref_top, text="パス表示", command=btn_1_ref_detail_click)
# btn_1_ref_detail.pack(side=tk.RIGHT, padx=(0,15))

#-----------1-BOTTOM--------------------------------------------------------------------------------
frame1_fileref_bottom = tk.Frame(labelframe_file_ref, bd=2, relief=tk.GROOVE)
frame1_fileref_bottom.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

label_1_svf = tk.Label(frame1_fileref_bottom, text="SVF=")
label_1_svf.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
label_1_rho = tk.Label(frame1_fileref_bottom, text="RHO=")
label_1_rho.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
label_1_mu = tk.Label(frame1_fileref_bottom, text="MU=")
label_1_mu.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
label_1_muw = tk.Label(frame1_fileref_bottom, text="MUW=")
label_1_muw.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

#----------2. グラフ選択-----------------------------------------------------------------------------
labelframe_2_list = tk.LabelFrame(frame1, text="2. グラフ選択", width=100, height=250, bd=5, relief=tk.GROOVE)
labelframe_2_list.propagate(False)
labelframe_2_list.place(x=20, y=130)

#-------2-ラジオボタン------------
rdo_2_var = tk.IntVar()
rdo_2_var.set(0)
rdo_2_1 = tk.Radiobutton(labelframe_2_list, value=0, variable=rdo_2_var, text="A1")
rdo_2_1.pack(pady=(10,0))
rdo_2_2 = tk.Radiobutton(labelframe_2_list, value=1, variable=rdo_2_var, text="A2")
rdo_2_2.pack()
rdo_2_3 = tk.Radiobutton(labelframe_2_list, value=2, variable=rdo_2_var, text="A3")
rdo_2_3.pack()
rdo_2_4 = tk.Radiobutton(labelframe_2_list, value=3, variable=rdo_2_var, text="A4")
rdo_2_4.pack()
rdo_2_5 = tk.Radiobutton(labelframe_2_list, value=4, variable=rdo_2_var, text="A5")
rdo_2_5.pack()
rdo_2_6 = tk.Radiobutton(labelframe_2_list, value=5, variable=rdo_2_var, text="A6")
rdo_2_6.pack()

#---------2-適用ボタン-------------
btn_pre = tk.Button(labelframe_2_list, text='適用', command=lambda:btn_pre_click(ylim_lst, True), state="disabled")
btn_pre.pack(expand=True)
y_max_flag = False


#----------3. y軸調整-----------------------------------------------------------------------
labelframe_3_axes_title = tk.LabelFrame(frame1, text="3. Y軸調整", width=300, height=250, bd=5, relief=tk.GROOVE)
labelframe_3_axes_title.propagate(False)
labelframe_3_axes_title.place(x=130, y=130)

#-----------3-上限---------------------------------------------------------------------------
labelframe_3_axes_ymax = tk.LabelFrame(labelframe_3_axes_title, text="上限")
labelframe_3_axes_ymax.propagate(False)
labelframe_3_axes_ymax.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=10)

#-----------3-上限-frame1---------------------------------------
frame_3_max_1 = tk.Frame(labelframe_3_axes_ymax)
frame_3_max_1.pack(side=tk.LEFT)
#-----------3-上限-frame1-ラジオボタン---------------
rdo_3_max_var = tk.IntVar()
rdo_3_max_var.set(0)
rdo_3_1 = tk.Radiobutton(frame_3_max_1, value=0, variable=rdo_3_max_var, text="+", font=("normal","15"))
rdo_3_1.pack(side=tk.TOP)
rdo_3_2 = tk.Radiobutton(frame_3_max_1, value=1, variable=rdo_3_max_var, text="-", font=("normal","15"))
rdo_3_2.pack(side=tk.TOP)

#-----------3-上限-frame2---------------------------------------
frame_3_max_2 = tk.Frame(labelframe_3_axes_ymax)
frame_3_max_2.pack(side=tk.LEFT)
#-----------3-上限-frame2-リストボックススクロール------
listbox_max1_nums = (str(0.5*x) for x in range(0,20))
listbox_max1_nums = list(listbox_max1_nums)
listbox_max1_lists = tk.StringVar(value=listbox_max1_nums)
listbox_max1 = tk.Listbox(frame_3_max_2, listvariable=listbox_max1_lists, height=4, width=5, exportselection=False)
scrollbar_max1 = tk.Scrollbar(frame_3_max_2, orient=tk.VERTICAL, command=listbox_max1.yview)
listbox_max1["yscrollcommand"] = scrollbar_max1.set
listbox_max1.grid(row=0, column=0, padx=(10,0))
scrollbar_max1.grid(row=0, column=1, sticky=(tk.N, tk.S))

#-----------3-上限-frame3-----------------------------------------------------------------
frame_3_max_3 = tk.Frame(labelframe_3_axes_ymax)
frame_3_max_3.pack(side=tk.LEFT)
#-----------3-上限-frame3-ラベル------------------------------------------
label_3_max = tk.Label(frame_3_max_3, text="E+", font=("normal","12","bold"))
label_3_max.pack()

#-----------3-上限-frame4-----------------------------------------------------------------
frame_3_max_4 = tk.Frame(labelframe_3_axes_ymax)
frame_3_max_4.pack(side=tk.LEFT)
#-----------3-上限-frame4-リストボックススクロール------
listbox_max2_nums = (str(x).zfill(2) for x in range(0,21))
listbox_max2_nums = list(listbox_max2_nums)
listbox_max2_lists = tk.StringVar(value=listbox_max2_nums)
listbox_max2 = tk.Listbox(frame_3_max_4, listvariable=listbox_max2_lists, height=4, width=5, exportselection=False)
scrollbar_max2 = tk.Scrollbar(frame_3_max_4, orient=tk.VERTICAL, command=listbox_max2.yview)
listbox_max2["yscrollcommand"] = scrollbar_max2.set
listbox_max2.grid(row=0, column=0, padx=(10,0))
scrollbar_max2.grid(row=0, column=1, sticky=(tk.N, tk.S))

#-----------3-上限-frame5-----------------------------------------------------------------
frame_3_max_5 = tk.Frame(labelframe_3_axes_ymax)
frame_3_max_5.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
#-----------3-上限-frame5-適用ボタン---------------------------
btn_3_max_apply = tk.Button(frame_3_max_5, text="適用", command=btn_3_max_apply_clilck, state="disabled")
btn_3_max_apply.pack(expand=True)



#-----------3-下限------------------------------------------------------------------
labelframe_3_axes_ymin = tk.LabelFrame(labelframe_3_axes_title, text="下限")
labelframe_3_axes_ymin.propagate(False)
labelframe_3_axes_ymin.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=10, pady=10)

#-----------3-下限-frame1---------------------------------------
frame_3_min_1 = tk.Frame(labelframe_3_axes_ymin)
frame_3_min_1.pack(side=tk.LEFT)
#-----------3-下限-frame1-ラジオボタン---------------
rdo_3_min_var = tk.IntVar()
rdo_3_min_var.set(0)
rdo_3_1 = tk.Radiobutton(frame_3_min_1, value=0, variable=rdo_3_min_var, text="+", font=("normal","15"))
rdo_3_1.pack(side=tk.TOP)
rdo_3_2 = tk.Radiobutton(frame_3_min_1, value=1, variable=rdo_3_min_var, text="-", font=("normal","15"))
rdo_3_2.pack(side=tk.TOP)

#-----------3-下限-frame2---------------------------------------
frame_3_min_2 = tk.Frame(labelframe_3_axes_ymin)
frame_3_min_2.pack(side=tk.LEFT)
#-----------3-下限-frame2-リストボックススクロール------
listbox_min1_nums = (str(0.5*x) for x in range(0,20))
listbox_min1_nums = list(listbox_min1_nums)
listbox_min1_lists = tk.StringVar(value=listbox_min1_nums)
listbox_min1 = tk.Listbox(frame_3_min_2, listvariable=listbox_min1_lists, height=4, width=5, exportselection=False)
scrollbar_min1 = tk.Scrollbar(frame_3_min_2, orient=tk.VERTICAL, command=listbox_min1.yview)
listbox_min1["yscrollcommand"] = scrollbar_min1.set
listbox_min1.grid(row=0, column=0, padx=(10,0))
scrollbar_min1.grid(row=0, column=1, sticky=(tk.N, tk.S))

#-----------3-下限-frame3-----------------------------------------------------------------
frame_3_min_3 = tk.Frame(labelframe_3_axes_ymin)
frame_3_min_3.pack(side=tk.LEFT)
#-----------3-下限-frame3-ラベル------------------------------------------
label_3_min = tk.Label(frame_3_min_3, text="E+", font=("normal","12","bold"))
label_3_min.pack()

#-----------3-下限-frame4-----------------------------------------------------------------
frame_3_min_4 = tk.Frame(labelframe_3_axes_ymin)
frame_3_min_4.pack(side=tk.LEFT)
#-----------3-下限-frame4-リストボックススクロール------
listbox_min2_nums = (str(x).zfill(2) for x in range(0,21))
listbox_min2_nums = list(listbox_min2_nums)
listbox_min2_lists = tk.StringVar(value=listbox_min2_nums)
listbox_min2 = tk.Listbox(frame_3_min_4, listvariable=listbox_min2_lists, height=4, width=5, exportselection=False)
scrollbar_min2 = tk.Scrollbar(frame_3_min_4, orient=tk.VERTICAL, command=listbox_min2.yview)
listbox_min2["yscrollcommand"] = scrollbar_min2.set
listbox_min2.grid(row=0, column=0, padx=(10,0))
scrollbar_min2.grid(row=0, column=1, sticky=(tk.N, tk.S))

#-----------3-下限-frame5-----------------------------------------------------------------
frame_3_min_5 = tk.Frame(labelframe_3_axes_ymin)
frame_3_min_5.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
#-----------3-下限-frame5-ボタン---------------------------
btn_3_min_apply = tk.Button(frame_3_min_5, text="適用", command=btn_3_min_apply_clilck, state="disabled")
btn_3_min_apply.pack(expand=True)

#-----------保存先ボタン---------------------------------------------
btn_save_dir = tk.Button(frame1, text='保存先フォルダ選択', fg="red", command=btn_save_dir_click, state="disabled")
btn_save_dir.place(x=100, y=410)

#-----------保存ボタン---------------------------------------------
btn_save = tk.Button(frame1, text='保存', state="disabled", command=btn_save_click)
btn_save.place(x=250, y=410)

#-----------保存しましたボタン-------------------------------------
label_saved = tk.Label(frame1, text="保存しました!", fg=root.cget("background")) #初期はwindow背景色
label_saved.pack_forget()
label_saved.place(x=300, y=413)


#-----------グラフ出力--frame-----------------------------------------------------------
frame_graph = tk.Frame(root, bd=2, relief=tk.GROOVE, width=640, height=480)
frame_graph.propagate(False)
frame_graph.place(x=470, y=10)

#---ラベル---
label_graph_not_exist = tk.Label(frame_graph, text="ここにグラフが描画されます")
label_graph_not_exist.pack(expand=True)

#------------------------------------------------------
root.mainloop()