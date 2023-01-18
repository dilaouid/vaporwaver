import sys
import os
import tkinter.messagebox
from PIL import Image

def define(file: str, folderName: str) -> str:
    if not os.path.exists("picts/" + folderName + "/" + file + ".png"):
        tkinter.messagebox.showerror("Error", "The " + folderName + " file '" + file + "' does not exist.")
        sys.exit()
    return "picts/" + folderName + "/" + file + ".png"

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
    "gcChar": None,
    "gcMisc": None,
    "render": {
        "background": define("default", "backgrounds"),
        "misc": define("none", "miscs"),
        "characterPath": None,
        "val": {
            "characterXpos": 0,
            "characterYpos": 0,
            "characterScale": 100,
            "characterRotation": 0,
            "characterGlitch": .1,
            "characterGlitchSeed": 1,
            "characterGradient": "none",
            "characterGlow": "none",
            "miscPosX": 0,
            "miscPosY": 0,
            "miscScale": 100,
            "miscRotate": 0,
            "crt": False
        },
    },
    "backgrounds": get_all_backgrounds(),
    "background_container": None,
    "misc_container": None,
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
        "hot",
        "parula",
        "magma",
        "inferno",
        "plasma",
        "viridis",
        "cividis"
    ],
    "glow": [
        "none",
        "red",
        "green",
        "blue",
        "yellow"
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
            "rotate": None,
            "glitch": None,
            "glitchSeed": None,
            "gradients": None,
            "glow": None
        },
        "misc": {
            "posX": None,
            "posY": None,
            "scale": 100,
            "rotate": None,
            "select": None
        },
        "crt": {
            "checkbox": None
        }
    }
}