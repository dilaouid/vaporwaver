import os
from tkinter import filedialog
from PIL import Image

from data import globals, path_finder, get_temp_file
from lib.image_handler import load_and_convert_image, save_as_png
from lib.elements import Character, Misc
from lib.image_processor import ImageProcessor

class OutputHandler:
    def __init__(self, cli_mode: bool = False):
        self.cli_mode = cli_mode
        self.temp_files = []
        self.character_processor = Character(None, None)
        self.misc_processor = Misc(None, None)
        self.image_processor = ImageProcessor()

    def prepare_background(self) -> Image.Image:
        """Prépare l'image de fond"""
        background = Image.open(path_finder(globals["render"]["background"]))
        return self.image_processor.ensure_rgba(background)

    def prepare_character(self) -> Image.Image:
        """Prépare l'image du personnage selon le mode (CLI/GUI)"""
        if self.cli_mode:
            return self._prepare_cli_character()
        return self._prepare_gui_character()

    def _prepare_gui_character(self) -> Image.Image:
        """
        Prépare le personnage en mode GUI en partant du fichier converti (s'il existe)
        et en appliquant à chaque fois le gradient et/ou le glitch selon les paramètres actuels.
        Le résultat est sauvegardé dans un unique fichier temporaire ("char").
        """
        temp_char = get_temp_file("char")
        # Toujours supprimer le précédent fichier temporaire pour forcer le recalcul
        if os.path.exists(temp_char):
            os.remove(temp_char)
        
        # Si un fichier converti existe (créé lors de l'import), l'utiliser comme base.
        temp_conv = get_temp_file("char-converted")
        if os.path.exists(temp_conv):
            character = load_and_convert_image(temp_conv)
        else:
            # Sinon, utiliser le chemin d'origine (mais dans l'idéal, mettez à jour votre import pour que
            # globals["render"]["characterPath"] pointe sur le fichier converti)
            character = load_and_convert_image(globals["render"]["characterPath"])
        
        cp = self.character_processor

        # Appliquer le gradient si nécessaire
        if globals["render"]["val"]["characterGradient"] != "none":
            character = cp.apply_gradient(character, globals["render"]["val"]["characterGradient"])
        
        # Appliquer les transformations de base (scale et rotation)
        character = cp.transform_image(
            character,
            int(globals["render"]["val"]["characterScale"]),
            int(globals["render"]["val"]["characterRotation"])
        )
        
        # Appliquer le glitch si nécessaire
        if float(globals["render"]["val"]["characterGlitch"]) != 0.1:
            character = cp.apply_glitch(
                character,
                float(globals["render"]["val"]["characterGlitch"]),
                int(globals["render"]["val"]["characterGlitchSeed"])
            )
        
        # Sauvegarder le résultat dans le fichier temporaire unique
        character.save(temp_char, "PNG")
        self.temp_files.append(temp_char)
        return character

    def _prepare_cli_character(self) -> Image.Image:
        """
        Prépare le personnage en mode CLI.
        (Le principe est similaire au mode GUI, en veillant à sauvegarder le résultat glitché dans un fichier temporaire.)
        """
        character_path = globals["render"].get("characterPath")
        if not character_path:
            raise ValueError("Character path not found")

        cp = self.character_processor
        if globals["render"]["val"]["characterGradient"] != "none":
            character = Image.open(character_path)
            character = cp.apply_gradient(character, globals["render"]["val"]["characterGradient"])
            character = cp.transform_image(
                character,
                int(globals["render"]["val"]["characterScale"]),
                int(globals["render"]["val"]["characterRotation"])
            )
            temp_file = get_temp_file("char-cli")
            character.save(temp_file)
            self.temp_files.append(temp_file)
        else:
            temp_file = get_temp_file("char-cli")
            character = Image.open(character_path)
            character = cp.transform_image(
                character,
                int(globals["render"]["val"]["characterScale"]),
                int(globals["render"]["val"]["characterRotation"])
            )
            character.save(temp_file)
            self.temp_files.append(temp_file)
        
        # Appliquer le glitch si nécessaire
        if float(globals["render"]["val"]["characterGlitch"]) != 0.1:
            character = cp.apply_glitch(
                character,
                float(globals["render"]["val"]["characterGlitch"]),
                int(globals["render"]["val"]["characterGlitchSeed"])
            )
        return self.image_processor.ensure_rgba(character)

    def prepare_misc(self) -> Image.Image:
        """Prépare l'image misc si elle existe"""
        if globals["render"]["misc"] == path_finder("picts/miscs/none.png"):
            return None

        misc = load_and_convert_image(path_finder(globals["render"]["misc"]))
        return self.misc_processor.transform_image(
            misc,
            int(globals["render"]["val"].get("miscScale", 100)),
            int(globals["render"]["val"].get("miscRotate", 0))
        )

    def paste_character(self, background: Image.Image, character: Image.Image) -> None:
        """Colle le personnage sur le fond"""
        if character is None:
            return

        alpha_mask = character.split()[3]
        x, y = self.image_processor.calculate_center_position(
            background.size,
            (int(globals["render"]["val"]["characterXpos"]),
             int(globals["render"]["val"]["characterYpos"]))
        )
        
        paste_x = int(x - character.size[0] / 2)
        paste_y = int(y - character.size[1] / 2)
        background.paste(character, (paste_x, paste_y), alpha_mask)

    def paste_misc(self, background: Image.Image, misc: Image.Image) -> None:
        """Colle le misc sur le fond"""
        if misc is None:
            return

        alpha_mask = misc.split()[3]
        x, y = self.image_processor.calculate_center_position(
            background.size,
            (int(globals["render"]["val"]["miscPosX"]),
             int(globals["render"]["val"]["miscPosY"]))
        )
        
        paste_x = int(x - misc.size[0] / 2)
        paste_y = int(y - misc.size[1] / 2)
        background.paste(misc, (paste_x, paste_y), alpha_mask)

    def apply_crt_effect(self, background: Image.Image) -> None:
        """Applique l'effet CRT si activé"""
        if not globals["render"]["val"]["crt"]:
            return

        crt = Image.open(path_finder("picts/crt/crt.png"))
        crt = self.image_processor.ensure_rgba(crt)
        background.paste(crt, (0, 0), crt.split()[3])

    def handle_gui_save(self) -> bool:
        """Gère la sauvegarde en mode GUI"""
        if self.cli_mode:
            return True

        path_save = filedialog.asksaveasfilename(
            initialdir=os.getcwd(),
            title="Select file",
            defaultextension=".png",
            initialfile="vaporwaved.png"
        )
        if not path_save:
            return False

        globals["render"]["output"] = path_save
        return True

    def cleanup(self) -> None:
        """Nettoie les fichiers temporaires utilisés"""
        # Supprimer le fichier temporaire unique "char"
        temp_char = get_temp_file("char")
        if os.path.exists(temp_char):
            try:
                os.remove(temp_char)
            except Exception as e:
                print(f"Warning: Could not remove temporary file {temp_char}: {e}")
        
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception as e:
                print(f"Warning: Could not remove temporary file {temp_file}: {e}")

