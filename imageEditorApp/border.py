from tkinter import Toplevel, Label, Scale, BOTTOM, CENTER, HORIZONTAL
from tkinter import filedialog
import tkinter.ttk as ttk
import numpy as np
import cv2
from menusPosition import setScreenPosition

class BorderFrame(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master, bg='#424242')

        setScreenPosition(self,230,450,4.7)

        self.bordered_image = self.master.new_edited_photo
        self.is_bordered = False

        style = ttk.Style()
        style.map("bor.TButton", foreground=[('!active', 'cyan'),('pressed', 'slate blue'), ('active', 'light cyan')], background=[ ('!active','slate blue'),('pressed', 'cyan'), ('active', 'dark slate blue')])
        style.configure("bor.TButton", font=('Century Gothic', 14),padding=8, anchor='center', width=20, borderwidth=0)

        Label(self, text="RED", anchor=CENTER, background='#424242', font=('Century Gothic', 10), foreground='azure').pack(pady=5)
        self.trackbar_R = Scale(self, from_=0, to=255, orient=HORIZONTAL, length=200, troughcolor="dark slate blue", background='#424242', borderwidth=0,  highlightbackground='#424242', highlightthickness=0, font=('Century Gothic', 10), foreground='azure')
        self.trackbar_R.pack()

        Label(self, text="GREEN", anchor=CENTER, background='#424242', font=('Century Gothic', 10), foreground='azure').pack(pady=5)
        self.trackbar_G = Scale(self, from_=0, to=255, orient=HORIZONTAL, length=200, troughcolor="dark slate blue", background='#424242', borderwidth=0,  highlightbackground='#424242', highlightthickness=0, font=('Century Gothic', 10), foreground='azure')
        self.trackbar_G.pack()

        Label(self, text="BLUE", anchor=CENTER, background='#424242', font=('Century Gothic', 10), foreground='azure').pack(pady=5)
        self.trackbar_B = Scale(self, from_=0, to=255, orient=HORIZONTAL, length=200, troughcolor="dark slate blue", background='#424242', borderwidth=0,  highlightbackground='#424242', highlightthickness=0, font=('Century Gothic', 10), foreground='azure')
        self.trackbar_B.pack()

        Label(self, text="THICKNESS", anchor=CENTER, background='#424242', font=('Century Gothic', 10), foreground='azure').pack(pady=5)
        self.trackbar_thick = Scale(self, from_=0, to=100, resolution=10, orient=HORIZONTAL, length=200, troughcolor="dark slate blue", background='#424242', borderwidth=0,  highlightbackground='#424242', highlightthickness=0, font=('Century Gothic', 10), foreground='azure')
        self.trackbar_thick.set(1)
        self.trackbar_thick.pack()

        self.cancel_butt = ttk.Button(master=self, text="CANCEL", style="bor.TButton")
        self.cancel_butt.pack(side=BOTTOM)
        self.reset_butt = ttk.Button(master=self, text="RESET", style="bor.TButton")
        self.reset_butt.pack(side=BOTTOM)
        self.preview_butt = ttk.Button(master=self, text="PREVIEW", style="bor.TButton")
        self.preview_butt.pack(side=BOTTOM)
        self.apply_butt = ttk.Button(master=self, text="APPLY", style="bor.TButton")
        self.apply_butt.pack(side=BOTTOM)

        self.cancel_butt.bind("<ButtonPress>",self.closeBorderMenu)
        self.apply_butt.bind("<ButtonPress>",self.applyChanges)
        self.preview_butt.bind("<ButtonPress>",self.previewChanges)
        self.reset_butt.bind("<ButtonPress>",self.resetChanges)

    def getBGR(self):
        value_red = int(self.trackbar_R.get())
        value_green = int(self.trackbar_G.get())
        value_blue = int(self.trackbar_B.get())

        return [value_blue, value_green, value_red]

    def setBorderPhoto(self, color, size):
        if self.is_bordered == False:
            self.bordered_image = cv2.copyMakeBorder(self.bordered_image,size,size,size,size,cv2.BORDER_CONSTANT,value=color)
            self.is_bordered = True

    def applyChanges(self,event):
        color_border = self.getBGR()
        size = self.trackbar_thick.get()

        self.setBorderPhoto(color_border,size)

        self.master.new_edited_photo = self.bordered_image
        self.master.new_view_photo.show_image(img=self.master.new_edited_photo)
        self.destroy()

    def previewChanges(self,event):
        color_border = self.getBGR()
        size = self.trackbar_thick.get()

        self.setBorderPhoto(color_border,size)

        self.master.new_view_photo.show_image(img=self.bordered_image)

    def resetChanges(self,event):
        self.is_bordered = False
        self.trackbar_R.set(0)
        self.trackbar_G.set(0)
        self.trackbar_B.set(0)
        self.trackbar_thick.set(1)
        self.bordered_image = self.master.new_edited_photo
        self.master.new_view_photo.show_image(img=self.bordered_image)

    def closeBorderMenu(self,event):
        self.master.new_view_photo.show_image(img=self.master.new_edited_photo)
        self.destroy()
