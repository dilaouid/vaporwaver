import os, errno, sys
from tkinter import filedialog
from data import globals, path_finder
from PIL import Image

from lib.character import min_rotateCharacter, applygradient, resizeCharacter, glitchingCLI

def outputPicture(cli: bool = False) -> None:
    background = Image.open(path_finder(globals["render"]["background"]))
    
    if globals["render"]["misc"] != path_finder("picts/miscs/none.png"):
        misc = Image.open(path_finder(globals["render"]["misc"]))
        misc = misc.resize(
            (
                int(misc.size[0] * int(globals["render"]["val"]["miscScale"]) / 100),
                int(misc.size[1] * int(globals["render"]["val"]["miscScale"]) / 100)
            ),
            Image.Resampling.LANCZOS
        )
        misc = misc.rotate(int(globals["render"]["val"]["miscRotate"]), expand=True)
        background.paste(
            misc,
            (
                int(background.size[0] * int(globals["render"]["val"]["miscPosX"]) / 100),
                int(background.size[1] * int(globals["render"]["val"]["miscPosY"]) / 100)
            ),
            misc
        )
    
    if os.path.exists("tmp/char.png"):
        character = Image.open("tmp/char.png")
    else:
        character = Image.open(globals["render"]["val"]["characterPath"])
        character = character.resize(
            (
                int(character.size[0] * int(globals["render"]["val"]["characterScale"]) / 100),
                int(character.size[1] * int(globals["render"]["val"]["characterScale"]) / 100)
            ),
            Image.Resampling.LANCZOS
        )
        character = character.rotate(int(globals["render"]["val"]["characterRotation"]), expand=True)
    
    if not cli:
        background.paste(
            character,
            (
                int(background.size[0] * int(globals["render"]["val"]["characterXpos"]) / 100) - int(character.size[0] / 2),
                int(background.size[1] * int(globals["render"]["val"]["characterYpos"]) / 100) - int(character.size[1] / 2)
            ),
            character
        )
        path_save = filedialog.asksaveasfilename(
            initialdir=os.getcwd(),
            title="Select file",
            defaultextension=".png",
            initialfile="vaporwaved.png"
        )
        if globals["render"]["val"]["crt"]:
            crt = Image.open(path_finder("picts/crt/crt.png"))
            background.paste(crt, (0, 0), crt)
    else:
        path_save = globals["render"]["output"]
        output_dir = os.path.dirname(path_save)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except OSError as exc:
                sys.stderr.write("Error: The path is invalid, should be like 'path/to/file.png'")
                if exc.errno != errno.EEXIST:
                    raise
        character = Image.open(globals["render"]["val"]["characterPath"])
        character = resizeCharacter(character)
        character = min_rotateCharacter(character)
        if globals["render"]["val"]["characterGradient"] != "none":
            character = applygradient(path_finder('./tmp/char-cli.png'))
        else:
            character.save('./tmp/char-cli.png')
            character = Image.open('./tmp/char-cli.png')
        character = glitchingCLI(character)
        background.paste(character, (int(background.size[0] * int(globals["render"]["val"]["characterXpos"]) / 100) - int(character.size[0] / 2),
                                      int(background.size[1] * int(globals["render"]["val"]["characterYpos"]) / 100) - int(character.size[1] / 2)), character)
        if globals["render"]["val"]["crt"]:
            crt = Image.open(path_finder("picts/crt/crt.png"))
            background.paste(crt, (0, 0), crt)

    
    background.save(path_save)
    if os.path.exists("./tmp/char-cli.png"):
        os.remove("./tmp/char-cli.png")
