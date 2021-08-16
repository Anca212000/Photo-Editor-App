from tkinter import Toplevel, Label, Scale, BOTTOM, CENTER, HORIZONTAL
import tkinter.ttk as ttk
import numpy as np
import cv2
from menusPosition import setScreenPosition

class AdjustFrame(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master, bg='#424242')

        setScreenPosition(self,200,680,3.8)

        self.adjust_image = self.master.new_edited_photo
        self.is_adjusted = False

        style = ttk.Style()
        style.map("adj.TButton", foreground=[('!active', 'cyan'),('pressed', 'slate blue'), ('active', 'light cyan')], background=[ ('!active','slate blue'),('pressed', 'cyan'), ('active', 'dark slate blue')])
        style.configure("adj.TButton", font=('Century Gothic', 14), padding=5, anchor='center', width=18, borderwidth=0)

        Label(self, text="RED", anchor=CENTER, background='#424242', font=('Century Gothic', 10), foreground='azure').pack(pady=5)
        self.trackbar_R = Scale(self, from_=0, to=254, orient=HORIZONTAL, length=180, troughcolor="dark slate blue", background='#424242', borderwidth=0,  highlightbackground='#424242', highlightthickness=0, font=('Century Gothic', 10), foreground='azure')
        self.trackbar_R.set(0)
        self.trackbar_R.pack()

        Label(self, text="GREEN", anchor=CENTER, background='#424242', font=('Century Gothic', 10), foreground='azure').pack(pady=5)
        self.trackbar_G = Scale(self, from_=0, to=254, orient=HORIZONTAL, length=180, troughcolor="dark slate blue", background='#424242', borderwidth=0,  highlightbackground='#424242', highlightthickness=0, font=('Century Gothic', 10), foreground='azure')
        self.trackbar_G.set(0)
        self.trackbar_G.pack()

        Label(self, text="BLUE", anchor=CENTER, background='#424242', font=('Century Gothic', 10), foreground='azure').pack(pady=5)
        self.trackbar_B = Scale(self, from_=0, to=254, orient=HORIZONTAL, length=180, troughcolor="dark slate blue", background='#424242', borderwidth=0,  highlightbackground='#424242', highlightthickness=0, font=('Century Gothic', 10), foreground='azure')
        self.trackbar_B.set(0)
        self.trackbar_B.pack()

        Label(self, text="CONTRAST", anchor=CENTER, background='#424242', font=('Century Gothic', 10), foreground='azure').pack(pady=5)
        self.track_contrast = Scale(self, from_=-127, to=127, resolution=1, orient=HORIZONTAL, length=180, troughcolor="dark slate blue", background='#424242', borderwidth=0,  highlightbackground='#424242', highlightthickness=0, font=('Century Gothic', 10), foreground='azure')
        self.track_contrast.set(0)
        self.track_contrast.pack()

        Label(self, text="BRIGHTNESS", anchor=CENTER, background='#424242', font=('Century Gothic', 10), foreground='azure').pack(pady=5)
        self.track_brightness = Scale(self, from_=-255, to=255, resolution=1, orient=HORIZONTAL, length=180, troughcolor="dark slate blue", background='#424242', borderwidth=0,  highlightbackground='#424242', highlightthickness=0, font=('Century Gothic', 10), foreground='azure')
        self.track_brightness.set(0)
        self.track_brightness.pack()

        Label(self, text="SHARPNESS", anchor=CENTER, background='#424242', font=('Century Gothic', 10), foreground='azure').pack(pady=5)
        self.track_sharpness = Scale(self, from_=9, to=12, resolution=0.1, orient=HORIZONTAL, length=180, troughcolor="dark slate blue", background='#424242', borderwidth=0,  highlightbackground='#424242', highlightthickness=0, font=('Century Gothic', 10), foreground='azure')
        self.track_sharpness.set(8)
        self.track_sharpness.pack()

        self.cancel_butt = ttk.Button(master=self, text="CANCEL", style="adj.TButton")
        self.cancel_butt.pack(side=BOTTOM)
        self.reset_butt = ttk.Button(master=self, text="RESET", style="adj.TButton")
        self.reset_butt.pack(side=BOTTOM)
        self.preview_butt = ttk.Button(master=self, text="PREVIEW", style="adj.TButton")
        self.preview_butt.pack(side=BOTTOM)
        self.apply_butt = ttk.Button(master=self, text="APPLY", style="adj.TButton")
        self.apply_butt.pack(side=BOTTOM)

        self.cancel_butt.bind("<ButtonPress>",self.closeAdjustMenu)
        self.apply_butt.bind("<ButtonPress>",self.applyChanges)
        self.preview_butt.bind("<ButtonPress>",self.viewChanges)
        self.reset_butt.bind("<ButtonPress>",self.resetAllValues)

    def closeAdjustMenu(self,event):
        self.master.new_view_photo.show_image(img=self.master.new_edited_photo)
        self.destroy()

    def getTrackbarValues(self):
        return self.trackbar_R.get(), self.trackbar_G.get(), self.trackbar_B.get(), self.track_contrast.get(), self.track_brightness.get(), self.track_sharpness.get()

    def setAdjustSettings(self):
        if self.is_adjusted == False:
            self.is_adjusted = True

            red, green, blue, contrast, brightness, sharpness = self.getTrackbarValues()

            b, g, r = cv2.split(self.adjust_image)

            if blue!=0:
                for b_value in b:
                    cv2.add(b_value, blue, b_value)
            if green!=0:
                for g_value in g:
                    cv2.add(g_value, green, g_value)
            if red!=0:
                for r_value in r:
                    cv2.add(r_value, red, r_value)

            self.adjust_image = cv2.merge((b,g,r))

            if brightness != 0:
                if brightness > 0:
                    shadow = brightness
                    max = 255
                else:
                    shadow = 0
                    max = 255 + brightness

                alpha = (max - shadow) / 255
                gamma = shadow

                self.adjust_image = cv2.addWeighted(self.adjust_image, alpha, self.adjust_image, 0, gamma)

            if contrast != 0:
                alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
                gamma = 127 * (1 - alpha)

                self.adjust_image = cv2.addWeighted(self.adjust_image, alpha, self.adjust_image, 0, gamma)

            if sharpness!=8:
                kernal=np.array([[-1,-1,-1],[-1,int(sharpness),-1],[-1,-1,-1]])
                self.adjust_image = cv2.filter2D(self.adjust_image,-1,kernal)\

    def applyChanges(self,event):
        self.setAdjustSettings()

        self.master.new_edited_photo = self.adjust_image
        self.master.new_view_photo.show_image(img=self.master.new_edited_photo)
        self.destroy()

    def viewChanges(self,event):
        self.setAdjustSettings()
        self.master.new_view_photo.show_image(img=self.adjust_image)

    def resetAllValues(self,event):
        self.is_adjusted = False
        self.trackbar_R.set(0)
        self.trackbar_G.set(0)
        self.trackbar_B.set(0)
        self.track_contrast.set(0)
        self.track_brightness.set(0)
        self.track_sharpness.set(8)
        self.adjust_image = self.master.new_edited_photo
        self.master.new_view_photo.show_image(img=self.adjust_image)
