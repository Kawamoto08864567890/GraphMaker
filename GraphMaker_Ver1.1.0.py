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
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

##### Tab1 ####
btn_fileref_click_flag = False
sep_value = " "
header_value = None
x_axes_selected_flag = False
y_axes_selected_flag = False

##### Tab2 ####
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
    pt = Table(Frame2_T1, showstatusbar=True, dataframe=df)
    pt.show()


def turn_normal():
    Btn2_T1F1Lf1F1["state"] = "normal"
    Radio0_T1F1Lf2F1["state"] = "normal"
    Radio1_T1F1Lf2F1["state"] = "normal"
    Radio2_T1F1Lf2F1["state"] = "normal"
    Radio3_TF1Lf2F2["state"] = "normal"
    Radio0_T1F1Lf3["state"] = "normal"
    Radio1_T1F1Lf3["state"] = "normal"
    Label_T1F1Lf4["state"] = "normal"
    Entry_T1F1Lf4Lf1["state"] = "normal"
    Btn_T1F1Lf4Lf1["state"] = "normal"
    Label_T1F1Lf4Lf1["state"] = "normal"
    Entry_T1F1Lf4Lf2["state"] = "normal"
    Btn_T1F1Lf4Lf2["state"] = "normal"
    Label_T1F1Lf4Lf2["state"] = "normal"


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
    var = Var_radio_T1F1Lf2.get()
    if var == 3:
        Entry_T1F1Lf2F2["state"] = "normal"
        Btn_T1F1Lf2F2["state"] = "normal"
    else:
        update_tabel(var)
        Entry_T1F1Lf2F2.delete(0, tk.END)
        Entry_T1F1Lf2F2["state"] = "disabled"
        Btn_T1F1Lf2F2["state"] = "disabled"    
         
    
def btn_entry_sep_click():
    global sep_value
    try:
        sep_value = var_entry_T1F1Lf2.get()
        update_tabel(3)
    except:
        messagebox.showerror("不正な入力", "不正な入力です")


def btn_Entry_T1F1Lf3_click():
    global header_value
    try:
        header_value = int(var_entry_T1F1Lf3.get()) - 1
        update_tabel(Var_radio_T1F1Lf2.get())
    except pd.errors.ParserError:
        messagebox.showerror("不正な入力", "入力値が行数を超えています")
    except:
        messagebox.showerror("不正な入力", "1以上の整数を入力してください")


def radio_header():
    global header_value
    var = var_radio_T1F1Lf3.get()
    if var == 0:
        header_value = None
        update_tabel(Var_radio_T1F1Lf2.get())
        Entry_T1F1Lf3["state"] = "disabled"
        Label_T1F1Lf3["state"] = "disabled"
        Btn_T1F1Lf3["state"] = "disabled"
        var_entry_T1F1Lf3.set("1")
    else:
        Entry_T1F1Lf3["state"] = "normal"
        Label_T1F1Lf3["state"] = "normal"
        Btn_T1F1Lf3["state"] = "normal"


#---適用ボタン-グラフ描画-------------------------------------------------
def btn_pre_click(flag):
    global ylim_lst, selected_x_column, selected_y_column, df, save_flag1, readfile, fig
    Label_saved_T2F1["foreground"] = root.cget("background")
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

        canvas_graph = FigureCanvasTkAgg(fig, Tab2)
        canvas_graph.get_tk_widget().place(x=475, y=13)
    except:
        messagebox.showerror("エラー", "unknownERROR")
    else:
        save_flag1 = True
        if save_flag1 and save_flag2:
            Btn_save_T2F1["state"] = "normal"


def check_axes_selected():
    global x_axes_selected_flag, y_axes_selected_flag
    if x_axes_selected_flag and y_axes_selected_flag:
        Btn_T1F1["state"] = "normal"
        Btn_T2F1Lf1Lf1C4["state"] = "normal"
        Btn_T2F1Lf1Lf2C5["state"] = "normal"
        btn_pre_click(True)
        Btn_savedir_T2F1["state"] = "normal"
        Btn_save_T2F1["state"] = "normal"


