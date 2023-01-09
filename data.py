import sys
import os
import tkinter.messagebox
from PIL import Image

def defineBackground(background) -> str:
    if not os.path.exists("picts/backgrounds/" + background + ".png"):
        tkinter.messagebox.showerror("Error", "The background file '"+background+"' does not exist.")
        sys.exit()
    return "picts/backgrounds/" + background + ".png"

def defineMisc(background) -> str:
    if not os.path.exists("picts/miscs/" + background + ".png"):
        tkinter.messagebox.showerror("Error", "The misc file '"+background+"' does not exist.")
        sys.exit()
    return "picts/miscs/" + background + ".png"

def get_all_miscs() -> list:
    miscs = []
    for file in os.listdir("picts/miscs"):
        if file.endswith(".png"):
            miscs.append(file[:-4])
    return miscs

def get_all_backgrounds() -> list:
    backgrounds = []
    for file in os.listdir("picts/backgrounds"):
        if file.endswith(".png") and Image.open("picts/backgrounds/" + file).size == (460, 595):
            backgrounds.append(file[:-4])
    return backgrounds

globals = {
    "character": None,
    "characterPath": None,
    "gcChar": None,
    "gcMisc": None,
    "val": {
        "characterXpos": 0,
        "characterYpos": 0,
        "characterScale": 100,
        "characterGlitch": .1,
        "characterGlitchSeed": 1,
        "characterGradient": "none",
        "miscPosX": 0,
        "miscPosY": 0,
        "miscScale": 100,
        "crt": False
    },
    "background": defineBackground("default"),
    "backgrounds": get_all_backgrounds(),
    "background_container": None,
    "misc_container": None,
    "misc": defineMisc("none"),
    "miscs": get_all_miscs(),
    "misc_container": None,
    "crt_container": None,
    "gradients": [
        "none",
        "autumn",
        "bone",
        "jet",
        "winter",
        "rainbow",
        "ocean",
        "summer",
        "spring",
        "cool",
        "hsv",
        "pink",
        "hot"
    ],
    "CRT": None,
}

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
            "scale": 100,
            "glitch": None,
            "glitchSeed": None,
            "gradients": None,
        },
        "misc": {
            "posX": None,
            "posY": None,
            "scale": 100,
            "select": None
        },
        "crt": {
            "checkbox": None
        }
    }
}