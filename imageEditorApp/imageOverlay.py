from tkinter import Toplevel, Label, Scale, CENTER, BOTTOM, HORIZONTAL
from tkinter import filedialog
import tkinter.ttk as ttk
import numpy as np
import cv2
from menusPosition import setScreenPosition


class ImageOverlay(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master, bg='#424242')

        self.title("Set transparency")

        setScreenPosition(self,240,220,5)

        self.img_under =  self.master.new_edited_photo
        self.image_blend = None
        self.is_overlay = False

        filename = filedialog.askopenfilename()
        self.img_overlay = cv2.imread(filename)

        style = ttk.Style()
        style.map("overImg.TButton", foreground=[('!active', 'cyan'),('pressed', 'slate blue'), ('active', 'light cyan')], background=[ ('!active','slate blue'),('pressed', 'cyan'), ('active', 'dark slate blue')])
        style.configure("overImg.TButton", font=('Century Gothic', 14),padding=3, anchor='center', width=24, borderwidth=0)

        Label(self, text="Transparency", anchor=CENTER, background='#424242', font=('Century Gothic', 10), foreground='azure').pack(pady=5)
        self.bar_opacity = Scale(self, from_=0, to=1, resolution=0.1, orient=HORIZONTAL, length=220, troughcolor="dark slate blue", background='#424242', borderwidth=0,  highlightbackground='#424242', highlightthickness=0, font=('Century Gothic', 10), foreground='azure')
        self.bar_opacity.set(0)
        self.bar_opacity.pack()

        self.cancel_opac_butt = ttk.Button(self, text="CANCEL", style="overImg.TButton")
        self.cancel_opac_butt.pack(side=BOTTOM)
        self.reset_opac_butt = ttk.Button(self, text="RESET", style="overImg.TButton")
        self.reset_opac_butt.pack(side=BOTTOM)
        self.preview_opac_butt = ttk.Button(self, text="PREVIEW", style="overImg.TButton")
        self.preview_opac_butt.pack(side=BOTTOM)
        self.apply_opac_butt = ttk.Button(self, text="APPLY", style="overImg.TButton")
        self.apply_opac_butt.pack(side=BOTTOM)

        self.apply_opac_butt.bind("<ButtonPress>", self.apply_changes)
        self.preview_opac_butt.bind("<ButtonPress>", self.preview_changes)
        self.reset_opac_butt.bind("<ButtonPress>", self.reset_changes)
        self.cancel_opac_butt.bind("<ButtonPress>", self.cancel_changes)

    def apply_changes(self,event):
        self.setOverlay()
        self.master.new_edited_photo = self.image_blend
        self.master.new_view_photo.show_image(img=self.master.new_edited_photo)
        self.destroy()

    def setOverlay(self):
        if self.is_overlay == False:
            self.is_overlay = True
            value_opacity = self.bar_opacity.get()
            height_img_under, width_img_under, channels_img_under = self.img_under.shape
            resized_img_overlay = cv2.resize(self.img_overlay, (width_img_under,height_img_under), interpolation = cv2.INTER_AREA)
            self.image_blend = cv2.addWeighted(self.img_under,0.8,resized_img_overlay,value_opacity,0)

    def preview_changes(self,event):
        self.setOverlay()
        self.master.new_view_photo.show_image(img=self.image_blend)

    def reset_changes(self,event):
        self.bar_opacity.set(0)
        self.is_overlay = False
        self.image_blend = self.master.new_edited_photo
        self.master.new_view_photo.show_image(img=self.image_blend)

    def cancel_changes(self,event):
        self.master.new_view_photo.show_image(img=self.img_under)
        self.destroy()
