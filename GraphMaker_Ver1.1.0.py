import tkinter as tk #
import tkinter.ttk as ttk #
from tkinter import filedialog, messagebox #
from tkinter import * #
from tkinterdnd2 import * # pip install
from pandastable import Table #
import pandas as pd #
from os.path import expanduser #
from pathlib import Path #
import matplotlib.pyplot as plt #
import unicodedata # 
import re
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

##### tab1 ####
btn_fileref_click_flag = False
sep_value = " "
header_value = None
x_axes_selected_flag = False
y_axes_selected_flag = False

##### tab2 ####
save_flag1 = False
save_flag2 = False # Can save graph if both flag is True.
ylim_lst = [None, None]
save_dir = None
#------------------------------------------------------------------------------
def _destroyWindow():
    root.quit()
    root.destroy()

##########################################################################################
#                                        tab 1
##########################################################################################
def update_tabel(num):
    global readfile, sep_value, header_value, df
    if num == 0: #空白区切り
        df = pd.read_csv(readfile, delim_whitespace=True, header=header_value)
    elif num == 1: #カンマ
        df = pd.read_csv(readfile, header=header_value)
    elif num == 2: #tab
        df = pd.read_table(readfile, header=header_value)
    else: #other
        df = pd.read_csv(readfile, sep=sep_value, header=header_value)
    pt = Table(frame_table, showstatusbar=True, dataframe=df)
    pt.show()


def turn_normal():
    btn_fileref_pass["state"] = "normal"
    radio_sep0["state"] = "normal"
    radio_sep1["state"] = "normal"
    radio_sep2["state"] = "normal"
    radio_sep3["state"] = "normal"
    radio_header0["state"] = "normal"
    radio_header1["state"] = "normal"
    label_axes_select["state"] = "normal"
    entry_x_axes_select["state"] = "normal"
    btn_entry_x_axes_select["state"] = "normal"
    label_x_axes_select["state"] = "normal"
    entry_y_axes_select["state"] = "normal"
    btn_entry_y_axes_select["state"] = "normal"
    label_y_axes_select["state"] = "normal"


def btn_fileref_click():
    global idir, readfile, btn_fileref_click_flag
    if btn_fileref_click_flag == False:
        idir = expanduser("~")
    file_path = filedialog.askopenfilename(initialdir = idir)
    if file_path == "":
        pass
    else:
        readfile = file_path
        idir = Path(readfile).parent
        turn_normal()
        btn_fileref_click_flag = True
        update_tabel(0)


def is_japanese(string):
    for ch in string:
        name = unicodedata.name(ch) 
        if "CJK UNIFIED" in name \
        or "HIRAGANA" in name \
        or "KATAKANA" in name:
            return True
    return False


def file_drop(event):
    global idir, readfile, btn_fileref_click_flag
    readfile = event.data
    if is_japanese(readfile):
        readfile = readfile.replace("{", "")
        readfile = readfile.replace("}", "")
        readfile = readfile.replace("\\", "/")
    idir = Path(readfile).parent
    turn_normal()
    btn_fileref_click_flag = True
    update_tabel(0)


def btn_fileref_pass_click():
    global readfile
    messagebox.showinfo("ファイルパス", readfile)


def radio_sep():
    var = var_sep.get()
    if var == 3:
        entry_sep["state"] = "normal"
        btn_entry_sep["state"] = "normal"
    else:
        update_tabel(var)
        entry_sep.delete(0, tk.END)
        entry_sep["state"] = "disabled"
        btn_entry_sep["state"] = "disabled"    
         
    
def btn_entry_sep_click():
    global sep_value
    try:
        sep_value = var_entry_sep.get()
        update_tabel(3)
    except:
        messagebox.showerror("不正な入力", "不正な入力です")


def btn_entry_header_click():
    global header_value
    try:
        header_value = int(var_entry_header.get()) - 1
        update_tabel(var_sep.get())
    except pd.errors.ParserError:
        messagebox.showerror("不正な入力", "入力値が行数を超えています")
    except:
        messagebox.showerror("不正な入力", "1以上の整数を入力してください")


def radio_header():
    global header_value
    var = var_header.get()
    if var == 0:
        header_value = None
        update_tabel(var_sep.get())
        entry_header["state"] = "disabled"
        label_entry_header["state"] = "disabled"
        btn_entry_header["state"] = "disabled"
        var_entry_header.set("1")
    else:
        entry_header["state"] = "normal"
        label_entry_header["state"] = "normal"
        btn_entry_header["state"] = "normal"


