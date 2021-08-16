from tkinter.ttk import Frame
from ttkthemes import ThemedTk
from windowApp import BuildApp


def main():

    root = ThemedTk(theme='black')
    #print(root.get_themes())
    app = BuildApp()
    root.mainloop()


if __name__ == '__main__':
    main()