def btn_entry_x_axes_select_click():
    global df, selected_x_column, x_axes_selected_flag
    try:
        selected_x_column_tmp = int(Entry_T1F1Lf4Lf1.get())
        if selected_x_column_tmp > len(df.columns) - 1:
            messagebox.showerror("ERROR01", f"0~{int(len(df.columns))}の整数を入力してください")
        else:
            selected_x_column = selected_x_column_tmp
            var_str_T1F1Lf4Lf1.set(f"選択中 : {selected_x_column}")
            Label_T1F1Lf4Lf1["foreground"] = "black"
            x_axes_selected_flag = True
    except:
        messagebox.showerror("ERROR02", f"0~{int(len(df.columns))}以上の整数を入力してください")
    else:
        check_axes_selected()

def btn_entry_y_axes_select_click():
    global df, selected_y_column, y_axes_selected_flag
    try:
        selected_y_column_tmp = int(Entry_T1F1Lf4Lf2.get())
        if selected_y_column_tmp > len(df.columns) - 1:
            messagebox.showerror("不正な入力", f"0~{int(len(df.columns))}の整数を入力してください")
        else:
            selected_y_column = selected_y_column_tmp
            var_str_T1F1Lf4Lf2.set(f"選択中 : {selected_y_column}")
            Label_T1F1Lf4Lf2["foreground"] = "black"
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
    selected_index = Listbox_T2F1Lf1Lf1C2.curselection()
    data = Listbox_T2F1Lf1Lf1C2.get(selected_index)
    return data

def btn_3_max_apply_2_selected():
    selected_index = Listbox_T2F1Lf1Lf1C4.curselection()
    data = Listbox_T2F1Lf1Lf1C4.get(selected_index)
    return data

#---上限-適用ボタン------------------------------
def btn_3_max_apply_clilck():
    global ylim_lst
    s = ""
    signlst = ["+", "-"]
    Label_saved_T2F1["foreground"] = root.cget("background")
    try:
        s += signlst[var_radio_T2F1Lf1Lf1C1.get()]
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
    selected_index = Listbox_T2F1Lf1Lf2C2.curselection()
    data = Listbox_T2F1Lf1Lf2C2.get(selected_index)
    return data

def btn_3_min_apply_2_selected():
    selected_index = Listbox_T2F1Lf1Lf2C4.curselection()
    data = Listbox_T2F1Lf1Lf2C4.get(selected_index)
    return data

#---下限-適用ボタン------------------------------
def btn_3_min_apply_clilck():
    global ylim_lst
    s = ""
    signlst = ["+", "-"]
    Label_saved_T2F1["foreground"] = root.cget("background")
    try:
        s += signlst[var_radio_T2F1Lf1Lf2C1.get()]
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
    Label_saved_T2F1["foreground"] = root.cget("background")
    dir = filedialog.askdirectory(initialdir = Path(idir).parent)
    if dir != "":
        save_dir = dir
        Btn_savedir_T2F1["foreground"] = "black"
        save_flag2 = True
        if save_flag1 and save_flag2:
            Btn_save_T2F1["state"] = "normal"

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
                Label_saved_T2F1["foreground"] = "black"
        else:
            fig.savefig(save_file_name)
            Label_saved_T2F1["foreground"] = "black"
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

Tab1 = ttk.Frame(notebook)
Tab2 = ttk.Frame(notebook)

Tab1.drop_target_register(DND_FILES)
Tab1.dnd_bind("<<Drop>>", file_drop)

Tab1.pack(expand=True, fill=tk.BOTH)
Tab2.pack(expand=True, fill=tk.BOTH)
notebook.add(Tab1, text="1. データ抽出", padding=3)
notebook.add(Tab2, text="2. グラフ作成", padding=3)
notebook.pack(expand=True, fill=tk.BOTH)

##########################################################################################
#                                           tab 1
##########################################################################################
#-------------------------------------------------------------------------------
Frame1_T1 = ttk.Frame(Tab1, width=300, height=600)
Frame1_T1.propagate(False)
Frame1_T1.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
#-------------------------------------------------------------------------------
Labelframe1_T1F1 = ttk.LabelFrame(Frame1_T1, text="ファイル選択",  width=250, height=110)
Labelframe1_T1F1.propagate(False)
Labelframe1_T1F1.pack(side=tk.TOP, pady=10)

