def setScreenPosition(self,width,height,precision):
    width_app = width
    height_app = height
    value_prec = precision

    screen_w = self.winfo_screenwidth()
    screen_h = self.winfo_screenheight()

    x = (screen_w - width_app)/2
    x = x / value_prec
    y = (screen_h - height_app)/2

    self.geometry('%dx%d+%d+%d' % (width_app, height_app, x, y))
