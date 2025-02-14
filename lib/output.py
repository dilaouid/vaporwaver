import os, errno, sys
from tkinter import filedialog
from data import globals, path_finder, get_temp_file
from PIL import Image

from lib.character import min_rotateCharacter, applygradient, resizeCharacter, glitchingCLI

def outputPicture(cli: bool = False) -> None:
    temp_files = []
    try:
        background = Image.open(path_finder(globals["render"]["background"]))
        
        if globals["render"]["misc"] != path_finder("picts/miscs/none.png"):
            misc = Image.open(path_finder(globals["render"]["misc"]))
            misc = misc.resize((
                int(misc.size[0] * int(globals["render"]["val"]["miscScale"]) / 100),
                int(misc.size[1] * int(globals["render"]["val"]["miscScale"]) / 100)
            ), Image.Resampling.LANCZOS)
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
            temp_char = get_temp_file("char")
            if os.path.exists(temp_char):
                character = Image.open(temp_char)
            else:
                character = Image.open(globals["render"]["val"]["characterPath"])
                character = character.resize((
                    int(character.size[0] * int(globals["render"]["val"]["characterScale"]) / 100),
                    int(character.size[1] * int(globals["render"]["val"]["characterScale"]) / 100)
                ), Image.Resampling.LANCZOS)
                character = character.rotate(int(globals["render"]["val"]["characterRotation"]), expand=True)
            background.paste(
                character,
                (
                    int(background.size[0] * int(globals["render"]["val"]["characterXpos"]) / 100) - int(character.size[0] / 2),
                    int(background.size[1] * int(globals["render"]["val"]["characterYpos"]) / 100) - int(character.size[1] / 2)
                ),
                character.split()[-1]  # utiliser explicitement le masque alpha
            )
            # Dans le mode GUI, le chemin est choisi via filedialog
            from tkinter import filedialog
            path_save = filedialog.asksaveasfilename(
                initialdir=os.getcwd(),
                title="Select file",
                defaultextension=".png",
                initialfile="vaporwaved.png"
            )
        else:
            if globals["render"]["val"]["characterGradient"] != "none":
                working_character = applygradient(get_temp_file("char-cli"))
                temp_files.append(get_temp_file("char-cli"))
            else:
                temp_cli = get_temp_file("char-cli")
                working_character = Image.open(globals["render"]["val"]["characterPath"])
                working_character = resizeCharacter(working_character)
                if globals["render"]["val"]["characterRotation"]:
                    working_character = min_rotateCharacter(working_character)
                working_character.save(temp_cli)
                temp_files.append(temp_cli)
                working_character = Image.open(temp_cli)
            
            working_character = glitchingCLI(working_character)
            
            # S'assurer que l'image est en RGBA et utiliser son canal alpha comme masque
            if working_character.mode != 'RGBA':
                working_character = working_character.convert('RGBA')
            background.paste(
                working_character,
                (
                    int(background.size[0] * int(globals["render"]["val"]["characterXpos"]) / 100) - int(working_character.size[0] / 2),
                    int(background.size[1] * int(globals["render"]["val"]["characterYpos"]) / 100) - int(working_character.size[1] / 2)
                ),
                working_character.split()[-1]
            )

        if globals["render"]["val"]["crt"]:
            crt = Image.open(path_finder("picts/crt/crt.png"))
            background.paste(crt, (0, 0), crt)
        
        background.save(globals["render"]["output"])
        # Nettoyage
        temp_cli = get_temp_file("char-cli")
        if os.path.exists(temp_cli):
            os.remove(temp_cli)
    finally:
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception as e:
                print(f"Warning: Could not remove temporary file {temp_file}: {e}")