label1_T1F1Lf1 = ttk.Label(Labelframe1_T1F1, text="ここにファイルをドロップ")
label1_T1F1Lf1.pack(side=tk.TOP)
label2_T1F1Lf1 = ttk.Label(Labelframe1_T1F1, text="または")
label2_T1F1Lf1.pack(side=tk.TOP, pady=5)

Frame1_T1F1Lf1 = ttk.Frame(Labelframe1_T1F1)
Frame1_T1F1Lf1.pack(side=tk.TOP, fill=tk.BOTH)

Btn1_T1F1Lf1F1 = ttk.Button(Frame1_T1F1Lf1, text='ファイル参照', command=btn_fileref_click)
Btn1_T1F1Lf1F1.pack(side=tk.LEFT, padx=(85,0))

Btn2_T1F1Lf1F1 = ttk.Button(Frame1_T1F1Lf1, text="...", command=btn_fileref_pass_click, state="disabled", width=3)
Btn2_T1F1Lf1F1.pack(side=tk.LEFT, padx=(30,0))
#-------------------------------------------------------------------------------
Labelframe2_T1F1 = ttk.LabelFrame(Frame1_T1, text = "区切り", width=250, height=110)
Labelframe2_T1F1.propagate(False)
Labelframe2_T1F1.pack(side=tk.TOP, padx=10, pady=10)
#-------------------------------------------------------------------------------
Frame1_T1F1Lf2 = ttk.Frame(Labelframe2_T1F1, width=220, height=50)
Frame1_T1F1Lf2.propagate(False)
Frame1_T1F1Lf2.pack(side=tk.TOP, expand=True)

Var_radio_T1F1Lf2 = tk.IntVar()
Var_radio_T1F1Lf2.set(0)
Radio0_T1F1Lf2F1 = ttk.Radiobutton(Frame1_T1F1Lf2, value=0, text="空白区切り", variable=Var_radio_T1F1Lf2, command=radio_sep, state="disabled", takefocus=False)
Radio0_T1F1Lf2F1.pack(side=tk.LEFT)
Radio1_T1F1Lf2F1 = ttk.Radiobutton(Frame1_T1F1Lf2, value=1, text="カンマ(,)", variable=Var_radio_T1F1Lf2, command=radio_sep, state="disabled", takefocus=False)
Radio1_T1F1Lf2F1.pack(side=tk.LEFT)
Radio2_T1F1Lf2F1 = ttk.Radiobutton(Frame1_T1F1Lf2, value=2, text="tab(\\t)", variable=Var_radio_T1F1Lf2, command=radio_sep, state="disabled", takefocus=False)
Radio2_T1F1Lf2F1.pack(side=tk.LEFT)
#---------------------------------------
Frame2_T1F1Lf2 = ttk.Frame(Labelframe2_T1F1, width=250, height=50)
Frame2_T1F1Lf2.propagate(False)
Frame2_T1F1Lf2.pack(side=tk.TOP, expand=True)

Radio3_TF1Lf2F2 = ttk.Radiobutton(Frame2_T1F1Lf2, value=3, text="その他", variable=Var_radio_T1F1Lf2, command=radio_sep, state="disabled", takefocus=False)
Radio3_TF1Lf2F2.pack(side=tk.LEFT, padx=(13,0))

var_entry_T1F1Lf2 = tk.StringVar()
Entry_T1F1Lf2F2 = ttk.Entry(Frame2_T1F1Lf2, textvariable=var_entry_T1F1Lf2, width=5, state="disabled")
Entry_T1F1Lf2F2.pack(side=tk.LEFT)
Btn_T1F1Lf2F2 = ttk.Button(Frame2_T1F1Lf2, text="適用", state="disabled", command=btn_entry_sep_click)
Btn_T1F1Lf2F2.pack(side=tk.LEFT, padx=5)

#-------------------------------------------------------------------------------
Labelframe3_T1F1 = ttk.LabelFrame(Frame1_T1, text = "ヘッダー行", width=250, height=60)
Labelframe3_T1F1.propagate(False)
Labelframe3_T1F1.pack(side=tk.TOP, padx=10, pady=10)

