import os
from tkinter import filedialog
from data import globals
from PIL import Image

def outputPicture() -> None:
def outputPicture(cli: bool = False) -> None:
    # create an image of the selected background with a size of 460 x 495
    background = Image.open(globals["render"]["background"])
    # paste the misc image on the background image at the given position and given scale
    if globals["misc_container"] is not None and globals["render"]["characterPath"] != "picts/miscs/none.png":
        misc = Image.open(globals["render"]["misc"])
        misc = misc.resize((int(misc.size[0] * int(globals["render"]["val"]["miscScale"]) / 100), int(misc.size[1] * int(globals["render"]["val"]["miscScale"]) / 100)), Image.ANTIALIAS)
        misc = misc.rotate(int(globals["render"]["val"]["miscRotate"]), expand=True)
        background.paste(misc, (int(background.size[0] * int(globals["render"]["val"]["miscPosX"]) / 100), int(background.size[1] * int(globals["render"]["val"]["miscPosY"]) / 100)), misc)
    # paste the character image if the file tmp/char.png exists
    if os.path.exists("tmp/char.png"):
        character = Image.open("tmp/char.png")
    else:
        # if the file tmp/char.png does not exist, paste the character image from the selected character with the given position and scale
        character = Image.open(globals["render"]["characterPath"])
        character = character.resize((int(character.size[0] * int(globals["render"]["val"]["characterScale"]) / 100), int(character.size[1] * int(globals["render"]["val"]["characterScale"]) / 100)), Image.ANTIALIAS)
    background.paste(character, (int(background.size[0] * int(globals["render"]["val"]["characterXpos"]) / 100) - int(character.size[0] / 2), int(background.size[1] * int(globals["render"]["val"]["characterYpos"]) / 100) - int(character.size[1] / 2)), character)
    # apply the crt effect if the crt checkbox is checked
    if globals["render"]["val"]["crt"]:
        crt = Image.open("picts/crt/crt.png")
        background.paste(crt, (0, 0), crt)
    if cli == False:
        path = filedialog.asksaveasfilename(initialdir = os.getcwd(), title = "Select file", defaultextension=".png", initialfile="vaporwaved.png")
    else:
        path = globals["outputPath"] + "/output.png"
    background.save(path)