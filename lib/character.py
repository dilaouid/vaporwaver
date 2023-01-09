from data import globals, gui
from PIL import Image, ImageTk
from glitch_this import ImageGlitcher
import cv2

glitching: bool = False

def gradientCharacter(gradient: str):
    if glitching == False:
        globals["val"]["characterGlitch"] = .1
        globals["val"]["characterGlitchSeed"] = 0
        gui["el"]["char"]["glitch"].set(.1)
        gui["el"]["char"]["glitchSeed"].set(0)
    globals["val"]["characterGradient"] = gradient
    if globals["val"]["characterGradient"] == "none":
        image: Image = Image.open(globals["characterPath"])
        image = image.resize((int(image.size[0] * int(globals["val"]["characterScale"]) / 100), int(image.size[1] * int(globals["val"]["characterScale"]) / 100)), Image.LANCZOS)
        globals["gcChar"] = ImageTk.PhotoImage(image)
        gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])
        return image


    globals["gcChar"] = None
    gui["frame"]["canvas"].character = None
    print(globals["val"]["characterGradient"])
    image = cv2.imread(globals["characterPath"], cv2.IMREAD_UNCHANGED)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.applyColorMap(image, getattr(cv2, "COLORMAP_" + globals["val"]["characterGradient"].upper()))
    image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
    image[:, :, 3] = cv2.imread(globals["characterPath"], cv2.IMREAD_UNCHANGED)[:, :, 3]
    image = Image.fromarray(image)
    image = image.resize((int(image.size[0] * int(globals["val"]["characterScale"]) / 100), int(image.size[1] * int(globals["val"]["characterScale"]) / 100)), Image.LANCZOS)
    globals["gcChar"] = ImageTk.PhotoImage(image)
    gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])
    return image

def resizeAndUpdate():
    image: Image = Image.open(globals["characterPath"])
    if globals["val"]["characterGradient"] != "none":
        image = gradientCharacter(globals["val"]["characterGradient"])
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
    image: Image = resizeAndUpdate()

    glitcher = ImageGlitcher()
    glitched_image: Image = glitcher.glitch_image(image, color_offset=True, glitch_amount=float(globals["val"]["characterGlitch"]), seed=int(globals["val"]["characterGlitchSeed"]))
    globals["gcChar"]: Image = ImageTk.PhotoImage(glitched_image)
    gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])

def glitchCharacter(axis, value):
    if globals["character"] is None:
        return
    globals["val"][axis] = value
    global glitching
    glitching = True
    image = resizeAndUpdate()

    glitcher = ImageGlitcher()
    glitched_image = glitcher.glitch_image(image, color_offset=True, glitch_amount=float(globals["val"]["characterGlitch"]), seed=int(globals["val"]["characterGlitchSeed"]))
    globals["gcChar"] = ImageTk.PhotoImage(glitched_image)
    gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])
    glitching = False