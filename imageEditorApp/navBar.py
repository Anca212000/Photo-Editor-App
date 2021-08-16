from tkinter import *
from tkinter import filedialog
import tkinter.messagebox as messBox
import tkinter.ttk as ttk
import cv2
from filter import FilterFrame
from adjust import AdjustFrame
from imageOverlay import ImageOverlay
from collage import CollageFrame
from border import BorderFrame
from text import TextFrame
from menusPosition import setScreenPosition
import error as boxError


class NavigationBar(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master=master)

        self.new_edited_photo = None
        self.new_view_photo = None
        self.filename = ""
        self.is_image_selected = False

        self.addNavButtons()

    def addNavButtons(self):
        style = ttk.Style()
        style.map("main.TButton", foreground=[('!active', 'cyan'),('pressed', 'slate blue'), ('active', 'light cyan')], background=[ ('!active','slate blue'),('pressed', 'cyan'), ('active', 'dark slate blue')])
        style.configure("main.TButton", font=('Century Gothic', 15),padding=12.5, anchor=CENTER, width=16, borderwidth=0)

        self.new_button = ttk.Button(self, text="NEW", style="main.TButton")
        self.new_button.pack()

        self.save_button = ttk.Button(self, text="SAVE", style="main.TButton")
        self.save_button.pack()

        self.save_as_button = ttk.Button(self, text="SAVE AS", style="main.TButton")
        self.save_as_button.pack()

        self.filter_button = ttk.Button(self, text="FILTER", style="main.TButton")
        self.filter_button.pack()

        self.adjust_button = ttk.Button(self, text="ADJUST", style="main.TButton")
        self.adjust_button.pack()

        self.image_over_button = ttk.Button(self, text="IMAGE OVERLAY", style="main.TButton")
        self.image_over_button.pack()

        self.collage_button = ttk.Button(self, text="COLLAGE", style="main.TButton")
        self.collage_button.pack()

        self.add_text_button = ttk.Button(self, text="ADD TEXT", style="main.TButton")
        self.add_text_button.pack()

        self.add_frame_button = ttk.Button(self, text="ADD FRAME", style="main.TButton")
        self.add_frame_button.pack()

        self.discard_button = ttk.Button(self, text="DISCARD", style="main.TButton")
        self.discard_button.pack()

        self.quit_button = ttk.Button(self, text="EXIT", style="main.TButton", command=self.quit)
        self.quit_button.pack()

        self.new_button.bind("<ButtonPress>", self.new_button_pressed)
        self.save_button.bind("<ButtonPress>", self.save_button_pressed)
        self.save_as_button.bind("<ButtonPress>", self.save_as_button_pressed)
        self.filter_button.bind("<ButtonPress>", self.filter_button_pressed)
        self.adjust_button.bind("<ButtonPress>", self.adjust_button_pressed)
        self.image_over_button.bind("<ButtonPress>", self.image_over_button_pressed)
        self.collage_button.bind("<ButtonPress>", self.collage_button_pressed)
        self.add_text_button.bind("<ButtonPress>", self.add_text_button_pressed)
        self.add_frame_button.bind("<ButtonPress>", self.add_frame_button_pressed)
        self.discard_button.bind("<ButtonPress>", self.discard_button_pressed)

    def new_button_pressed(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.new_button:
            filename = filedialog.askopenfilename(title="Choose a file",
            filetypes=[('image files', (".jpg",".jpeg",".jfif",".png",".bmp",".tiff",".tif"))])
            image = cv2.imread(filename)

            if image is not None:
                self.filename = filename
                self.master.original_image = image.copy()
                self.new_edited_photo = image.copy()
                self.master.view_photo.show_image(img=self.new_edited_photo)
                self.is_image_selected = True

    def save_button_pressed(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.save_button:
            if(self.is_image_selected == False):
                boxError.showError(self)
            else:
                used_image = self.new_edited_photo
                image_filename = self.filename
                cv2.imwrite(image_filename, used_image)

    def save_as_button_pressed(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.save_as_button:
            if(self.is_image_selected == False):
                boxError.showError(self)
            else:
                filename = filedialog.asksaveasfilename(filetypes=(("JPEG/JFIF files", "*.jpg *.jpeg *.jfif"),
                ("PNG files","*.png"),
                ("BITMAP files","*.bmp"),
                ("TIFF/TIF files","*.tiff *.tif"),
                ),
                )
                type_extension = [".jpg",".jpeg",".jfif",".png",".bmp",".tiff",".tif"]
                if filename == '':
                    return

                check_type = False
                for type in type_extension:
                    if filename.endswith(type):
                        check_type = True
                        break

                if check_type == False:
                    if(filename.find(".") != -1):
                        filename = filename.split('.')[0]
                    filename += ".jpg"

                save_image = self.new_edited_photo
                cv2.imwrite(filename, save_image)
                self.filename = filename

    def filter_button_pressed(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.filter_button:
            if(self.is_image_selected == False):
                boxError.showError(self)
            else:
                self.new_view_photo = self.master.view_photo
                self.master.processed_image = self.new_edited_photo
                self.master.filter_frame = FilterFrame(master=self)
                self.master.filter_frame.grab_set()

    def adjust_button_pressed(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.adjust_button:
            if(self.is_image_selected == False):
                boxError.showError(self)
            else:
                self.new_view_photo = self.master.view_photo
                self.master.processed_image = self.new_edited_photo
                self.master.adjust_frame = AdjustFrame(master=self)
                self.master.adjust_frame.grab_set()

    def image_over_button_pressed(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.image_over_button:
            if(self.is_image_selected == False):
                boxError.showError(self)
            else:
                self.new_view_photo = self.master.view_photo
                self.master.processed_image = self.new_edited_photo
                self.master.image_overlay_frame = ImageOverlay(master=self)
                self.master.image_overlay_frame.grab_set()

    def collage_button_pressed(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.collage_button:
            if(self.is_image_selected == False):
                boxError.showError(self)
            else:
                self.new_view_photo = self.master.view_photo
                self.master.processed_image = self.new_edited_photo
                self.master.collage_frame = CollageFrame(master=self)
                self.master.collage_frame.grab_set()

    def add_text_button_pressed(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.add_text_button:
            if(self.is_image_selected == False):
                boxError.showError(self)
            else:
                self.new_view_photo = self.master.view_photo
                self.master.processed_image = self.new_edited_photo
                self.master.add_text_frame = TextFrame(master=self)
                self.master.add_text_frame.grab_set()

    def add_frame_button_pressed(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.add_frame_button:
            if(self.is_image_selected == False):
                boxError.showError(self)
            else:
                self.new_view_photo = self.master.view_photo
                self.master.processed_image = self.new_edited_photo
                self.master.add_border_frame = BorderFrame(master=self)
                self.master.add_border_frame.grab_set()

    def discard_button_pressed(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.discard_button:
            if(self.is_image_selected == False):
                boxError.showError(self)
            else:
                self.master.processed_image = self.master.original_image
                self.master.view_photo.show_image()
