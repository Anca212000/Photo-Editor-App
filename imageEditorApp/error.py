import tkinter.messagebox as messBox
from tkinter import Toplevel, Label, BOTTOM, CENTER, HORIZONTAL
import tkinter.ttk as ttk

def showError(self):
    global message_box
    message_box = Toplevel(self)
    message_box.title("No image selected")
    message_box.geometry("300x140+%d+%d" % ((self.master.winfo_screenwidth() - 250)/2,(self.master.winfo_screenheight() - 150)/2))
    message_box.config(bg='#18002d')

    mess_label = Label(message_box,text="Select an image first!", foreground="salmon",background='#18002d', font=("Century Gothic",18))
    mess_label.pack(padx=10,pady=18)

    style = ttk.Style()
    style.configure("ok.TButton", padding='5', font=("Century Gothic",16,"bold"), width=4, foreground='salmon')

    ok_button = ttk.Button(message_box, text=" OK ", style="ok.TButton")
    ok_button.pack(side=BOTTOM, pady=10)
    ok_button.bind("<ButtonPress>", closeMessageBox)

def closeMessageBox(self):
    global message_box
    message_box.destroy()
