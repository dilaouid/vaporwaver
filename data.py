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
    "window": None,
    "character": None,
    "characterXpos": 0,
    "characterYpos": 0,
    "characterWidth": 0,
    "characterHeight": 0,
    "characterGlitch": 0,
    "characterGradient": 0,
    "background": defineBackground("default"),
    "miscItem": None,
    "miscPosX": 0,
    "miscPosY": 0,
    "miscWidth": 0,
    "miscHeight": 0,
    "CRT": False,
    "Animate": False,
}