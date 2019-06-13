from tkinter import Frame, Tk, Label, Button
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Separator
from PIL     import Image, ImageTk
import Imagepreview
import time
import os

def main():
    root = Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.geometry('900x600+50+50')
    root.title('Imagepreview Test')

    window = Frame(root)
    window.grid(column=0, row=0, sticky='news')
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=0)
    window.rowconfigure(1, weight=1)

    topWidget   = Label(window, text = 'Image Preview', font=('Arial', '32'))
    topWidget.grid(column=0, row=0, sticky='we')
    topWidget.columnconfigure(0, weight=1)
    topWidget.rowconfigure(0, weight=1)

    '''************ImagePreview************'''
    previewFrame = Frame(window)
    previewFrame.grid(column=0, row=1, sticky='news')
    previewFrame.columnconfigure(0, weight=1)
    previewFrame.rowconfigure(0, weight=1)

    try:
        testImage = Image.open('test.jpg')
    except:
        testImage = Image.new('RGB', (100,100), color='#999999')
    preview   = Imagepreview.Imagepreview(previewFrame, testImage, zoomscale=1.2, minzoomlevel=0.1, maxzoomlevel=20.0, quality=0, backgroundcolor='#999999')
    preview.grid(column=0, row=0, sticky='news')
    '''************************************'''

    buttonColor = 'gray80'

    controlFrame = Frame(window)
    controlFrame.grid(column=1, row=0, rowspan=3, padx=3)
    previewFrame.rowconfigure(2, weight=0)

    def update_label(event=None):
        infoLabel.config(anchor='w', text='Scale:\t\tx{}\n\nWidth:\t\t{}\nHeight:\t\t{}\n\nScale width:\t{}\nScale height:\t{}'.format(round(preview.canvasScale,2), testImage.width, testImage.height, preview.resizedImage.width, preview.resizedImage.height))
    def reset_button(event=None):
        preview.reset_preview()
        update_label()
    def original_button(event=None):
        preview.original_zoom()
        update_label()

    resetButton    = Button(controlFrame, text='Reset Preview (Ctrl+R)', command=reset_button, bg=buttonColor)
    resetButton.grid(column=0, row=0, sticky='we')
    originalButton = Button(controlFrame, text='x1.0 zoom (Num 1)', command=original_button, bg=buttonColor)
    originalButton.grid(column=0, row=1, sticky='we')

    seperatorOne  = Separator(controlFrame)
    seperatorOne.grid(column=0, row=2, sticky='we', pady=10)

    infoLabel      = Label(controlFrame, anchor='w')
    infoLabel.grid(column=0, row=3, sticky='s')
    infoLabel.config(text='Scale:\t\tx{}\n\nWidth:\t\t{}\nHeight:\t\t{}\n\nScale width:\t{}\nScale height:\t{}'.format(round(preview.canvasScale,2), testImage.width, testImage.height, preview.resizedImage.width, preview.resizedImage.height))

    if os.name == 'nt':
        root.bind('<MouseWheel>', update_label)
    elif os.name == 'posix':
        root.bind('<Button-4>', update_label)
        root.bind('<Button-5>', update_label)
    # root.bind('<MouseWheel>', update_label)
    root.bind('1',            original_button)
    root.bind('<Control-r>',  reset_button)

    def update_quality(x):
        for child in qualityFrame.winfo_children():
            try:
                child.configure(bg='white', fg='black')
            except:
                pass
        if x == 0:
            qualityZero.configure(bg='gray10', fg='white')
        elif x == 1:
            qualityOne.configure(bg='gray10', fg='white')
        elif x == 2:
            qualityTwo.configure(bg='gray10', fg='white')
        elif x == 3:
            qualityThree.configure(bg='gray10', fg='white')
        elif x == 4:
            qualityFour.configure(bg='gray10', fg='white')
        preview.resizeQuality = x
        preview.scaleChanged = True
        preview.display_image(image=preview.previewImage, quality=x)

    seperatorTwo  = Separator(controlFrame)
    seperatorTwo.grid(column=0, row=4, sticky='we', pady=10)

    qualityFrame  = Frame(controlFrame)
    qualityFrame.grid(column=0, row=5, sticky='we', padx=30)
    qualityFrame.columnconfigure(0, weight=1)

    qualityLabel  = Label(qualityFrame, text='Resize Filter', font=('Arial', '10', 'bold'))
    qualityLabel.grid(column=0, row=0, sticky='we', pady=5)
    qualityZero   = Button(qualityFrame, text='0 (NEAREST)', anchor='w', command=lambda: update_quality(0))
    qualityZero.grid(column=0, row=1, sticky='we')
    qualityOne    = Button(qualityFrame, text='1 (BILINEAR)', anchor='w', command=lambda: update_quality(1))
    qualityOne.grid(column=0, row=2, sticky='we')
    qualityTwo    = Button(qualityFrame, text='2 (HAMMING)', anchor='w', command=lambda: update_quality(2))
    qualityTwo.grid(column=0, row=3, sticky='we')
    qualityThree  = Button(qualityFrame, text='3 (BICUBIC)', anchor='w', command=lambda: update_quality(3))
    qualityThree.grid(column=0, row=4, sticky='we')
    qualityFour   = Button(qualityFrame, text='4 (LANCZOS)', anchor='w', command=lambda: update_quality(4))
    qualityFour.grid(column=0, row=5, sticky='we')
    update_quality(0)

    seperatorThree  = Separator(controlFrame)
    seperatorThree.grid(column=0, row=6, sticky='we', pady=10)

    def load_image():
        try:
            filetypes           = [ ('JPEG','*.jpg *.jpeg'),
                                    ('PNG','*.png'),
                                    ("all files","*.*")]
            testImage = Image.open(askopenfilename(title='Load Image...', defaultextension='.', filetypes=filetypes))
            preview.update_image(image=testImage)
        except AttributeError:
            pass

    loadButton = Button(controlFrame, text='Load Image', font=('Arial', '18'),command=load_image, bg=buttonColor)
    loadButton.grid(column=0, row=7, sticky='we')

    window.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    preview.reset_preview()
    window.mainloop()


if __name__ == '__main__':
    main()