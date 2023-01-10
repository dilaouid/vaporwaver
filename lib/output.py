import os
from data import globals
from PIL import Image

def outputPicture() -> None:
    # create an image of the selected background with a size of 460 x 495
    background = Image.open(globals["background"])
    # paste the misc image on the background image at the given position and given scale
    if globals["misc_container"] is not None and globals["misc"] != "picts/miscs/none.png":
        misc = Image.open(globals["misc"])
        misc = misc.resize((int(misc.size[0] * int(globals["val"]["miscScale"]) / 100), int(misc.size[1] * int(globals["val"]["miscScale"]) / 100)), Image.ANTIALIAS)
        misc = misc.rotate(int(globals["val"]["miscRotate"]), expand=True)
        background.paste(misc, (int(background.size[0] * int(globals["val"]["miscPosX"]) / 100), int(background.size[1] * int(globals["val"]["miscPosY"]) / 100)), misc)
    # paste the character image if the file tmp/char.png exists
    if os.path.exists("tmp/char.png"):
        character = Image.open("tmp/char.png")
        background.paste(character, (int(background.size[0] * int(globals["val"]["characterXpos"]) / 100), int(background.size[1] * int(globals["val"]["characterYpos"]) / 100)), character)
    else:
        # if the file tmp/char.png does not exist, paste the character image from the selected character with the given position and scale
        character = Image.open(globals["characterPath"])
        character = character.resize((int(character.size[0] * int(globals["val"]["characterScale"]) / 100), int(character.size[1] * int(globals["val"]["characterScale"]) / 100)), Image.ANTIALIAS)
        background.paste(character, (int(background.size[0] * int(globals["val"]["characterXpos"]) / 100), int(background.size[1] * int(globals["val"]["characterYpos"]) / 100)), character)
    # apply the crt effect if the crt checkbox is checked
    if globals["val"]["crt"]:
        crt = Image.open("picts/crt/crt.png")
        background.paste(crt, (0, 0), crt)
    # save the image
    background.save("tmp/output.png")