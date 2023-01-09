from data import globals, gui
import tkinter as tk

def crt(enable: bool)-> None:
    globals["val"]["crt"] = enable
    if enable == True:
        image = tk.PhotoImage(file='./picts/crt/crt.png')
        globals["CRT"] = gui["frame"]["canvas"].create_image((0, 0), image=image, anchor=tk.NW)
        gui["frame"]["canvas"].crt = image
        gui["frame"]["canvas"].itemconfig(globals["CRT"], image=image)
    else:
        # remove the CRT image from the preview canvas
        gui["frame"]["canvas"].delete(globals["CRT"])