var_radio_T1F1Lf3 = tk.IntVar()
var_radio_T1F1Lf3.set(0)
Radio0_T1F1Lf3 = ttk.Radiobutton(Labelframe3_T1F1, value=0, text="なし", variable=var_radio_T1F1Lf3, command=radio_header, state="disabled", takefocus=False)
Radio0_T1F1Lf3.pack(side=tk.LEFT, padx=10)
Radio1_T1F1Lf3 = ttk.Radiobutton(Labelframe3_T1F1, value=1, variable=var_radio_T1F1Lf3, command=radio_header, state="disabled", takefocus=False)
Radio1_T1F1Lf3.pack(side=tk.LEFT, padx=(10,0))

var_entry_T1F1Lf3 = tk.StringVar()
var_entry_T1F1Lf3.set("1")
Entry_T1F1Lf3 = ttk.Entry(Labelframe3_T1F1, textvariable=var_entry_T1F1Lf3, width=5, state="disabled")
Entry_T1F1Lf3.pack(side=tk.LEFT)

Label_T1F1Lf3 = ttk.Label(Labelframe3_T1F1, text="行まで", state="disabled")
Label_T1F1Lf3.pack(side=tk.LEFT)

Btn_T1F1Lf3 = ttk.Button(Labelframe3_T1F1, text="適用", state="disabled", command=btn_Entry_T1F1Lf3_click)
Btn_T1F1Lf3.pack(side=tk.LEFT)
#-------------------------------------------------------------------------------
Labelframe4_T1F1 = ttk.LabelFrame(Frame1_T1, text="軸選択", width=250, height=180)
Labelframe4_T1F1.propagate(False)
Labelframe4_T1F1.pack(side=tk.TOP)

Label_T1F1Lf4 = ttk.Label(Labelframe4_T1F1, text="列番号を選択してください", state="disabled")
Label_T1F1Lf4.pack(side=tk.TOP)

#------------------------------------------------------------
Labelframe1_T1F1Lf4 = ttk.LabelFrame(Labelframe4_T1F1, text="X軸", width=230, height=60)
Labelframe1_T1F1Lf4.propagate(False)
Labelframe1_T1F1Lf4.pack(side=tk.TOP, expand=True, pady=5)

Entry_T1F1Lf4Lf1 = ttk.Entry(Labelframe1_T1F1Lf4, state="disabled", width=5)
Entry_T1F1Lf4Lf1.pack(side=tk.LEFT, padx=(20,10))

Btn_T1F1Lf4Lf1 = ttk.Button(Labelframe1_T1F1Lf4, text="適用", state="disabled", command=btn_entry_x_axes_select_click)
Btn_T1F1Lf4Lf1.pack(side=tk.LEFT)

var_str_T1F1Lf4Lf1 = tk.StringVar()
var_str_T1F1Lf4Lf1.set("未選択")
Label_T1F1Lf4Lf1 = ttk.Label(Labelframe1_T1F1Lf4, foreground="red", textvariable=var_str_T1F1Lf4Lf1, state="disabled")
Label_T1F1Lf4Lf1.pack(side=tk.LEFT, padx=(10,0))
#------------------------------------------------------------
Labelframe2_T1F1Lf4 = ttk.LabelFrame(Labelframe4_T1F1, text="Y軸", width=230, height=60)
Labelframe2_T1F1Lf4.propagate(False)
Labelframe2_T1F1Lf4.pack(side=tk.TOP, expand=True, pady=5)

Entry_T1F1Lf4Lf2 = ttk.Entry(Labelframe2_T1F1Lf4, state="disabled", width=5)
Entry_T1F1Lf4Lf2.pack(side=tk.LEFT, padx=(20,10))

Btn_T1F1Lf4Lf2 = ttk.Button(Labelframe2_T1F1Lf4, text="適用", state="disabled", command=btn_entry_y_axes_select_click)
Btn_T1F1Lf4Lf2.pack(side=tk.LEFT)

var_str_T1F1Lf4Lf2 = tk.StringVar()
var_str_T1F1Lf4Lf2.set("未選択")
Label_T1F1Lf4Lf2 = ttk.Label(Labelframe2_T1F1Lf4, foreground="red", textvariable=var_str_T1F1Lf4Lf2, state="disabled")
Label_T1F1Lf4Lf2.pack(side=tk.LEFT, padx=(10,0))
#-------------------------------------------------------------------------------
Btn_T1F1 = ttk.Button(Frame1_T1, text="グラフ作成!", command=btn_changepage_click, state="disabled")
Btn_T1F1.pack(side=tk.TOP, pady=(15,0))
#-------------------------------------------------------------------------------
Frame2_T1 = ttk.Frame(Tab1)
Frame2_T1.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)

