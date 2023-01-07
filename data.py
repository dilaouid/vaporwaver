import sys
import os
import tkinter.messagebox

def defineBackground(background):
    if not os.path.exists("picts/backgrounds/" + background + ".png"):
        tkinter.messagebox.showerror("Error", "The background file '"+background+"' does not exist.")
        sys.exit()
    return "picts/backgrounds/" + background + ".png"


global globals
globals = {
    "character": None,
    "val": {
        "characterXpos": 0,
        "characterYpos": 0,
        "characterWidth": 0,
        "characterHeight": 0,
        "characterGlitch": 0,
        "characterGradient": 0,
        "miscPosX": 0,
        "miscPosY": 0,
        "miscWidth": 0,
        "miscHeight": 0,
    },
    "background": defineBackground("default"),
    "miscItem": None,
    "CRT": False,
    "Animate": False,
}

global gui
gui = {
    "frame": {
            "left": None,
            "right": None,
            "window": None,
    },
    "el": {
        "warning_label": None,
        "save_button": None,
        "char": {
            "posX": None,
            "posY": None,
            "width": None,
            "height": None,
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