from tkinter import Toplevel, Label, Scale, Entry, StringVar, OptionMenu, BOTTOM, CENTER, HORIZONTAL
import tkinter.ttk as ttk
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import cv2
import os
from menusPosition import setScreenPosition

class TextFrame(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master, bg='#424242')

        setScreenPosition(self,280,680,6.5)

        self.added_text_img = self.master.new_edited_photo
        self.is_added_text = False

        Label(self, text="Enter text", background='#424242', font=('Century Gothic', 12), foreground='azure').pack(pady=2)
        self.input_text = Entry(self, bd = 1, bg="dark slate blue", fg="azure", width=40)
        self.input_text.pack()

        self.OPTIONS_FONT = [
        "Century Gothic",
        "Augusta",
        "Christmas Sparkle",
        "Gameplay",
        "Lemon Friday"
        ]

        self.OPTIONS_FONT_S = [10,20,30,50,60,70,80,90,100]

        Label(self, text="Select font-family:", background='#424242', font=('Century Gothic', 12), foreground='azure').pack(pady=2)
        self.font_fam = StringVar(self)
        self.font_fam.set(self.OPTIONS_FONT[0])

        self.opt_font_fam = OptionMenu(self, self.font_fam, *self.OPTIONS_FONT)
        self.opt_font_fam.pack()
        self.opt_font_fam.config(bg="dark slate blue", fg="azure")

        Label(self, text="Select font-size:", background='#424242', font=('Century Gothic', 12), foreground='azure').pack(pady=5)
        self.font_size = StringVar(self)
        self.font_size.set(self.OPTIONS_FONT_S[0])

        self.opt_font_size = OptionMenu(self, self.font_size, *self.OPTIONS_FONT_S)
        self.opt_font_size.pack(pady=2)
        self.opt_font_size.config(bg="dark slate blue", fg="azure")

        Label(self, text="RED", anchor=CENTER, background='#424242', font=('Century Gothic', 10), foreground='azure').pack(pady=3)
        self.trackbar_R = Scale(self, from_=0, to=254, orient=HORIZONTAL, length=240, troughcolor="dark slate blue", background='#424242', borderwidth=0,  highlightbackground='#424242', highlightthickness=0, font=('Century Gothic', 10), foreground='azure')
        self.trackbar_R.set(0)
        self.trackbar_R.pack()

        Label(self, text="GREEN", anchor=CENTER, background='#424242', font=('Century Gothic', 10), foreground='azure').pack(pady=3)
        self.trackbar_G = Scale(self, from_=0, to=254, orient=HORIZONTAL, length=240, troughcolor="dark slate blue", background='#424242', borderwidth=0,  highlightbackground='#424242', highlightthickness=0, font=('Century Gothic', 10), foreground='azure')
        self.trackbar_G.set(0)
        self.trackbar_G.pack()

        Label(self, text="BLUE", anchor=CENTER, background='#424242', font=('Century Gothic', 10), foreground='azure').pack(pady=3)
        self.trackbar_B = Scale(self, from_=0, to=254, orient=HORIZONTAL, length=240, troughcolor="dark slate blue", background='#424242', borderwidth=0,  highlightbackground='#424242', highlightthickness=0, font=('Century Gothic', 10), foreground='azure')
        self.trackbar_B.set(0)
        self.trackbar_B.pack()

        height = self.added_text_img.shape[0]
        width = self.added_text_img.shape[1]

        Label(self, text="X:", background='#424242', font=('Century Gothic', 10), foreground='azure').pack(pady=3)
        self.coord_x = Scale(self, from_=0, to=int(width), orient=HORIZONTAL, length=240, troughcolor="dark slate blue", background='#424242', borderwidth=0,  highlightbackground='#424242', highlightthickness=0, font=('Century Gothic', 10), foreground='azure')
        self.coord_x.set(0)
        self.coord_x.pack()

        Label(self, text="Y:", background='#424242', font=('Century Gothic', 10), foreground='azure').pack(pady=3)
        self.coord_y = Scale(self, from_=0, to=int(height), orient=HORIZONTAL, length=240, troughcolor="dark slate blue", background='#424242', borderwidth=0,  highlightbackground='#424242', highlightthickness=0, font=('Century Gothic', 10), foreground='azure')
        self.coord_y.set(0)
        self.coord_y.pack()

        style = ttk.Style()
        style.map("text.TButton", foreground=[('!active', 'cyan'),('pressed', 'slate blue'), ('active', 'light cyan')], background=[ ('!active','slate blue'),('pressed', 'cyan'), ('active', 'dark slate blue')])
        style.configure("text.TButton", font=('Century Gothic', 14),padding=6, anchor='center', width=26, borderwidth=0)

        self.cancel_butt = ttk.Button(master=self, text="CANCEL", style="text.TButton")
        self.cancel_butt.pack(side=BOTTOM)
        self.reset_butt = ttk.Button(master=self, text="RESET", style="text.TButton")
        self.reset_butt.pack(side=BOTTOM)
        self.preview_butt = ttk.Button(master=self, text="PREVIEW", style="text.TButton")
        self.preview_butt.pack(side=BOTTOM)
        self.apply_butt = ttk.Button(master=self, text="APPLY", style="text.TButton")
        self.apply_butt.pack(side=BOTTOM)

        self.cancel_butt.bind("<ButtonPress>",self.closeTextWindow)
        self.apply_butt.bind("<ButtonPress>",self.applyChanges)
        self.preview_butt.bind("<ButtonPress>",self.previewChanges)
        self.reset_butt.bind("<ButtonPress>",self.resetChanges)

    def putTextOnImage(self):
        if self.is_added_text == False:
            self.is_added_text = True
            text = self.input_text.get()
            font_family = self.font_fam.get()
            font_size = self.font_size.get()

            b = self.trackbar_B.get()
            g = self.trackbar_G.get()
            r = self.trackbar_R.get()

            x = self.coord_x.get()
            y = self.coord_y.get()

            fontpath = f"./fonts/{font_family}.ttf"

            font = ImageFont.truetype(fontpath, int(font_size))
            img_pil = Image.fromarray(self.added_text_img)
            draw = ImageDraw.Draw(img_pil)
            draw.text((x, y), text, font = font, fill = (b, g, r))
            self.added_text_img = np.array(img_pil)

    def applyChanges(self,event):
        self.putTextOnImage()

        self.master.new_edited_photo = self.added_text_img
        self.master.new_view_photo.show_image(img=self.master.new_edited_photo)
        self.destroy()

    def previewChanges(self,event):
        self.putTextOnImage()

        self.master.new_view_photo.show_image(img=self.added_text_img)

    def resetChanges(self,event):
        self.is_added_text = False
        self.input_text.delete(0,len(self.input_text.get()))
        self.font_fam.set(self.OPTIONS_FONT[0])
        self.font_size.set(self.OPTIONS_FONT_S[0])
        self.trackbar_R.set(0)
        self.trackbar_G.set(0)
        self.trackbar_B.set(0)
        self.coord_x.set(0)
        self.coord_y.set(0)
        self.added_text_img = self.master.new_edited_photo
        self.master.new_view_photo.show_image(img=self.added_text_img)

    def closeTextWindow(self,event):
        self.master.new_view_photo.show_image(img=self.master.new_edited_photo)
        self.destroy()