pt = Table(Frame2_T1, showstatusbar=True)
pt.show()


##########################################################################################
#                                        tab 2
##########################################################################################
#---------------------------------------------------------------------------------------------
Frame1_T2 = ttk.Frame(Tab2)
Frame1_T2.propagate(False)
Frame1_T2.place(x=10, y=10, width=450, height=480)


#----------3. y軸調整-----------------------------------------------------------------------
Labelframe1_T2F1 = ttk.LabelFrame(Frame1_T2, text="Y軸調整", width=300, height=250)
Labelframe1_T2F1.propagate(False)
Labelframe1_T2F1.place(x=130, y=130)

#-----------3-上限---------------------------------------------------------------------------
Labelframe1_T2F1Lf1 = ttk.LabelFrame(Labelframe1_T2F1, text="上限")
Labelframe1_T2F1Lf1.propagate(False)
Labelframe1_T2F1Lf1.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=10)

#-----------3-上限-Frame1_T2---------------------------------------
Container1_T2F1Lf1Lf1 = ttk.Frame(Labelframe1_T2F1Lf1)
Container1_T2F1Lf1Lf1.pack(side=tk.LEFT)
#-----------3-上限-Frame1_T2-ラジオボタン---------------
var_radio_T2F1Lf1Lf1C1 = tk.IntVar()
var_radio_T2F1Lf1Lf1C1.set(0)
Radio0_T2F1Lf1Lf1C1 = ttk.Radiobutton(Container1_T2F1Lf1Lf1, value=0, variable=var_radio_T2F1Lf1Lf1C1, text="+", takefocus=False)
Radio0_T2F1Lf1Lf1C1.pack(side=tk.TOP)
Radio1_T2F1Lf1Lf1C1 = ttk.Radiobutton(Container1_T2F1Lf1Lf1, value=1, variable=var_radio_T2F1Lf1Lf1C1, text="-", takefocus=False)
Radio1_T2F1Lf1Lf1C1.pack(side=tk.TOP)

#-----------3-上限-frame2_T1---------------------------------------
Container2_T2F1Lf1Lf1 = ttk.Frame(Labelframe1_T2F1Lf1)
Container2_T2F1Lf1Lf1.pack(side=tk.LEFT)
#-----------3-上限-frame2_T1-リストボックススクロール------
listbox_nums_T2F1Lf1Lf1C2 = (str(0.5*x) for x in range(0,20))
listbox_nums_T2F1Lf1Lf1C2 = list(listbox_nums_T2F1Lf1Lf1C2)
listbox_lists_T2F1Lf1Lf1C2 = tk.StringVar(value=listbox_nums_T2F1Lf1Lf1C2)
Listbox_T2F1Lf1Lf1C2 = tk.Listbox(Container2_T2F1Lf1Lf1, listvariable=listbox_lists_T2F1Lf1Lf1C2, height=4, width=5, exportselection=False)
Scrollbar_T2F1Lf1Lf1C2 = tk.Scrollbar(Container2_T2F1Lf1Lf1, orient=tk.VERTICAL, command=Listbox_T2F1Lf1Lf1C2.yview)
Listbox_T2F1Lf1Lf1C2["yscrollcommand"] = Scrollbar_T2F1Lf1Lf1C2.set
Listbox_T2F1Lf1Lf1C2.grid(row=0, column=0, padx=(10,0))
Scrollbar_T2F1Lf1Lf1C2.grid(row=0, column=1, sticky=(tk.N, tk.S))

#-----------3-上限-frame3-----------------------------------------------------------------
Container3_T2F1Lf1Lf1 = ttk.Frame(Labelframe1_T2F1Lf1)
Container3_T2F1Lf1Lf1.pack(side=tk.LEFT)
#-----------3-上限-frame3-ラベル------------------------------------------
Label_T2F1Lf1Lf1C3 = ttk.Label(Container3_T2F1Lf1Lf1, text="E+", font=("normal","12","bold"))
Label_T2F1Lf1Lf1C3.pack()