#---適用ボタン-グラフ描画-------------------------------------------------
def btn_pre_click(flag):
    global ylim_lst, selected_x_column, selected_y_column, df, save_flag1, readfile, fig
    label_saved["fg"] = root.cget("background")
    try:
        plt.clf()
        plt.close()
    except:
        pass

    if flag == True:
        ylim_lst = [None, None]

    try:
        # title = "hoge"

        fig = plt.figure(figsize=(6.3, 4.7))
        ax = fig.add_subplot(1,1,1)
        ax.scatter(df[selected_x_column], df[selected_y_column])

        # ax.yaxis.set_major_formatter('{x:.1e}')
        ax.set_xlim(0, 0.030)
        ax.set_ylim(ylim_lst)

        # ax.set_xlabel("Eaij")
        # ax.set_ylabel(initial_lst[rdo_2_var.get()]+" [Pa]")
        # ax.set_title("Ea-"+initial_lst[rdo_2_var.get()])

        fig.tight_layout()

        canvas_graph = FigureCanvasTkAgg(fig, tab2)
        canvas_graph.get_tk_widget().place(x=475, y=13)
    except:
        messagebox.showerror("エラー", "unknownERROR")
    else:
        save_flag1 = True
        if save_flag1 and save_flag2:
            btn_save["state"] = "normal"


def check_axes_selected():
    global x_axes_selected_flag, y_axes_selected_flag
    if x_axes_selected_flag and y_axes_selected_flag:
        btn_changepage["state"] = "normal"
        btn_3_max_apply["state"] = "normal"
        btn_3_min_apply["state"] = "normal"
        btn_pre_click(True)
        btn_save_dir["state"] = "normal"
        btn_save["state"] = "normal"


def btn_entry_x_axes_select_click():
    global df, selected_x_column, x_axes_selected_flag
    try:
        selected_x_column_tmp = int(entry_x_axes_select.get())
        if selected_x_column_tmp > len(df.columns) - 1:
            messagebox.showerror("不正な入力", f"0~{int(len(df.columns))}の整数を入力してください")
        else:
            selected_x_column = selected_x_column_tmp
            var_label_x_axes_select.set(f"選択中 : {selected_x_column}")
            label_x_axes_select["fg"] = "black"
            x_axes_selected_flag = True
    except:
        messagebox.showerror("不正な入力", f"0~{int(len(df.columns))}以上の整数を入力してください")
    else:
        check_axes_selected()

def btn_entry_y_axes_select_click():
    global df, selected_y_column, y_axes_selected_flag
    try:
        selected_y_column_tmp = int(entry_y_axes_select.get())
        if selected_y_column_tmp > len(df.columns) - 1:
            messagebox.showerror("不正な入力", f"0~{int(len(df.columns))}の整数を入力してください")
        else:
            selected_y_column = selected_y_column_tmp
            var_label_y_axes_select.set(f"選択中 : {selected_y_column}")
            label_y_axes_select["fg"] = "black"
            y_axes_selected_flag = True
    except:
        messagebox.showerror("不正な入力", f"0~{int(len(df.columns))}以上の整数を入力してください")
    else:
        check_axes_selected()


def btn_changepage_click():
    global selected_x_column, selected_y_column
    notebook.select(1)

##########################################################################################
#                                        tab 2
##########################################################################################
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
            btn_pre_click(False)
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
            btn_pre_click(False)
#------------------------------------------------


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
    global save_dir, fig
    try:
        # save_file_name = save_dir + f"/Eaij-{initial_lst[rdo_2_var.get()]}_{title}.jpg"
        save_file_name = "hoge"
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

# #----上限と下限が同じ値のときエラー出力---------------------------------------------------------------
# def error_min_equal_max(num):
#     global ylim_lst
#     if ylim_lst[0] == ylim_lst[1]:
#         messagebox.showwarning(title="不正な入力", message="上限と下限には異なる値を適用してください.")
#         ylim_lst[num] = None

#-----------------------------------------------





#-------------------------------------------
# root = tk.Tk()
root = TkinterDnD.Tk()
root.title("GraphMaker 1.1.0")
root.protocol('WM_DELETE_WINDOW', _destroyWindow)

