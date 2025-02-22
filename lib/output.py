# output.py
import os
from data import globals, path_finder, get_temp_file
from PIL import Image

from lib.image_handler import load_and_convert_image, save_as_png
from lib.character import min_rotateCharacter, applygradient, resizeCharacter, glitchingCLI, get_centered_position

def outputPicture(cli: bool = False) -> None:
    temp_files = []
    try:
        background = Image.open(path_finder(globals["render"]["background"]))
        # Ensure background is in RGBA mode
        if background.mode != 'RGBA':
            background = background.convert('RGBA')
        
        # Préparer le character et le misc avant de les coller
        misc_prepared = None
        character_prepared = None
        
        # Préparer le misc s'il y en a un
        if globals["render"]["misc"] != path_finder("picts/miscs/none.png"):
            misc_prepared = load_and_convert_image(path_finder(globals["render"]["misc"]))
            
            # S'assurer que miscScale a une valeur valide (par défaut 100)
            misc_scale = globals["render"]["val"].get("miscScale", 100)
            
            # Calculer les nouvelles dimensions
            new_width = int(misc_prepared.size[0] * misc_scale / 100)
            new_height = int(misc_prepared.size[1] * misc_scale / 100)
            
            # Vérifier que les dimensions sont valides
            if new_width > 0 and new_height > 0:
                misc_prepared = misc_prepared.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Rotation avec la valeur par défaut 0 si non définie
            misc_rotate = globals["render"]["val"].get("miscRotate", 0)
            misc_prepared = misc_prepared.rotate(misc_rotate, expand=True)
        
        # Préparer le character selon le mode (GUI ou CLI)
        if not cli:
            temp_char = get_temp_file("char")
            if os.path.exists(temp_char):
                character_prepared = load_and_convert_image(temp_char)
            else:
                character_prepared = load_and_convert_image(globals["render"]["val"]["characterPath"])
                character_prepared = character_prepared.resize((
                    int(character_prepared.size[0] * int(globals["render"]["val"]["characterScale"]) / 100),
                    int(character_prepared.size[1] * int(globals["render"]["val"]["characterScale"]) / 100)
                ), Image.Resampling.LANCZOS)
                character_prepared = character_prepared.rotate(int(globals["render"]["val"]["characterRotation"]), expand=True)
        else:
            if globals["render"]["val"]["characterGradient"] != "none":
                character_prepared = applygradient(get_temp_file("char-cli"))
                temp_files.append(get_temp_file("char-cli"))
            else:
                temp_cli = get_temp_file("char-cli")
                character_prepared = Image.open(globals["render"]["val"]["characterPath"])
                character_prepared = resizeCharacter(character_prepared)
                if globals["render"]["val"]["characterRotation"]:
                    character_prepared = min_rotateCharacter(character_prepared)
                character_prepared.save(temp_cli)
                temp_files.append(temp_cli)
                character_prepared = Image.open(temp_cli)
            
            character_prepared = glitchingCLI(character_prepared)
            if character_prepared.mode != 'RGBA':
                character_prepared = character_prepared.convert('RGBA')

        # Coller les éléments dans l'ordre selon misc_above_character
        if globals.get("misc_above_character", False):
            # Character en premier, puis misc par dessus
            if character_prepared is not None:
                alpha_mask = character_prepared.split()[3]
                x, y = get_centered_position(
                    background.size[0],
                    background.size[1],
                    int(globals["render"]["val"]["characterXpos"]),
                    int(globals["render"]["val"]["characterYpos"])
                )
                paste_x = int(x - character_prepared.size[0] / 2)
                paste_y = int(y - character_prepared.size[1] / 2)
                background.paste(character_prepared, (paste_x, paste_y), alpha_mask)

            if misc_prepared is not None:
                alpha_mask = misc_prepared.split()[3]
                misc_x = int(background.size[0] * int(globals["render"]["val"]["miscPosX"]) / 100) - int(misc_prepared.size[0] / 2)
                misc_y = int(background.size[1] * int(globals["render"]["val"]["miscPosY"]) / 100) - int(misc_prepared.size[1] / 2)
                background.paste(misc_prepared, (misc_x, misc_y), alpha_mask)
        else:
            # Misc en premier, puis character par dessus
            if misc_prepared is not None:
                alpha_mask = misc_prepared.split()[3]
                misc_x = int(background.size[0] * int(globals["render"]["val"]["miscPosX"]) / 100) - int(misc_prepared.size[0] / 2)
                misc_y = int(background.size[1] * int(globals["render"]["val"]["miscPosY"]) / 100) - int(misc_prepared.size[1] / 2)
                background.paste(misc_prepared, (misc_x, misc_y), alpha_mask)

            if character_prepared is not None:
                alpha_mask = character_prepared.split()[3]
                x, y = get_centered_position(
                    background.size[0],
                    background.size[1],
                    int(globals["render"]["val"]["characterXpos"]),
                    int(globals["render"]["val"]["characterYpos"])
                )
                paste_x = int(x - character_prepared.size[0] / 2)
                paste_y = int(y - character_prepared.size[1] / 2)
                background.paste(character_prepared, (paste_x, paste_y), alpha_mask)

        # Ajouter l'effet CRT si activé
        if globals["render"]["val"]["crt"]:
            crt = Image.open(path_finder("picts/crt/crt.png"))
            if crt.mode != 'RGBA':
                crt = crt.convert('RGBA')
            alpha_mask = crt.split()[3]
            background.paste(crt, (0, 0), alpha_mask)

        # Gérer la sauvegarde en mode GUI
        if not cli:
            from tkinter import filedialog
            path_save = filedialog.asksaveasfilename(
                initialdir=os.getcwd(),
                title="Select file",
                defaultextension=".png",
                initialfile="vaporwaved.png"
            )
            if not path_save:
                return
            globals["render"]["output"] = path_save

        # Vérifier et sauvegarder
        if not globals["render"]["output"] or not os.path.splitext(globals["render"]["output"])[1]:
            print("Erreur: Chemin de sortie invalide ou sans extension")
            return
            
        print(f"Saving to {globals['render']['output']}")
        save_as_png(background, globals["render"]["output"])

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
