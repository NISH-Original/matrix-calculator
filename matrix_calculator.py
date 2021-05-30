from tkinter import *
from sys import exit
import numpy as np
from tkinter import messagebox
from tkinter import ttk

global lst1
lst1 = []

global lst2
lst2 = []

#A special type of entry that only accepts int as input
class IntEntry(Entry):
    def __init__(self, master=None, **kwargs):
        self.var = StringVar()
        Entry.__init__(self, master, textvariable=self.var, **kwargs)
        self.old_value = ''
        self.var.trace('w', self.check)
        self.get, self.set = self.var.get, self.var.set

    def check(self, *args):
        if len(self.get()) > 4:
            self.set(self.get()[:4])
            
#A widget that shows the descrition of an element when the mouse is hovered over it
class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

def DoItAgain():
    matrix1.destroy()
    matrix2.destroy()
    result_window.destroy()
    Submit.config(state=NORMAL)
    
def Quit():
    exit()

def EnterMatrix2(event = None):
    global Compute
    Compute.config(state=DISABLED)
    global lst2
    lst2 = []
    row_lst2 = []
    i = 0
    while i < int(total_rows2):
        for j in range(int(total_columns2)):
            if len(globals()["e2"+str(i+1)+str(j+1)].get()) == 0:
                globals()["entry2"+str(i+1)+str(j+1)] = 0 
            else:    
                try:
                    globals()["entry2"+str(i+1)+str(j+1)] = int(globals()["e2"+str(i+1)+str(j+1)].get())
                except:
                    messagebox.showerror("ERROR","Please enter a valid number!")
                    Next.config(state=DISABLED)
            row_lst2.append(globals()["entry2"+str(i+1)+str(j+1)])
        lst2.append(row_lst2)
        row_lst2 = []
        i += 1
    for row in lst2:
        print(row)
    if operation_used == "Multiply":
        result = [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*lst2)] for X_row in lst1]
    elif operation_used == "Add":
        result = [[lst1[i][j] + lst2[i][j]  for j in range(len(lst1[0]))] for i in range(len(lst1))]
    elif operation_used == "Subtract":
        result = [[lst1[i][j] - lst2[i][j]  for j in range(len(lst1[0]))] for i in range(len(lst1))]
    
    print("Result: ")
    for r in result:
        print(r)

    #prints result in GUI
    global result_window
    result_window = Toplevel()
    result_window.title("result")
    result_window.resizable(False, False)
    for i in range(int(len(result))):
        for j in range(len(result[0])):
            globals()["result"+str(i+1)+str(j+1)] = Entry(result_window, width=7, fg='green', font=('Arial',16,'bold'))
            globals()["result"+str(i+1)+str(j+1)].grid(row=i, column=j)
            globals()["result"+str(i+1)+str(j+1)].insert(END, result[i][j])
    Again = Button(result_window, text="Again", padx=10, pady=2, command = DoItAgain)
    Again.grid(row = 2, column = total_columns1+2)
    Quit_button = Button(result_window, text="Quit", padx=13, pady=2, command = Quit)
    Quit_button.grid(row = 1, column = total_columns1+2)

def AskForMatrix2(event = None):
    global Next
    Next.config(state=DISABLED)
    global lst1
    lst1 = []
    row_lst1 = []
    i = 0
    while i < int(total_rows1):
        for j in range(int(total_columns1)):
            if len(globals()["e1"+str(i+1)+str(j+1)].get()) == 0:
                globals()["entry1"+str(i+1)+str(j+1)] = 0 
            else:    
                try:
                    globals()["entry1"+str(i+1)+str(j+1)] = int(globals()["e1"+str(i+1)+str(j+1)].get())
                except:
                    messagebox.showerror("ERROR","Please enter a valid number!")
                    Submit.config(state=NORMAL)
            row_lst1.append(globals()["entry1"+str(i+1)+str(j+1)])
        lst1.append(row_lst1)
        row_lst1 = []
        i += 1
    for row in lst1:
        print(row)
    global matrix2
    matrix2 = Toplevel()
    matrix2.configure(bg = '#3d3d3d')
    matrix2.title("matrix 2")
    matrix2.resizable(False, False)
    for i in range(int(total_rows2)):
        for j in range(int(total_columns2)):
            globals()["e2"+str(i+1)+str(j+1)] = IntEntry(matrix2, width=5, fg='blue', font=('Arial',16,'bold'))
            globals()["e2"+str(i+1)+str(j+1)].grid(row=i, column=j)
            CreateToolTip(globals()["e2"+str(i+1)+str(j+1)], text = '{},{}'.format(i+1, j+1))
    global Compute
    Compute = Button(matrix2, text="Compute", padx=10, pady=2, command = EnterMatrix2)
    Compute.grid(row = 2, column = total_columns2+2)

    