notebook = ttk.Notebook(root)

tab1 = tk.Frame(notebook)
tab2 = tk.Frame(notebook)

tab1.drop_target_register(DND_FILES)
tab1.dnd_bind("<<Drop>>", file_drop)

tab1.pack(expand=True, fill=tk.BOTH)
tab2.pack(expand=True, fill=tk.BOTH)
notebook.add(tab1, text="1. データ抽出", padding=3)
notebook.add(tab2, text="2. グラフ作成", padding=3)
notebook.pack(expand=True, fill=tk.BOTH)

##########################################################################################
#                                           tab 1
##########################################################################################
#-------------------------------------------------------------------------------
frame_set = tk.Frame(tab1, bd=5, relief=tk.GROOVE, width=300, height=600)
frame_set.propagate(False)
frame_set.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
#-------------------------------------------------------------------------------
labelframe_fileref = tk.LabelFrame(frame_set, text="ファイル選択",  width=250, height=110)
labelframe_fileref.propagate(False)
labelframe_fileref.pack(side=tk.TOP, pady=10)

label_filedrop1 = tk.Label(labelframe_fileref, text="ここにファイルをドロップ")
label_filedrop1.pack(side=tk.TOP)
label_filedrop2 = tk.Label(labelframe_fileref, text="または")
label_filedrop2.pack(side=tk.TOP, pady=5)

frame_fileref = tk.Frame(labelframe_fileref)
frame_fileref.pack(side=tk.TOP)

btn_fileref = tk.Button(frame_fileref, text='ファイル参照', command=btn_fileref_click)
btn_fileref.pack(side=tk.LEFT, padx=(70,0))

btn_fileref_pass = tk.Button(frame_fileref, text="...", command=btn_fileref_pass_click, state="disabled")
btn_fileref_pass.pack(side=tk.LEFT, padx=(50,0))
#-------------------------------------------------------------------------------
labelframe_sep = tk.LabelFrame(frame_set, text = "区切り", width=250, height=110)
labelframe_sep.propagate(False)
labelframe_sep.pack(side=tk.TOP, padx=10, pady=10)
#-------------------------------------------------------------------------------
frame_sep_top = tk.Frame(labelframe_sep, width=220, height=50)
frame_sep_top.propagate(False)
frame_sep_top.pack(side=tk.TOP, expand=True)

var_sep = tk.IntVar()
var_sep.set(0)
radio_sep0 = tk.Radiobutton(frame_sep_top, value=0, text="空白区切り", variable=var_sep, command=radio_sep, state="disabled")
radio_sep0.pack(side=tk.LEFT)
radio_sep1 = tk.Radiobutton(frame_sep_top, value=1, text="カンマ(,)", variable=var_sep, command=radio_sep, state="disabled")
radio_sep1.pack(side=tk.LEFT)
radio_sep2 = tk.Radiobutton(frame_sep_top, value=2, text="tab(\\t)", variable=var_sep, command=radio_sep, state="disabled")
radio_sep2.pack(side=tk.LEFT)
#---------------------------------------
frame_sep_bottom = tk.Frame(labelframe_sep, width=250, height=50)
frame_sep_bottom.propagate(False)
frame_sep_bottom.pack(side=tk.TOP, expand=True)

radio_sep3 = tk.Radiobutton(frame_sep_bottom, value=3, text="その他", variable=var_sep, command=radio_sep, state="disabled")
radio_sep3.pack(side=tk.LEFT, padx=(13,0))

var_entry_sep = tk.StringVar()
entry_sep = tk.Entry(frame_sep_bottom, textvariable=var_entry_sep, width=5, state="disabled")
entry_sep.pack(side=tk.LEFT)
btn_entry_sep = tk.Button(frame_sep_bottom, text="適用", state="disabled", command=btn_entry_sep_click)
btn_entry_sep.pack(side=tk.LEFT, padx=5)

#-------------------------------------------------------------------------------
labelframe_header = tk.LabelFrame(frame_set, text = "ヘッダー行", width=250, height=60)
labelframe_header.propagate(False)
labelframe_header.pack(side=tk.TOP, padx=10, pady=10)

