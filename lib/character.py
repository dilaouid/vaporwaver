import os
from data import globals, gui, path_finder
from PIL import Image, ImageTk, ImageFilter
from glitch_this import ImageGlitcher
import cv2
import numpy as np

rotateCharacterBool = False

def resizeCharacter(image):
    return image.resize((int(image.size[0] * int(globals["render"]["val"]["characterScale"]) / 100), int(image.size[1] * int(globals["render"]["val"]["characterScale"]) / 100)), Image.LANCZOS)

def min_rotateCharacter(image):
    return image.rotate(globals["render"]["val"]["characterRotation"], expand=True)

def glitchingCLI(image) -> Image:
    glitcher = ImageGlitcher()
    glitched_image = glitcher.glitch_image(image, color_offset=True, glitch_amount=float(globals["render"]["val"]["characterGlitch"]), seed=int(globals["render"]["val"]["characterGlitchSeed"]))
    glitched_image.save(path_finder('./tmp/char-cli.png'))
    return Image.open(path_finder('./tmp/char-cli.png'))

def glitching(image) -> Image:
    glitcher = ImageGlitcher()
    glitched_image = glitcher.glitch_image(image, color_offset=True, glitch_amount=float(globals["render"]["val"]["characterGlitch"]), seed=int(globals["render"]["val"]["characterGlitchSeed"]))
    glitched_image.save('./tmp/char.png')
    return ImageTk.PhotoImage(glitched_image)

def applygradient(path: str = './tmp/char.png'):
    image = cv2.imread(globals["render"]["characterPath"], cv2.IMREAD_UNCHANGED)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.applyColorMap(image, getattr(cv2, "COLORMAP_" + globals["render"]["val"]["characterGradient"].upper()))
    image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
    image[:, :, 3] = cv2.imread(globals["render"]["characterPath"], cv2.IMREAD_UNCHANGED)[:, :, 3]
    image = Image.fromarray(image)
    image = resizeCharacter(image)
    image = min_rotateCharacter(image)
    image.save(path)
    return Image.open(path)

def gradientCharacter(gradient: str):
    globals["render"]["val"]["characterGradient"] = gradient
    if globals["render"]["val"]["characterGradient"] == "none":
        image: Image = Image.open(globals["render"]["characterPath"])
        image = resizeCharacter(image)
        if rotateCharacterBool:
            image = min_rotateCharacter(image)
        image.save('./tmp/char.png')
        globals["gcChar"] = ImageTk.PhotoImage(image)
        if globals["render"]["val"]["characterGlitch"] != .1:
            globals["gcChar"] = glitching(Image.open('./tmp/char.png'))
        gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])
        return image
    globals["gcChar"] = None
    gui["frame"]["canvas"].character = None
    image = applygradient()
    globals["gcChar"] = ImageTk.PhotoImage(image)
    gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])

    # if there is glitch appluy glitching effect
    if globals["render"]["val"]["characterGlitch"] != .1:
        globals["gcChar"] = glitching(Image.open('./tmp/char.png'))
        gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])
    return image

def resizeAndUpdate() -> Image:
    image: Image = Image.open(globals["render"]["characterPath"])
    if globals["render"]["val"]["characterGradient"] != "none":
        image = gradientCharacter(globals["render"]["val"]["characterGradient"])
    image = resizeCharacter(image)
    if rotateCharacterBool:
        image = min_rotateCharacter(image)
    if not os.path.exists('./tmp'):
        os.makedirs('./tmp')
    image.save('./tmp/char.png')
    return Image.open('./tmp/char.png')

def moveCharacter(axis, value) -> None:
    if globals["character"] is None:
        return
    globals["render"]["val"][axis] = value
    # change the position of the character according to % of the canvas
    gui["frame"]["canvas"].coords(globals["character"], gui["frame"]["canvas"].winfo_width() * int(globals["render"]["val"]["characterXpos"]) / 100, gui["frame"]["canvas"].winfo_height() * int(globals["render"]["val"]["characterYpos"]) / 100)

def scaleCharacter(axis, value) -> None:
    if globals["character"] is None:
        return
    globals["render"]["val"]["characterScale"] = value
    image: Image = resizeAndUpdate()
    globals["gcChar"]: Image = glitching(image)
    gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])

def glitchCharacter(axis, value) -> None:
    if globals["character"] is None:
        return
    globals["render"]["val"][axis] = value
    image = resizeAndUpdate()
    globals["gcChar"] = glitching(image)
    gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])

# rotate the character by a given angle (in degrees) keeping the transparency
def rotateCharacter(axis: str, value: int) -> None:
    global rotateCharacterBool
    rotateCharacterBool = True
    if globals["character"] is None:
        return
    globals["render"]["val"][axis] = int(value)
    image: Image = resizeAndUpdate()
    # image = image.rotate(int(globals["render"]["val"]["characterRotation"]), expand=True)
    image.save('./tmp/char.png')
    globals["gcChar"] = ImageTk.PhotoImage(image)
    gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])
    rotateCharacterBool = False

def glowCharacter(color: str) -> None:
    # apply a contour around transparent pixels of the character with keep alpha
    if globals["character"] is None:
        return
    image = resizeAndUpdate()
    image = image.filter(ImageFilter.CONTOUR)
    globals["gcChar"] = glitching(image)
    gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])