def AskForMatrix1(event = None):
    global Submit
    Submit.config(state=DISABLED)
    global Next
    global total_rows1
    global total_columns1
    global total_rows2
    global total_columns2
    global operation_used

    total_rows1 = total_rows_1.get()
    total_columns1 = total_columns_1.get()
    total_rows2 = total_rows_2.get()
    total_columns2 = total_columns_2.get()
    operation_used = operation.get()

    def display_matrix_1_window():
        global matrix1
        matrix1 = Toplevel()
        matrix1.configure(bg = '#3d3d3d')
        matrix1.title("matrix 1")
        matrix1.resizable(False, False)
        for i in range(int(total_rows1)):
            for j in range(int(total_columns1)):
                globals()["e1"+str(i+1)+str(j+1)] = IntEntry(matrix1, width=5, fg='blue', font=('Arial',16,'bold'))
                globals()["e1"+str(i+1)+str(j+1)].grid(row=i, column=j)
                CreateToolTip(globals()["e1"+str(i+1)+str(j+1)], text = '{},{}'.format(i+1, j+1))
        global Next
        Next = Button(matrix1, text="Next", padx=10, pady=2, command = AskForMatrix2)
        Next.grid(row = 2, column = total_columns1+2)
    
    if operation_used == "Multiply":
        if int(total_rows2) != int(total_columns1):
            messagebox.showerror("ERROR","Rows of matrix 2 must be equal to\ncolumns of matrix 1 for multiplication!")
        else:
            display_matrix_1_window()
    elif operation_used == "Add" or operation_used == "Subtract":
        if int(total_rows1) != int(total_rows2) or int(total_columns1) != int(total_columns2):
            messagebox.showerror("ERROR","Rows and columns of both the matrices must be equal\nfor addition and subtraction!")
        else:
            display_matrix_1_window()
    if operation_used == "Choose one":
        messagebox.showerror("ERROR","Please choose an operation!")

menu = Tk()
menu.title("Matrices Calculator")
menu.resizable(False, False)
menu.geometry("350x300")
menu.configure(bg = '#3d3d3d')
options1 = [1,2,3,4,5]

total_rows_1 = IntVar(menu)
total_rows_1.set(options1[2])
dropdown1 = OptionMenu(menu, total_rows_1, *options1)

total_columns_1 = IntVar(menu)
total_columns_1.set(options1[2])
dropdown2 = OptionMenu(menu, total_columns_1, *options1)

total_rows_2 = IntVar(menu)
total_rows_2.set(options1[2])
dropdown3 = OptionMenu(menu, total_rows_2, *options1)

total_columns_2 = IntVar(menu)
total_columns_2.set(options1[2])
dropdown4 = OptionMenu(menu, total_columns_2, *options1)

options2 = ["Choose one","Add", "Subtract", "Multiply"]
operation = StringVar(menu)
operation.set(options2[0])
dropdown5 = OptionMenu(menu, operation, *options2)

dropdown1.place(relx=0.35, rely=0.40, anchor=CENTER)
dropdown2.place(relx=0.6, rely=0.40, anchor=CENTER)
dropdown3.place(relx=0.35, rely=0.6, anchor=CENTER)
dropdown4.place(relx=0.6, rely=0.6, anchor=CENTER)
dropdown5.place(relx=0.47, rely=0.78, anchor=CENTER)

total_rows_1_label = Label(menu,text="Matrix 1:",font=("Arial Bold",10),  bg = '#3d3d3d', fg = 'white')
rows_table = Label(menu,text="Rows",font=("Arial Bold",10),  bg = '#3d3d3d', fg = 'white')
total_rows_2_label = Label(menu,text="Matrix 2:",font=("Arial Bold",10),  bg = '#3d3d3d', fg = 'white')
columns_table = Label(menu,text="Columns",font=("Arial Bold",10),  bg = '#3d3d3d', fg = 'white')
operation_label = Label(menu,text="Operation:",font=("Arial Bold",10),  bg = '#3d3d3d', fg = 'white')
main_name = Label(menu,text="Matrices Calculator",font=("Arial Bold",20),  bg = '#3d3d3d', fg = 'white')
sub_name = Label(menu,text="By NISH",font=("Arial Bold",10),  bg = '#3d3d3d', fg = 'white')

total_rows_1_label.place(relx=0.15,rely=0.40,anchor=CENTER)
rows_table.place(relx=0.35,rely=0.3,anchor=CENTER)
total_rows_2_label.place(relx=0.15,rely=0.6,anchor=CENTER)
columns_table.place(relx=0.6,rely=0.3,anchor=CENTER)
operation_label.place(relx=0.173, rely=0.78, anchor=CENTER)
main_name.place(relx=0.4, rely=0.1, anchor=CENTER)
sub_name.place(relx=0.12, rely=0.18, anchor=CENTER)

global Submit
Submit = Button(text="Submit", padx=10, pady=1.5, font=('Arial',10), bg="green", fg="white", command = AskForMatrix1)
Submit.place(relx=0.47, rely=0.92, anchor=CENTER)

menu.mainloop()