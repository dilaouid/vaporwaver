from data import globals, gui, path_finder
from PIL import Image, ImageTk
import tkinter as tk

def changeMisc(filename: str) -> None:
    globals["render"]["misc"] = path_finder('picts/miscs/' + filename + '.png')
    misc: Image = tk.PhotoImage(file=globals["render"]["misc"])
    gui["frame"]["canvas"].misc = misc
    
    # Get canvas dimensions for centering
    canvas_width = gui["frame"]["canvas"].winfo_width()
    canvas_height = gui["frame"]["canvas"].winfo_height()
    
    # Set position to center (50%)
    globals["render"]["val"]["miscScale"] = 100
    globals["render"]["val"]["miscPosX"] = 50
    globals["render"]["val"]["miscPosY"] = 50
    
    # Center the misc image on the canvas
    x = canvas_width * 0.5  # 50%
    y = canvas_height * 0.5  # 50%
    gui["frame"]["canvas"].coords(globals["misc_container"], x, y)
    
    # Update the image and ensure it's centered
    gui["frame"]["canvas"].itemconfig(globals["misc_container"], image=misc, anchor="center")
    
    # Update sliders
    for element in gui["el"]["misc"]:
        if element == "scale":
            gui["el"]["misc"][element].set(100)
        elif element == "miscPosX" or element == "miscPosY":
            gui["el"]["misc"][element].set(50)  # Center position (50%)
        elif element != "select":
            gui["el"]["misc"][element].set(0)

def moveMisc(axis, value) -> None:
    if globals["misc_container"] is None:
        return
    globals["render"]["val"][axis] = value
    canvas_width = gui["frame"]["canvas"].winfo_width()
    canvas_height = gui["frame"]["canvas"].winfo_height()
    x = canvas_width * int(globals["render"]["val"]["miscPosX"]) / 100
    y = canvas_height * int(globals["render"]["val"]["miscPosY"]) / 100
    gui["frame"]["canvas"].coords(globals["misc_container"], x, y)
    gui["frame"]["canvas"].itemconfig(globals["misc_container"], anchor="center")

def scaleMisc(axis, value) -> None:
    if globals["misc_container"] is None:
        return
    globals["render"]["val"]["miscScale"] = value
    image = Image.open(globals["render"]["misc"])
    image = image.resize((int(image.size[0] * int(globals["render"]["val"]["miscScale"]) / 100), int(image.size[1] * int(globals["render"]["val"]["miscScale"]) / 100)), Image.Resampling.LANCZOS)
    image = image.rotate(int(globals["render"]["val"]["miscRotate"]), expand=True)
    globals["gcMisc"] = ImageTk.PhotoImage(image)
    gui["frame"]["canvas"].itemconfig(globals["misc_container"], image=globals["gcMisc"], anchor="center")

def rotateMisc(axis, value) -> None:
    if globals["misc_container"] is None:
        return
    globals["render"]["val"]["miscRotate"] = value
    image = Image.open(globals["render"]["misc"])
    image = image.resize((int(image.size[0] * int(globals["render"]["val"]["miscScale"]) / 100), int(image.size[1] * int(globals["render"]["val"]["miscScale"]) / 100)), Image.Resampling.LANCZOS)
    image = image.rotate(int(globals["render"]["val"]["miscRotate"]), expand=True)
    globals["gcMisc"] = ImageTk.PhotoImage(image)
    gui["frame"]["canvas"].itemconfig(globals["misc_container"], image=globals["gcMisc"])