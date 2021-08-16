from tkinter import Frame, Canvas, CENTER, ROUND, PhotoImage, NW
from PIL import Image,ImageTk
import cv2


class PhotoViewer(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master=master, width=600, height=560, bg='#252525')

        self.shown_image = None
        self.ratio = 0

        self.canvas = Canvas(self, width=600, height=560, bg='#252525')#bg='#090033')
        self.canvas.place(relx=0.5,rely=0.5,anchor=CENTER)

    def show_image(self, img=None):
        if img is None:
            image = self.master.processed_image.copy()
        else:
            image = img

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channels = image.shape
        ratio = height / width

        new_width = width
        new_height = height

        if height > self.winfo_height() or width > self.winfo_width():
            if ratio < 1:
                new_width = self.winfo_width()
                new_height = int(new_width * ratio)
            else:
                new_height = self.winfo_height()
                new_width = int(new_height * (width / height))

        self.shown_image = cv2.resize(image, (new_width, new_height), Image.ANTIALIAS)
        self.shown_image = ImageTk.PhotoImage(Image.fromarray(self.shown_image))

        self.ratio = height / new_height

        self.canvas.delete()
        self.canvas.config(width=new_width, height=new_height)
        self.canvas.create_image(new_width / 2, new_height / 2, anchor=CENTER, image=self.shown_image)
        self.canvas.update()
