from tkinter import Toplevel, Label, Scale, TOP, CENTER, HORIZONTAL
from tkinter import filedialog
import tkinter.ttk as ttk
import numpy as np
import cv2
from menusPosition import setScreenPosition

class CollageFrame(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master, bg='#424242')

        setScreenPosition(self,245,208,5.2)

        self.first_image = self.master.new_edited_photo
        self.second_image = None
        self.collage_image = self.first_image
        self.is_second_img = False
        self.is_both_resized = False

        style = ttk.Style()
        style.map("coll.TButton", foreground=[('!active', 'cyan'),('pressed', 'slate blue'), ('active', 'light cyan')], background=[ ('!active','slate blue'),('pressed', 'cyan'), ('active', 'dark slate blue')])
        style.configure("coll.TButton", font=('Century Gothic', 14),padding=14, anchor='center', width=28, borderwidth=0)

        self.horiz_img_butt = ttk.Button(self, text="2 HORIZONTAL IMAGES", style="coll.TButton")
        self.horiz_img_butt.pack(side=TOP)
        self.vert_img_butt = ttk.Button(self, text="2 VERTICAL IMAGES", style="coll.TButton")
        self.vert_img_butt.pack(side=TOP)
        self.apply_coll_butt = ttk.Button(self, text="APPLY", style="coll.TButton")
        self.apply_coll_butt.pack(side=TOP)
        self.cancel_coll_butt = ttk.Button(self, text="CANCEL", style="coll.TButton")
        self.cancel_coll_butt.pack(side=TOP)

        self.horiz_img_butt.bind("<ButtonPress>", self.horizontal_images)
        self.vert_img_butt.bind("<ButtonPress>", self.vertical_images)
        self.apply_coll_butt.bind("<ButtonPress>", self.apply_changes)
        self.cancel_coll_butt.bind("<ButtonPress>", self.cancel_changes)

    def openSecondImage(self):
        if self.is_second_img == False:
            self.is_second_img = True
            filename = filedialog.askopenfilename()
            self.second_image = cv2.imread(filename)
            height = self.first_image.shape[0]
            width = self.first_image.shape[1]
            resized_img = cv2.resize(self.second_image, (width,height), interpolation = cv2.INTER_AREA)
            self.second_image = resized_img

    def resizeBothImages(self):
        if self.is_both_resized == False:
            self.is_both_resized = True
            self.first_image= cv2.resize(self.first_image, (0,0), None, 0.5, 0.5)
            self.second_image= cv2.resize(self.second_image, (0,0), None, 0.5, 0.5)

    def horizontal_images(self,event):
        self.openSecondImage()
        self.resizeBothImages()

        self.collage_image = np.hstack((self.first_image,self.second_image))

        self.master.new_view_photo.show_image(img=self.collage_image)

    def vertical_images(self,event):
        self.openSecondImage()
        self.resizeBothImages()

        self.collage_image = np.vstack((self.first_image,self.second_image))

        self.master.new_view_photo.show_image(img=self.collage_image)

    def apply_changes(self,event):
        self.master.new_edited_photo = self.collage_image
        final_image = self.collage_image
        self.master.new_view_photo.show_image(img=final_image)
        self.destroy()

    def cancel_changes(self,event):
        self.master.new_view_photo.show_image(img=self.master.new_edited_photo)
        self.destroy()
