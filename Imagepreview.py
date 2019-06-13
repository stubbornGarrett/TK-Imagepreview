'''
***************************************************************
A tkinter widget, for displaying, moveing and zooming an image.
***************************************************************
by stubbornGarrett (GitHub)
Tested with Python 3.7
June 2019
'''

from tkinter import Frame, Canvas
from PIL     import Image, ImageTk
import os

class Imagepreview(Frame):
    def __init__(self, parentWidget, image=None, zoomscale=1.2, minzoomlevel=0.1, maxzoomlevel=3, quality=0, backgroundcolor='#999999'):
        '''
        A tkinter Frame, which contains a canvas. The canvas adapts to the size of the frame.\n
        
        *****Init parameters*****
        parentWidget:    Widget which will contain this class (e.g. Tk root window or Frame).\n
        image:           The image, which will be displayed on the canvas (can be changed with '.update_image(*PIL.Image*)').\n
        backgroundcolor: Color of whitespace on canvas.\n
        zoomscale:       If the mouse is inside the canvas and the mousewheel gets triggered (Up/Down), the image is scaled by this factor.\n
        minzoom/maxzoom: Minimum and maximum value, for scaling the image.\n
        quality (0-4):    Different operations to resize image [NEAREST, BILINEAR, HAMMING, BICUBIC, LANCZOS]
        *************************

        *********Actions*********
        To move the image, have the mouse inside the canvas, hold down left mouse button and drag.
        For zooming, scroll the mouse wheel up or down.
        *************************
        '''

        Frame.__init__(self, master=parentWidget)
        self.previewImage   = image    # Original image
        self.resizedImage   = None     # Resized image - updates when *canvasScale* changes
        self.canvasImage    = None     # Displayed image
        self.canvasImage_ID = None     # Canvas ID of the displayed image

        self.imageLoaded = True if self.previewImage != None else False

        self.canvasScale    = 1.0
        self.scaleChanged   = True

        self.minlevel       = minzoomlevel
        self.maxlevel       = maxzoomlevel
        self.zoomscale      = zoomscale

        self.resizeFilter   = [Image.NEAREST, Image.BILINEAR, Image.HAMMING, Image.BICUBIC, Image.LANCZOS]
        self.resizeQuality  = quality

        # Create and place canvas
        self.previewCanvas = Canvas(self, highlightthickness=0, bg=backgroundcolor)
        self.previewCanvas.grid(column=0, row=0)

        self.create_binds()

        if self.imageLoaded:
            self.resizeWidth, self.resizeHeight = int(self.previewImage.width*(self.canvasScale)), int(self.previewImage.height*(self.canvasScale))
            self.resizeSize = self.resizeWidth, self.resizeHeight
            self.whiteSpaceX = int((self.previewCanvas.winfo_width() -self.resizeWidth) /2)+1
            self.whiteSpaceY = int((self.previewCanvas.winfo_height()-self.resizeHeight)/2)+1

        self.canvasZeroX = self.previewCanvas.xview()[0]
        self.canvasZeroY = self.previewCanvas.yview()[0]
        self.adjust_canvas_size(event=None)

    def create_binds(self):
        self.bind('<Configure>', self.adjust_canvas_size)
        self.previewCanvas.bind('<ButtonPress-1>',  self.scroll_start)
        self.previewCanvas.bind('<B1-Motion>',      self.scroll_move)
        if os.name == 'nt':
            self.previewCanvas.bind('<MouseWheel>', self.zoom)
        elif os.name == 'posix':
            self.previewCanvas.bind('<Button-4>', self.zoom)
            self.previewCanvas.bind('<Button-5>', self.zoom)

    def adjust_canvas_size(self, event=None):
        self.previewCanvas.config(width=self.winfo_width(), height=self.winfo_height())
        self.display_image(image=self.previewImage, quality=self.resizeQuality)

    def scroll_start(self, event):
        self.previewCanvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.previewCanvas.scan_dragto(event.x, event.y, gain=1)
        if self.check_border_contact():
            self.display_image(image=self.previewImage, quality=self.resizeQuality)

    def zoom(self, event):
        if os.name == 'nt':
            if event.delta >= 0 and self.canvasScale*self.zoomscale < self.maxlevel:
                self.canvasScale *= self.zoomscale
                self.scaleChanged = True
            elif event.delta >= 0 and self.canvasScale < self.maxlevel:
                self.canvasScale  = self.maxlevel
                self.scaleChanged = True
            if event.delta <  0 and self.canvasScale/self.zoomscale > self.minlevel:
                self.canvasScale *= 1/self.zoomscale
                self.scaleChanged = True
            elif event.delta < 0 and self.canvasScale > self.minlevel:
                self.canvasScale  = self.minlevel
                self.scaleChanged = True
        elif os.name == 'posix':
            if event.num   == 4 and self.canvasScale*self.zoomscale < self.maxlevel:
                self.canvasScale *= self.zoomscale
                self.scaleChanged = True
            elif event.num == 4 and self.canvasScale < self.maxlevel:
                self.canvasScale  = self.maxlevel
                self.scaleChanged = True
            if event.num   ==  5 and self.canvasScale/self.zoomscale > self.minlevel:
                self.canvasScale *= 1/self.zoomscale
                self.scaleChanged = True
            elif event.num == 5 and self.canvasScale > self.minlevel:
                self.canvasScale  = self.minlevel
                self.scaleChanged = True

        if self.previewCanvas.canvasx(self.previewCanvas.winfo_width()) < self.previewCanvas.winfo_width():
           self.previewCanvas.xview('scroll', +1, 'units')
           print('1')
        if self.previewCanvas.canvasx(0) > 0:
           self.previewCanvas.xview('scroll', -1, 'units')
           print('2')
        if self.previewCanvas.canvasy(self.previewCanvas.winfo_height()) < self.previewCanvas.winfo_height():
           self.previewCanvas.yview('scroll', +1, 'units')
           print('3')
        if self.previewCanvas.canvasy(0) > 0:
           self.previewCanvas.yview('scroll', -1, 'units')
           print('4')

        # if self.previewCanvas.canvasx(self.previewCanvas.winfo_width()) < self.previewCanvas.winfo_width():
        #     self.previewCanvas.xview('moveto', +0.1)
        #     print('1')
        # if self.previewCanvas.canvasx(0) > 0:
        #     self.previewCanvas.xview('moveto', -0.1)
        #     print('2')
        # if self.previewCanvas.canvasy(self.previewCanvas.winfo_height()) < self.previewCanvas.winfo_height():
        #     self.previewCanvas.yview('moveto', +0.1)
        #     print('3')
        # if self.previewCanvas.canvasy(0) > 0:
        #     self.previewCanvas.yview('moveto', -0.1)
        #     print('4')

        self.display_image(event.x, event.y, self.previewImage, self.resizeQuality)

    def update_image(self, image=None):
        self.previewImage = image
        self.resizedImage = image
        self.imageLoaded = False if self.previewImage == None else True
        if self.imageLoaded:
            self.resizeWidth, self.resizeHeight = int(self.previewImage.width*(self.canvasScale)), int(self.previewImage.height*(self.canvasScale))
            self.resizeSize = self.resizeWidth, self.resizeHeight
            self.whiteSpaceX = int((self.previewCanvas.winfo_width() -self.resizeWidth) /2)+1
            self.whiteSpaceY = int((self.previewCanvas.winfo_height()-self.resizeHeight)/2)+1

            self.reset_preview()
            self.display_image(image=self.previewImage, quality=self.resizeQuality)
        else:
            self.previewCanvas.delete(self.canvasImage_ID)
            self.canvasImage_ID = None

    def display_image(self, x=0, y=0, image=None, quality=0):
        if self.imageLoaded:
            if self.canvasImage_ID:
                self.previewCanvas.delete(self.canvasImage_ID)

            self.resizeWidth, self.resizeHeight = int(self.previewImage.width*self.canvasScale), int(self.previewImage.height*self.canvasScale)
            self.resizeSize  = self.resizeWidth, self.resizeHeight
            self.whiteSpaceX = int((self.previewCanvas.winfo_width() -self.resizeWidth) /2)+1
            self.whiteSpaceY = int((self.previewCanvas.winfo_height()-self.resizeHeight)/2)+1
            if self.scaleChanged:
                self.resizedImage = image.resize(self.resizeSize, resample=self.resizeFilter[quality])
                self.scaleChanged = False

            leftEdge   = self.previewCanvas.canvasx(0)-self.whiteSpaceX  if self.previewCanvas.canvasx(0) > self.whiteSpaceX  else 0
            rightEdge  = self.resizeWidth +(self.whiteSpaceX+self.previewCanvas.canvasx(0)) if self.resizeWidth +self.whiteSpaceX-(self.previewCanvas.canvasx(0)) > self.previewCanvas.winfo_width()  else self.resizedImage.width
            topEdge    = self.previewCanvas.canvasy(0)-self.whiteSpaceY  if self.previewCanvas.canvasy(0) > self.whiteSpaceY  else 0
            bottomEdge = self.resizeHeight+(self.whiteSpaceY+self.previewCanvas.canvasy(0)) if self.resizeHeight+self.whiteSpaceY-(self.previewCanvas.canvasy(0)) > self.previewCanvas.winfo_height() else self.resizedImage.height

            xPos = self.previewCanvas.winfo_width() / 2 + (leftEdge + rightEdge  - self.resizeWidth)  /2
            yPos = self.previewCanvas.winfo_height()/ 2 + (topEdge  + bottomEdge - self.resizeHeight) /2
            if rightEdge - leftEdge > 0 and bottomEdge - topEdge > 0:
                cropedImage         = self.resizedImage.crop((leftEdge, topEdge, rightEdge, bottomEdge))
                self.canvasImage    = ImageTk.PhotoImage(cropedImage)
                self.canvasImage_ID = self.previewCanvas.create_image(xPos, yPos, image=self.canvasImage)

    def check_border_contact(self):
        if self.previewCanvas.canvasx(0)+15 > self.whiteSpaceX \
        or self.resizeWidth +self.whiteSpaceX-(self.previewCanvas.canvasx(0)-15) > self.previewCanvas.winfo_width() \
        or self.previewCanvas.canvasy(0)+15 > self.whiteSpaceY \
        or self.resizeHeight+self.whiteSpaceY-(self.previewCanvas.canvasy(0)-15) > self.previewCanvas.winfo_height():
            return True
        else:
            return False

    def original_zoom(self, event=None):
        self.canvasScale  = 1.0
        self.scaleChanged = True
        self.display_image(image=self.previewImage, quality=self.resizeQuality)

    def reset_preview(self, event=None):
        if self.imageLoaded:
            if self.previewImage.height/self.previewCanvas.winfo_height() > self.previewImage.width/self.previewCanvas.winfo_width():
                self.canvasScale  = self.previewCanvas.winfo_height() / self.previewImage.height
                self.scaleChanged = True
            else:
                self.canvasScale  = self.previewCanvas.winfo_width()  / self.previewImage.width
                self.scaleChanged = True
            self.previewCanvas.xview_moveto(self.canvasZeroX)
            self.previewCanvas.yview_moveto(self.canvasZeroY)
            self.adjust_canvas_size()