#-----------3-上限-frame4-----------------------------------------------------------------
Container4_T2F1Lf1Lf1 = ttk.Frame(Labelframe1_T2F1Lf1)
Container4_T2F1Lf1Lf1.pack(side=tk.LEFT)
#-----------3-上限-frame4-リストボックススクロール------
listbox_nums_T2F1Lf1Lf1C4 = (str(x).zfill(2) for x in range(0,21))
listbox_nums_T2F1Lf1Lf1C4 = list(listbox_nums_T2F1Lf1Lf1C4)
listbox_lists_T2F1Lf1Lf1C4 = tk.StringVar(value=listbox_nums_T2F1Lf1Lf1C4)
Listbox_T2F1Lf1Lf1C4 = tk.Listbox(Container4_T2F1Lf1Lf1, listvariable=listbox_lists_T2F1Lf1Lf1C4, height=4, width=5, exportselection=False)
Scrollbar_T2F1Lf1Lf1C4 = tk.Scrollbar(Container4_T2F1Lf1Lf1, orient=tk.VERTICAL, command=Listbox_T2F1Lf1Lf1C4.yview)
Listbox_T2F1Lf1Lf1C4["yscrollcommand"] = Scrollbar_T2F1Lf1Lf1C4.set
Listbox_T2F1Lf1Lf1C4.grid(row=0, column=0, padx=(10,0))
Scrollbar_T2F1Lf1Lf1C4.grid(row=0, column=1, sticky=(tk.N, tk.S))

#-----------3-上限-frame5-----------------------------------------------------------------
Container5_T2F1Lf1Lf1 = ttk.Frame(Labelframe1_T2F1Lf1)
Container5_T2F1Lf1Lf1.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
#-----------3-上限-frame5-適用ボタン---------------------------
Btn_T2F1Lf1Lf1C4 = ttk.Button(Container5_T2F1Lf1Lf1, text="適用", command=btn_3_max_apply_clilck, state="disabled")
Btn_T2F1Lf1Lf1C4.pack(expand=True)



#-----------3-下限------------------------------------------------------------------
Labelframe2_T2F1Lf1 = ttk.LabelFrame(Labelframe1_T2F1, text="下限")
Labelframe2_T2F1Lf1.propagate(False)
Labelframe2_T2F1Lf1.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=10, pady=10)

#-----------3-下限-Frame1_T2---------------------------------------
Container1_T2F1Lf1Lf2 = ttk.Frame(Labelframe2_T2F1Lf1)
Container1_T2F1Lf1Lf2.pack(side=tk.LEFT)
#-----------3-下限-Frame1_T2-ラジオボタン---------------
var_radio_T2F1Lf1Lf2C1 = tk.IntVar()
var_radio_T2F1Lf1Lf2C1.set(0)
Radio0_T2F1Lf1Lf2C1 = ttk.Radiobutton(Container1_T2F1Lf1Lf2, value=0, variable=var_radio_T2F1Lf1Lf2C1, text="+", takefocus=False)
Radio0_T2F1Lf1Lf2C1.pack(side=tk.TOP)
Radio1_T2F1Lf1Lf2C1 = ttk.Radiobutton(Container1_T2F1Lf1Lf2, value=1, variable=var_radio_T2F1Lf1Lf2C1, text="-", takefocus=False)
Radio1_T2F1Lf1Lf2C1.pack(side=tk.TOP)

#-----------3-下限-frame2_T1---------------------------------------
Container2_T2F1Lf1Lf2 = ttk.Frame(Labelframe2_T2F1Lf1)
Container2_T2F1Lf1Lf2.pack(side=tk.LEFT)
#-----------3-下限-frame2_T1-リストボックススクロール------
listbox_nums_T2F1Lf1Lf2C2 = (str(0.5*x) for x in range(0,20))
listbox_nums_T2F1Lf1Lf2C2 = list(listbox_nums_T2F1Lf1Lf2C2)
listbox_lists_T2F1Lf1Lf2C2 = tk.StringVar(value=listbox_nums_T2F1Lf1Lf2C2)
Listbox_T2F1Lf1Lf2C2 = tk.Listbox(Container2_T2F1Lf1Lf2, listvariable=listbox_lists_T2F1Lf1Lf2C2, height=4, width=5, exportselection=False)
Scrollbar_T2F1Lf1Lf2C2 = tk.Scrollbar(Container2_T2F1Lf1Lf2, orient=tk.VERTICAL, command=Listbox_T2F1Lf1Lf2C2.yview)
Listbox_T2F1Lf1Lf2C2["yscrollcommand"] = Scrollbar_T2F1Lf1Lf2C2.set
Listbox_T2F1Lf1Lf2C2.grid(row=0, column=0, padx=(10,0))
Scrollbar_T2F1Lf1Lf2C2.grid(row=0, column=1, sticky=(tk.N, tk.S))

