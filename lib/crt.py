from data import globals, gui, path_finder
import tkinter as tk

def crt(enable: bool)-> None:
    globals["render"]["val"]["crt"] = enable
    if enable == True:
        path = path_finder('picts/crt/crt.png')
        image = tk.PhotoImage(file=path)
        globals["CRT"] = gui["frame"]["canvas"].create_image((0, 0), image=image, anchor=tk.NW)
        gui["frame"]["canvas"].crt = image
        gui["frame"]["canvas"].itemconfig(globals["CRT"], image=image)
    else:
        # remove the CRT image from the preview canvas
        gui["frame"]["canvas"].delete(globals["CRT"])