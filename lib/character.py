import tkinter as tk
import sys, os
from data import globals, gui
from PIL import Image, ImageTk
from glitch_this import ImageGlitcher

def resizeAndUpdate():
    image = Image.open(globals["characterPath"])
    image = image.resize((int(image.size[0] * int(globals["val"]["characterScale"]) / 100), int(image.size[1] * int(globals["val"]["characterScale"]) / 100)), Image.LANCZOS)
    image.save('./tmp/char.png')
    return Image.open('./tmp/char.png')

def moveCharacter(axis, value):
    if globals["character"] is None:
        return
    globals["val"][axis] = value
    # change the position of the character according to % of the canvas
    gui["frame"]["canvas"].coords(globals["character"], gui["frame"]["canvas"].winfo_width() * int(globals["val"]["characterXpos"]) / 100, gui["frame"]["canvas"].winfo_height() * int(globals["val"]["characterYpos"]) / 100)

def scaleCharacter(axis, value):
    if globals["character"] is None:
        return
    globals["val"]["characterScale"] = value
    image = resizeAndUpdate()

    glitcher = ImageGlitcher()
    glitched_image = glitcher.glitch_image(image, color_offset=True, glitch_amount=float(globals["val"]["characterGlitch"]), seed=int(globals["val"]["characterGlitchSeed"]))
    globals["gcChar"] = ImageTk.PhotoImage(glitched_image)
    gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])

def glitchCharacter(axis, value):
    if globals["character"] is None:
        return
    globals["val"][axis] = value
    image = resizeAndUpdate()

    glitcher = ImageGlitcher()
    glitched_image = glitcher.glitch_image(image, color_offset=True, glitch_amount=float(globals["val"]["characterGlitch"]), seed=int(globals["val"]["characterGlitchSeed"]))
    globals["gcChar"] = ImageTk.PhotoImage(glitched_image)
    gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])