#-----------3-下限-frame3-----------------------------------------------------------------
Container3_T2F1Lf1Lf2 = ttk.Frame(Labelframe2_T2F1Lf1)
Container3_T2F1Lf1Lf2.pack(side=tk.LEFT)
#-----------3-下限-frame3-ラベル------------------------------------------
Label_T2F1Lf1Lf2C3 = ttk.Label(Container3_T2F1Lf1Lf2, text="E+", font=("normal","12","bold"))
Label_T2F1Lf1Lf2C3.pack()

#-----------3-下限-frame4-----------------------------------------------------------------
Container4_T2F1Lf1Lf2 = ttk.Frame(Labelframe2_T2F1Lf1)
Container4_T2F1Lf1Lf2.pack(side=tk.LEFT)
#-----------3-下限-frame4-リストボックススクロール------
listbox_nums_T2F1Lf1Lf2C4 = (str(x).zfill(2) for x in range(0,21))
listbox_nums_T2F1Lf1Lf2C4 = list(listbox_nums_T2F1Lf1Lf2C4)
listbox_lists_T2F1Lf1Lf2C4 = tk.StringVar(value=listbox_nums_T2F1Lf1Lf2C4)
Listbox_T2F1Lf1Lf2C4 = tk.Listbox(Container4_T2F1Lf1Lf2, listvariable=listbox_lists_T2F1Lf1Lf2C4, height=4, width=5, exportselection=False)
Scrollbar_T2F1Lf1Lf2C4 = tk.Scrollbar(Container4_T2F1Lf1Lf2, orient=tk.VERTICAL, command=Listbox_T2F1Lf1Lf2C4.yview)
Listbox_T2F1Lf1Lf2C4["yscrollcommand"] = Scrollbar_T2F1Lf1Lf2C4.set
Listbox_T2F1Lf1Lf2C4.grid(row=0, column=0, padx=(10,0))
Scrollbar_T2F1Lf1Lf2C4.grid(row=0, column=1, sticky=(tk.N, tk.S))

#-----------3-下限-frame5-----------------------------------------------------------------
Container5_T2F1Lf1Lf2 = ttk.Frame(Labelframe2_T2F1Lf1)
Container5_T2F1Lf1Lf2.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
#-----------3-下限-frame5-ボタン---------------------------
Btn_T2F1Lf1Lf2C5 = ttk.Button(Container5_T2F1Lf1Lf2, text="適用", command=btn_3_min_apply_clilck, state="disabled")
Btn_T2F1Lf1Lf2C5.pack(expand=True)

#-----------保存先ボタン---------------------------------------------
Btn_savedir_T2F1 = ttk.Button(Frame1_T2, text='保存先フォルダ選択', command=btn_save_dir_click, state="disabled")
Btn_savedir_T2F1.place(x=100, y=410)

#-----------保存ボタン---------------------------------------------
Btn_save_T2F1 = ttk.Button(Frame1_T2, text='保存', state="disabled", command=btn_save_click)
Btn_save_T2F1.place(x=250, y=410)

#-----------保存しましたボタン-------------------------------------
Label_saved_T2F1 = ttk.Label(Frame1_T2, text="保存しました!", foreground=root.cget("background")) #初期はwindow背景色
Label_saved_T2F1.pack_forget()
Label_saved_T2F1.place(x=300, y=413)


#-----------グラフ出力--frame-----------------------------------------------------------
Frame2_T2 = ttk.Frame(Tab2, width=640, height=480)
Frame2_T2.propagate(False)
Frame2_T2.place(x=470, y=10)

#---ラベル---
Label_T2F2 = ttk.Label(Frame2_T2, text="ここにグラフが描画されます")
Label_T2F2.pack(expand=True)
#-------------------------------------------



root.mainloop()