var_header = tk.IntVar()
var_header.set(0)
radio_header0 = tk.Radiobutton(labelframe_header, value=0, text="なし", variable=var_header, command=radio_header, state="disabled")
radio_header0.pack(side=tk.LEFT, padx=10)
radio_header1 = tk.Radiobutton(labelframe_header, value=1, variable=var_header, command=radio_header, state="disabled")
radio_header1.pack(side=tk.LEFT, padx=(10,0))

var_entry_header = tk.StringVar()
var_entry_header.set("1")
entry_header = tk.Entry(labelframe_header, textvariable=var_entry_header, width=5, state="disabled")
entry_header.pack(side=tk.LEFT)

label_entry_header = tk.Label(labelframe_header, text="行まで", state="disabled")
label_entry_header.pack(side=tk.LEFT)

btn_entry_header = tk.Button(labelframe_header, text="適用", state="disabled", command=btn_entry_header_click)
btn_entry_header.pack(side=tk.LEFT)
#-------------------------------------------------------------------------------
labelframe_axes_select = tk.LabelFrame(frame_set, text="軸選択", width=250, height=180)
labelframe_axes_select.propagate(False)
labelframe_axes_select.pack(side=tk.TOP)

label_axes_select = tk.Label(labelframe_axes_select, text="列番号を選択してください", state="disabled")
label_axes_select.pack(side=tk.TOP)

#------------------------------------------------------------
labelframe_x_axes_select = tk.LabelFrame(labelframe_axes_select, text="X軸", width=230, height=60)
labelframe_x_axes_select.propagate(False)
labelframe_x_axes_select.pack(side=tk.TOP, expand=True, pady=5)

entry_x_axes_select = tk.Entry(labelframe_x_axes_select, state="disabled", width=5)
entry_x_axes_select.pack(side=tk.LEFT, padx=(50,10))

btn_entry_x_axes_select = tk.Button(labelframe_x_axes_select, text="適用", state="disabled", command=btn_entry_x_axes_select_click)
btn_entry_x_axes_select.pack(side=tk.LEFT)

var_label_x_axes_select = tk.StringVar()
var_label_x_axes_select.set("未選択")
label_x_axes_select = tk.Label(labelframe_x_axes_select, fg="red", textvariable=var_label_x_axes_select, state="disabled")
label_x_axes_select.pack(side=tk.LEFT, padx=(10,0))
#------------------------------------------------------------
labelframe_y_axes_select = tk.LabelFrame(labelframe_axes_select, text="Y軸", width=230, height=60)
labelframe_y_axes_select.propagate(False)
labelframe_y_axes_select.pack(side=tk.TOP, expand=True, pady=5)

entry_y_axes_select = tk.Entry(labelframe_y_axes_select, state="disabled", width=5)
entry_y_axes_select.pack(side=tk.LEFT, padx=(50,10))

btn_entry_y_axes_select = tk.Button(labelframe_y_axes_select, text="適用", state="disabled", command=btn_entry_y_axes_select_click)
btn_entry_y_axes_select.pack(side=tk.LEFT)

var_label_y_axes_select = tk.StringVar()
var_label_y_axes_select.set("未選択")
label_y_axes_select = tk.Label(labelframe_y_axes_select, fg="red", textvariable=var_label_y_axes_select, state="disabled")
label_y_axes_select.pack(side=tk.LEFT, padx=(10,0))
#-------------------------------------------------------------------------------
btn_changepage = tk.Button(frame_set, text="グラフ作成!", command=btn_changepage_click, state="disabled", width=25, height=2)
btn_changepage.pack(side=tk.TOP, pady=(15,0))
#-------------------------------------------------------------------------------
frame_table = tk.Frame(tab1)
frame_table.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)

pt = Table(frame_table, showstatusbar=True)
pt.show()


##########################################################################################
#                                        tab 2
##########################################################################################
#---------------------------------------------------------------------------------------------
frame1 = tk.Frame(tab2, bd=2, relief=tk.GROOVE)
frame1.propagate(False)
frame1.place(x=10, y=10, width=450, height=480)


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
frame_graph = tk.Frame(tab2, bd=2, relief=tk.GROOVE, width=640, height=480)
frame_graph.propagate(False)
frame_graph.place(x=470, y=10)

#---ラベル---
label_graph_not_exist = tk.Label(frame_graph, text="ここにグラフが描画されます")
label_graph_not_exist.pack(expand=True)
#-------------------------------------------



root.mainloop()