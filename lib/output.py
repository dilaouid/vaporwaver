import os
from data import globals, path_finder, get_temp_file
from PIL import Image

from lib.character import min_rotateCharacter, applygradient, resizeCharacter, glitchingCLI

def outputPicture(cli: bool = False) -> None:
    temp_files = []
    try:
        background = Image.open(path_finder(globals["render"]["background"]))
        # Ensure background is in RGBA mode
        if background.mode != 'RGBA':
            background = background.convert('RGBA')
        
        if globals["render"]["misc"] != path_finder("picts/miscs/none.png"):
            misc = Image.open(path_finder(globals["render"]["misc"]))
            # Ensure misc is in RGBA mode
            if misc.mode != 'RGBA':
                misc = misc.convert('RGBA')
                
            misc = misc.resize((
                int(misc.size[0] * int(globals["render"]["val"]["miscScale"]) / 100),
                int(misc.size[1] * int(globals["render"]["val"]["miscScale"]) / 100)
            ), Image.Resampling.LANCZOS)
            misc = misc.rotate(int(globals["render"]["val"]["miscRotate"]), expand=True)
            
            # Get alpha channel safely
            alpha_mask = None
            if misc.mode == 'RGBA':
                # Use alpha channel if available
                alpha_mask = misc.split()[3]
            
            # Calculate center position for misc (centered anchor point)
            misc_x = int(background.size[0] * int(globals["render"]["val"]["miscPosX"]) / 100) - int(misc.size[0] / 2)
            misc_y = int(background.size[1] * int(globals["render"]["val"]["miscPosY"]) / 100) - int(misc.size[1] / 2)
            
            # Safer paste operation with centered misc
            background.paste(
                misc,
                (misc_x, misc_y),
                alpha_mask
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
            
            # Ensure character is in RGBA mode and get alpha safely
            if character.mode != 'RGBA':
                character = character.convert('RGBA')
            
            alpha_mask = character.split()[3]
            
            background.paste(
                character,
                (
                    int(background.size[0] * int(globals["render"]["val"]["characterXpos"]) / 100) - int(character.size[0] / 2),
                    int(background.size[1] * int(globals["render"]["val"]["characterYpos"]) / 100) - int(character.size[1] / 2)
                ),
                alpha_mask
            )
            # Dans le mode GUI, le chemin est choisi via filedialog
            from tkinter import filedialog
            path_save = filedialog.asksaveasfilename(
                initialdir=os.getcwd(),
                title="Select file",
                defaultextension=".png",
                initialfile="vaporwaved.png"
            )
            # Si l'utilisateur annule la sauvegarde, sortir de la fonction
            if not path_save:
                return
            globals["render"]["output"] = path_save
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
            
            # Ensure image is in RGBA mode and get alpha safely
            if working_character.mode != 'RGBA':
                working_character = working_character.convert('RGBA')
            
            alpha_mask = working_character.split()[3]
            
            background.paste(
                working_character,
                (
                    int(background.size[0] * int(globals["render"]["val"]["characterXpos"]) / 100) - int(working_character.size[0] / 2),
                    int(background.size[1] * int(globals["render"]["val"]["characterYpos"]) / 100) - int(working_character.size[1] / 2)
                ),
                alpha_mask
            )

        if globals["render"]["val"]["crt"]:
            crt = Image.open(path_finder("picts/crt/crt.png"))
            # Ensure CRT overlay is in RGBA
            if crt.mode != 'RGBA':
                crt = crt.convert('RGBA')
            alpha_mask = crt.split()[3]
            background.paste(crt, (0, 0), alpha_mask)
        
        # Vérifier que le chemin de sortie a une extension valide
        if not globals["render"]["output"] or not os.path.splitext(globals["render"]["output"])[1]:
            print("Erreur: Chemin de sortie invalide ou sans extension")
            return
            
        print(f"Saving to {globals['render']['output']}")
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