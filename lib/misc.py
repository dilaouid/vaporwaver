from data import globals, gui
from PIL import Image, ImageTk
import tkinter as tk

def changeMisc(file):
    misc = tk.PhotoImage(file='picts/miscs/' + file + '.png')
    gui["frame"]["canvas"].misc = misc
    gui["frame"]["canvas"].itemconfig(globals["misc_container"], image=misc)

def moveMisc(axis, value):
    if globals["misc"] is None:
        return
    globals["val"][axis] = value
    # change the position of the character according to % of the canvas
    gui["frame"]["canvas"].coords(globals["misc"], gui["frame"]["canvas"].winfo_width() * int(globals["val"]["miscPosX"]) / 100, gui["frame"]["canvas"].winfo_height() * int(globals["val"]["miscPosY"]) / 100)

def scaleMisc(axis, value):
    if globals["misc"] is None:
        return
    globals["val"]["miscScale"] = value
    image = Image.open(globals["miscPath"])
    image = image.resize((int(image.size[0] * int(globals["val"]["miscScale"]) / 100), int(image.size[1] * int(globals["val"]["miscScale"]) / 100)), Image.ANTIALIAS)
    gui["frame"]["canvas"].itemconfig(globals["misc"], image=ImageTk.PhotoImage(image))