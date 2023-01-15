import os
from data import globals, gui
from PIL import Image, ImageTk
from glitch_this import ImageGlitcher
import cv2

def glitching(image) -> Image:
    glitcher = ImageGlitcher()
    glitched_image = glitcher.glitch_image(image, color_offset=True, glitch_amount=float(globals["val"]["characterGlitch"]), seed=int(globals["val"]["characterGlitchSeed"]))
    glitched_image.save('./tmp/char.png')
    return ImageTk.PhotoImage(glitched_image)

def gradientCharacter(gradient: str):
    globals["val"]["characterGradient"] = gradient
    if globals["val"]["characterGradient"] == "none":
        image: Image = Image.open(globals["characterPath"])
        image = image.resize((int(image.size[0] * int(globals["val"]["characterScale"]) / 100), int(image.size[1] * int(globals["val"]["characterScale"]) / 100)), Image.LANCZOS)
        image.save('./tmp/char.png')
        globals["gcChar"] = ImageTk.PhotoImage(image)
        if globals["val"]["characterGlitch"] != .1:
            globals["gcChar"] = glitching(Image.open('./tmp/char.png'))
        gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])
        return image
    globals["gcChar"] = None
    gui["frame"]["canvas"].character = None
    image = cv2.imread(globals["characterPath"], cv2.IMREAD_UNCHANGED)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.applyColorMap(image, getattr(cv2, "COLORMAP_" + globals["val"]["characterGradient"].upper()))
    image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
    image[:, :, 3] = cv2.imread(globals["characterPath"], cv2.IMREAD_UNCHANGED)[:, :, 3]
    image = Image.fromarray(image)
    image = image.resize((int(image.size[0] * int(globals["val"]["characterScale"]) / 100), int(image.size[1] * int(globals["val"]["characterScale"]) / 100)), Image.LANCZOS)
    globals["gcChar"] = ImageTk.PhotoImage(image)
    gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])
    image.save('./tmp/char.png')
    # if there is glitch appluy glitching effect
    if globals["val"]["characterGlitch"] != .1:
        image.save('./tmp/char.png')
        globals["gcChar"] = glitching(Image.open('./tmp/char.png'))
        gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])
    return image

def resizeAndUpdate() -> Image:
    image: Image = Image.open(globals["characterPath"])
    if globals["val"]["characterGradient"] != "none":
        image = gradientCharacter(globals["val"]["characterGradient"])
    image = image.resize((int(image.size[0] * int(globals["val"]["characterScale"]) / 100), int(image.size[1] * int(globals["val"]["characterScale"]) / 100)), Image.LANCZOS)
    if not os.path.exists('./tmp'):
        os.makedirs('./tmp')
    image.save('./tmp/char.png')
    return Image.open('./tmp/char.png')

def moveCharacter(axis, value) -> None:
    if globals["character"] is None:
        return
    globals["val"][axis] = value
    # change the position of the character according to % of the canvas
    gui["frame"]["canvas"].coords(globals["character"], gui["frame"]["canvas"].winfo_width() * int(globals["val"]["characterXpos"]) / 100, gui["frame"]["canvas"].winfo_height() * int(globals["val"]["characterYpos"]) / 100)

def scaleCharacter(axis, value) -> None:
    if globals["character"] is None:
        return
    globals["val"]["characterScale"] = value
    image: Image = resizeAndUpdate()
    globals["gcChar"]: Image = glitching(image)
    gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])

def glitchCharacter(axis, value) -> None:
    if globals["character"] is None:
        return
    globals["val"][axis] = value
    image = resizeAndUpdate()
    globals["gcChar"] = glitching(image)
    gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])

def glowCharacter(color: str) -> None:
    return