import sys
import os
import tkinter.messagebox
from PIL import Image

def path_finder(relative_path: str) -> str:
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

def define(file: str, folderName: str) -> str:
    path = path_finder("picts/" + folderName + "/" + file + ".png")
    if not os.path.exists(path):
        tkinter.messagebox.showerror("Error", "The " + folderName + " file '" + file + "' does not exist.")
        sys.exit()
    return path

def get_all_miscs() -> list:
    miscs = []
    path = path_finder("picts/miscs/")
    for file in os.listdir(path):
        if file.endswith(".png"):
            miscs.append(file[:-4])
    return miscs

def get_all_backgrounds() -> list:
    backgrounds = []
    path = path_finder("picts/backgrounds/")
    for file in os.listdir(path):
        if file.endswith(".png") and Image.open(path + file).size == (460, 595):
            backgrounds.append(file[:-4])
        else:
            print(f"Background '{file}' is not 460x595, skipping.")
    return backgrounds

globals = {
    "character": None,
    "gcChar": None,
    "gcMisc": None,
    "misc_above_character": False,
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
        "output": ""
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
        "cividis",
        "deepgreen"
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
            "gradients": None
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

def cleanup_temp_files():
    """Nettoie tous les fichiers temporaires du dossier tmp"""
    tmp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp')
    if os.path.exists(tmp_dir):
        for file in os.listdir(tmp_dir):
            try:
                file_path = os.path.join(tmp_dir, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Warning: Could not remove temporary file {file_path}: {e}")

def get_temp_file(name: str) -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp', f"{name}_{globals.get('temp_suffix', 'default')}.png")