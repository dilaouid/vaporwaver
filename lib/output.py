import os, errno, sys
from tkinter import filedialog
from data import globals, path_finder
from PIL import Image

from lib.character import min_rotateCharacter, applygradient, resizeCharacter, glitchingCLI

def outputPicture(cli: bool = False) -> None:
    temp_files = []
    try:
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
        
        if not cli:
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
            
            # Créer une copie en mémoire pour éviter la corruption
            working_character = character.copy()
            
            if globals["render"]["val"]["characterGradient"] != "none":
                working_character = applygradient(path_finder('./tmp/char-cli.png'))
                temp_files.append('./tmp/char-cli.png')
            else:
                temp_file = './tmp/char-cli.png'
                working_character.save(temp_file)
                temp_files.append(temp_file)
                working_character = Image.open(temp_file)

            
            # Appliquer le glitch directement sur l'image en mémoire
            working_character = glitchingCLI(working_character)
            
            # Coller l'image en mémoire
            background.paste(
                working_character,
                (
                    int(background.size[0] * int(globals["render"]["val"]["characterXpos"]) / 100) - int(working_character.size[0] / 2),
                    int(background.size[1] * int(globals["render"]["val"]["characterYpos"]) / 100) - int(working_character.size[1] / 2)
                ),
                working_character
            )

        if globals["render"]["val"]["crt"]:
            crt = Image.open(path_finder("picts/crt/crt.png"))
            background.paste(crt, (0, 0), crt)
        
        background.save(path_save)
        if os.path.exists("./tmp/char-cli.png"):
            os.remove("./tmp/char-cli.png")
    finally:
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception as e:
                print(f"Warning: Could not remove temporary file {temp_file}: {e}")
