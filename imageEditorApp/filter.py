from tkinter import Toplevel, RIGHT
import tkinter.ttk as ttk
import numpy as np
import cv2
from menusPosition import setScreenPosition


class FilterFrame(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master, bg='#424242')

        setScreenPosition(self,200,360,4)

        self.unfiltered_image = self.master.new_edited_photo
        self.filtered_image = None

        style = ttk.Style()
        style.map("C.TButton", foreground=[('!active', 'cyan'),('pressed', 'slate blue'), ('active', 'light cyan')], background=[ ('!active','slate blue'),('pressed', 'cyan'), ('active', 'dark slate blue')])
        style.configure("C.TButton", font=('Century Gothic', 15),padding=10, anchor='center', width=16, borderwidth=0)

        self.negative_button = ttk.Button(master=self, text="NEGATIVE", style="C.TButton") #bg='slate blue', fg='cyan', font=font.Font(family='Century Gothic', size=15, weight='bold'), padx=5, width=18, activebackground= 'dark slate blue',activeforeground='light cyan', command=self.color_butt_change)
        self.negative_button.pack()

        self.bl_wh_button = ttk.Button(master=self, text="BLACK WHITE", style="C.TButton")
        self.bl_wh_button.pack()

        self.sepia_button = ttk.Button(master=self, text="SEPIA", style="C.TButton")
        self.sepia_button.pack()

        self.emboss_button = ttk.Button(master=self, text="EMBOSS", style="C.TButton")
        self.emboss_button.pack()

        self.gauss_blur_button = ttk.Button(master=self, text="GAUSSIAN BLUR", style="C.TButton")
        self.gauss_blur_button.pack()

        self.median_blur_button = ttk.Button(master=self, text="MEDIAN BLUR", style="C.TButton")
        self.median_blur_button.pack()

        self.apply_button = ttk.Button(master=self, text="APPLY", style="C.TButton")
        self.apply_button.pack()

        self.cancel_button = ttk.Button(master=self, text="CANCEL", style="C.TButton", command=self.closeFilters)
        self.cancel_button.pack()

        self.negative_button.bind('<ButtonPress>',self.negative_button_pressed)
        self.bl_wh_button.bind('<ButtonPress>',self.bl_wh_button_pressed)
        self.sepia_button.bind('<ButtonPress>',self.sepia_button_pressed)
        self.emboss_button.bind('<ButtonPress>',self.emboss_button_pressed)
        self.gauss_blur_button.bind('<ButtonPress>',self.gauss_blur_button_pressed)
        self.median_blur_button.bind('<ButtonPress>',self.median_blur_button_pressed)
        self.apply_button.bind('<ButtonPress>',self.apply_button_pressed)

    def negative_button_pressed(self,event):
        image = self.unfiltered_image.copy()

        row = image.shape[0]
        col = image.shape[1]

        negative = image.copy()

        for i in range(row):
            for j in range(col):
                negative[i][j] = 255 - negative[i][j]

        self.filtered_image = negative
        self.master.new_view_photo.show_image(img=self.filtered_image)

    def bl_wh_button_pressed(self,event):
        image = self.unfiltered_image.copy()

        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.filtered_image = gray_img
        self.master.new_view_photo.show_image(img=self.filtered_image)

    def sepia_button_pressed(self,event):
        image = self.unfiltered_image.copy()

        intensity = 0.5

        try:
            image.shape[3]
        except IndexError:
            image = cv2.cvtColor(image,cv2.COLOR_BGR2BGRA)

        fr_h, fr_w, fr_c = image.shape

        blue = 20
        green = 66
        red = 112

        sepia_bgra = (blue, green, red, 1)
        overlay = np.full((fr_h, fr_w, 4), sepia_bgra, dtype='uint8')

        cv2.addWeighted(overlay, intensity, image, 1.0, 0, image)

        self.filtered_image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
        self.master.new_view_photo.show_image(img=self.filtered_image)

    def emboss_button_pressed(self, event):
        image = self.unfiltered_image.copy()

        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        filter = np.zeros((3, 3), dtype=np.int8)

        for i in range(3):
            for j in range(3):
                if i < j:
                    filter[i][j] = -1
                elif i > j:
                    filter[i][j] = 1

        height = image.shape[0]
        width = image.shape[1]

        offset = 128

        y = np.ones((height, width), np.uint8) * offset
        
        emboss_img = cv2.add(cv2.filter2D(gray_img, -1, filter), y)

        self.filtered_image = emboss_img
        self.master.new_view_photo.show_image(img=self.filtered_image)

    def gauss_blur_button_pressed(self, event):
        image = self.unfiltered_image.copy()

        blur_image = cv2.GaussianBlur(image,(5,5),0)

        self.filtered_image = blur_image
        self.master.new_view_photo.show_image(img=self.filtered_image)

    def median_blur_button_pressed(self, event):
        image = self.unfiltered_image.copy()

        blur_image = cv2.medianBlur(image,5)

        self.filtered_image = blur_image
        self.master.new_view_photo.show_image(img=self.filtered_image)

    def apply_button_pressed(self, event):
        self.master.new_edited_photo = self.filtered_image
        self.master.new_view_photo.show_image(img=self.master.new_edited_photo)
        self.destroy()

    def closeFilters(self):
        image_initial = self.unfiltered_image
        self.master.new_view_photo.show_image(img=image_initial)
        self.destroy()
