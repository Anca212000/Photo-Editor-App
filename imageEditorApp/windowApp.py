from tkinter import Tk, BOTH, RIGHT, LEFT, TOP, BOTTOM, SE
from tkinter.ttk import Frame, Button, Style, Label
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from navBar import NavigationBar
from photoViewer import PhotoViewer


class BuildApp(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.master.title("Photo Editor App")
        self.pack(fill=BOTH, expand=1)

        self.centerWindow()

        self.original_image = None
        self.processed_image = None
        self.filter_frame = None
        self.adjust_frame = None
        self.image_overlay_frame = None
        self.collage_frame = None
        self.add_text_frame = None
        self.add_border_frame = None

        style = Style()
        style.configure("title.TLabel", font=("Century Gothic", 36, "bold"), foreground="cyan", anchor='center')

        image = Image.open("images/camera.png")
        image = image.resize((100,100), Image.ANTIALIAS)

        imgLogo = ImageTk.PhotoImage(image)

        self.logo_label = Label(image=imgLogo)
        self.logo_label.image = imgLogo

        self.logo_label.place(x=15, y=5)

        self.logo_label = Label(text="Photo  Editor  App", style="title.TLabel")
        self.logo_label.place(relx=0.18,rely=0.06)

        self.nav_buttons = NavigationBar(master=self)
        self.nav_buttons.pack(padx=0,pady=5,side=RIGHT,anchor=SE)

        self.view_photo = PhotoViewer(master=self)
        self.view_photo.pack(side=BOTTOM,padx=1,pady=2)

    def centerWindow(self):
        width_app = 800
        height_app = 680

        screen_w = self.master.winfo_screenwidth()
        screen_h = self.master.winfo_screenheight()

        x = (screen_w - width_app)/2
        y = (screen_h - height_app)/2

        self.master.geometry('%dx%d+%d+%d' % (width_app, height_app, x, y))
