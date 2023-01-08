import sys
import os
import tkinter.messagebox
from PIL import Image

def defineBackground(background):
    if not os.path.exists("picts/backgrounds/" + background + ".png"):
        tkinter.messagebox.showerror("Error", "The background file '"+background+"' does not exist.")
        sys.exit()
    return "picts/backgrounds/" + background + ".png"


def get_all_backgrounds():
    backgrounds = []
    for file in os.listdir("picts/backgrounds"):
        # if the file is a png file, and the image have a size of 1280x720 pixels (the size of the window) add it to the list
        print(Image.open("picts/backgrounds/" + file).size)
        if file.endswith(".png") and Image.open("picts/backgrounds/" + file).size == (460, 595):
            backgrounds.append(file[:-4])
    return backgrounds

global globals
globals = {
    "character": None,
    "characterPath": None,
    "previewChar": None,
    "val": {
        "characterXpos": 0,
        "characterYpos": 0,
        "characterScale": 1,
        "characterGlitch": 0,
        "characterGradient": 0,
        "miscPosX": 0,
        "miscPosY": 0,
        "miscWidth": 0,
        "miscHeight": 0,
    },
    "background": defineBackground("default"),
    "backgrounds": get_all_backgrounds(),
    "background_container": None,
    "miscItem": None,
    "CRT": False,
    "Animate": False,
}

global gui
gui = {
    "frame": {
            "left": None,
            "right": None,
            "preview": None,
            "canvas": None,
            "window": None,
    },
    "el": {
        "warning_label": None,
        "save_button": None,
        "char": {
            "posX": None,
            "posY": None,
            "scale": 1,
            "glitch": None,
        },
        "misc": {
            "posX": None,
            "posY": None,
            "width": None,
            "height": None,
        }
    }
}