def outputPicture(cli: bool = False) -> None:
    temp_files = []
    try:
        background = Image.open(path_finder(globals["render"]["background"]))
        if background.mode != 'RGBA':
            background = background.convert('RGBA')
        bg_width, bg_height = background.size
        
        # Préparer character et misc
        character = None
        misc = None
        
        # Préparer le misc si ce n'est pas "none"
        if globals["render"]["misc"] != path_finder("picts/miscs/none.png"):
            misc = load_and_convert_image(path_finder(globals["render"]["misc"]))
            handler = OutputHandler(cli_mode=True)
            misc = handler.misc_processor.transform_image(
                misc,
                int(globals["render"]["val"].get("miscScale", 100)),
                int(globals["render"]["val"].get("miscRotate", 0))
            )

        # Préparer le character
        if not cli:
            temp_char = get_temp_file("char")
            if os.path.exists(temp_char):
                character = load_and_convert_image(temp_char)
            else:
                character = load_and_convert_image(globals["render"]["characterPath"])
                character_processor = Character(None, None)
                
                character = character_processor.transform_image(
                    character,
                    int(globals["render"]["val"]["characterScale"]),
                    int(globals["render"]["val"]["characterRotation"])
                )
        else:
            if globals["render"]["val"]["characterGradient"] != "none":
                character = Image.open(globals["render"]["characterPath"])
                character_processor = Character(None, None)
                character = character_processor.apply_gradient(
                    character,
                    globals["render"]["val"]["characterGradient"]
                )
                character = character_processor.transform_image(
                    character,
                    int(globals["render"]["val"]["characterScale"]),
                    int(globals["render"]["val"]["characterRotation"])
                )
                temp_files.append(get_temp_file("char-cli"))
            else:
                temp_cli = get_temp_file("char-cli")
                character = Image.open(globals["render"]["characterPath"])
                character_processor = Character(None, None)
                character = character_processor.transform_image(
                    character,
                    int(globals["render"]["val"]["characterScale"]),
                    int(globals["render"]["val"]["characterRotation"])
                )
                character.save(temp_cli)
                temp_files.append(temp_cli)
                character = character_processor.apply_glitch(
                    character,
                    float(globals["render"]["val"]["characterGlitch"]),
                    int(globals["render"]["val"]["characterGlitchSeed"])
                )


        # Vérifier que le chemin de sortie est valide
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
        
        # Coller les éléments dans le bon ordre selon misc_above_character
        if not globals.get("misc_above_character", False):
            if misc is not None:
                alpha_mask = misc.split()[3]
                misc_x = bg_width // 2 + int(bg_width * int(globals["render"]["val"]["miscPosX"]) / 100) - misc.width // 2
                misc_y = bg_height // 2 + int(bg_height * int(globals["render"]["val"]["miscPosY"]) / 100) - misc.height // 2
                background.paste(misc, (misc_x, misc_y), alpha_mask)
            if character is not None:
                alpha_mask = character.split()[3]
                char_x = bg_width // 2 + int(bg_width * int(globals["render"]["val"]["characterXpos"]) / 100) - character.width // 2
                char_y = bg_height // 2 + int(bg_height * int(globals["render"]["val"]["characterYpos"]) / 100) - character.height // 2
                background.paste(character, (char_x, char_y), alpha_mask)
        else:
            if character is not None:
                alpha_mask = character.split()[3]
                char_x = bg_width // 2 + int(bg_width * int(globals["render"]["val"]["characterXpos"]) / 100) - character.width // 2
                char_y = bg_height // 2 + int(bg_height * int(globals["render"]["val"]["characterYpos"]) / 100) - character.height // 2
                background.paste(character, (char_x, char_y), alpha_mask)
            if misc is not None:
                alpha_mask = misc.split()[3]
                misc_x = bg_width // 2 + int(bg_width * int(globals["render"]["val"]["miscPosX"]) / 100) - misc.width // 2
                misc_y = bg_height // 2 + int(bg_height * int(globals["render"]["val"]["miscPosY"]) / 100) - misc.height // 2
                background.paste(misc, (misc_x, misc_y), alpha_mask)


        # Effet CRT
        if globals["render"]["val"]["crt"]:
            crt = Image.open(path_finder("picts/crt/crt.png"))
            if crt.mode != 'RGBA':
                crt = crt.convert('RGBA')
            alpha_mask = crt.split()[3]
            background.paste(crt, (0, 0), alpha_mask)
        
        # Sauvegarder
        print(f"Saving to {globals['render']['output']}")
        save_as_png(background, globals["render"]["output"])
        
    except Exception as e:
        print(f"Error in outputPicture: {str(e)}")
    finally:
        # Nettoyage des fichiers temporaires
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception as e:
                print(f"Warning: Could not remove temporary file {temp_file}: {e}")