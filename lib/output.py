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
        self.tmp_dir = globals.get("tmp_dir") or os.environ.get('VAPORWAVER_TMP')
        self._register_cleanup()
        
        if not self.tmp_dir:
            raise ValueError("No temporary directory specified")
            
        print(f"OutputHandler initialized with tmp_dir: {self.tmp_dir}")

    def _register_cleanup(self):
        """Enregistre le nettoyage à faire à la fermeture du programme"""
        import atexit
        atexit.register(self.cleanup)

    def prepare_paths(self):
        # Vérifier et préparer tous les chemins nécessaires
        if not globals["render"].get("characterPath"):
            raise ValueError("Character path not set in globals")
            
        # Vérifier que le fichier character existe
        char_path = globals["render"]["characterPath"]
        if not os.path.isfile(char_path):
            raise ValueError(f"Character file not found: {char_path}")
            
        # Vérifier que le dossier temp existe
        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir, exist_ok=True)

    def process_image(self):
        """Process the image with all effects and save it"""
        try:
            # Vérifier que tous les chemins nécessaires existent
            output_path = globals["render"].get("output")
            if not output_path:
                raise ValueError("No output path specified")
            print(f"Will save to: {output_path}")
                
            # Préparer le background
            try:
                background = self.prepare_background()
                print("Background prepared successfully")
            except Exception as e:
                raise ValueError(f"Failed to prepare background: {str(e)}")
            
            # Préparer le character
            try:
                character = self.prepare_character()
                print("Character prepared successfully")
            except Exception as e:
                raise ValueError(f"Failed to prepare character: {str(e)}")
                
            # Préparer le misc si nécessaire
            misc = None
            try:
                if globals["render"]["misc"] != path_finder("picts/miscs/none.png"):
                    misc = self.prepare_misc()
                    print("Misc prepared successfully")
            except Exception as e:
                print(f"Warning: Failed to prepare misc: {str(e)}")
                
            # Assembler l'image dans le bon ordre
            try:
                if not globals.get("misc_above_character", False):
                    # Misc en dessous du character
                    if misc is not None:
                        self.paste_misc(background, misc)
                        print("Misc pasted successfully")
                    self.paste_character(background, character)
                    print("Character pasted successfully")
                else:
                    # Misc au-dessus du character
                    self.paste_character(background, character)
                    print("Character pasted successfully")
                    if misc is not None:
                        self.paste_misc(background, misc)
                        print("Misc pasted successfully")
                
                # Appliquer l'effet CRT si activé
                if globals["render"]["val"].get("crt", False):
                    self.apply_crt_effect(background)
                    print("CRT effect applied")
                    
            except Exception as e:
                raise ValueError(f"Failed to compose image: {str(e)}")
            
            # Sauvegarder l'image
            try:
                output_dir = os.path.dirname(output_path)
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)
                print(f"Saving output to: {output_path}")
                background.save(output_path, "PNG")
                print(f"Image saved successfully to {output_path}")
                if not os.path.exists(output_path):
                    raise ValueError(f"Output file was not created at {output_path}")
            except Exception as e:
                raise ValueError(f"Failed to save output image: {str(e)}")
            
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            raise



    def prepare_background(self) -> Image.Image:
        """Prépare l'image de fond"""
        background = Image.open(path_finder(globals["render"]["background"]))
        return self.image_processor.ensure_rgba(background)

    def paste_character(self, background: Image.Image, character: Image.Image) -> None:
        """Colle le personnage sur le fond en utilisant la même logique que le GUI"""
        if character is None:
            return

        # Récupérer les dimensions
        bg_width, bg_height = background.size
        char_width, char_height = character.size
        
        # Calculer la position exactement comme dans le GUI
        # Le GUI calcule: center + (containerSize * percent / 100)
        char_x_percent = int(globals["render"]["val"]["characterXpos"])
        char_y_percent = int(globals["render"]["val"]["characterYpos"])
        
        # Position centrale
        center_x = bg_width / 2
        center_y = bg_height / 2
        
        # Ajustement basé sur le pourcentage
        x = center_x + (bg_width * char_x_percent / 100)
        y = center_y + (bg_height * char_y_percent / 100)
        
        # Ajustement pour centrer le character (anchor="center")
        paste_x = int(x - char_width / 2)
        paste_y = int(y - char_height / 2)
        
        print(f"Background size: {bg_width}x{bg_height}")
        print(f"Character size: {char_width}x{char_height}")
        print(f"Character position %: ({char_x_percent}, {char_y_percent})")
        print(f"Center position: ({center_x}, {center_y})")
        print(f"Adjusted position: ({x}, {y})")
        print(f"Final paste position: ({paste_x}, {paste_y})")
        
        # Extraire le masque alpha et coller
        alpha_mask = character.split()[3]
        background.paste(character, (paste_x, paste_y), alpha_mask)

    def paste_misc(self, background: Image.Image, misc: Image.Image) -> None:
        """Colle le misc sur le fond en utilisant la même logique que le GUI"""
        if misc is None:
            return

        # Récupérer les dimensions
        bg_width, bg_height = background.size
        misc_width, misc_height = misc.size
        
        # Calculer la position exactement comme dans le GUI
        misc_x_percent = int(globals["render"]["val"]["miscPosX"])
        misc_y_percent = int(globals["render"]["val"]["miscPosY"])
        
        # Position centrale
        center_x = bg_width / 2
        center_y = bg_height / 2
        
        # Ajustement basé sur le pourcentage
        x = center_x + (bg_width * misc_x_percent / 100)
        y = center_y + (bg_height * misc_y_percent / 100)
        
        # Ajustement pour centrer le misc (anchor="center")
        paste_x = int(x - misc_width / 2)
        paste_y = int(y - misc_height / 2)
        
        print(f"Misc position %: ({misc_x_percent}, {misc_y_percent})")
        print(f"Final misc paste position: ({paste_x}, {paste_y})")
        
        # Extraire le masque alpha et coller
        alpha_mask = misc.split()[3]
        background.paste(misc, (paste_x, paste_y), alpha_mask)


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

    def apply_crt_effect(self, background: Image.Image) -> None:
        """Applique l'effet CRT si activé"""
        if not globals["render"]["val"]["crt"]:
            return
        
        print("Applying CRT effect")
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
        """Nettoie les fichiers temporaires de manière plus agressive"""
        # D'abord nettoyer les fichiers spécifiques
        temp_char = get_temp_file("char")
        temp_cli = get_temp_file("char-cli")
        temp_conv = get_temp_file("char-converted")
        specific_files = [temp_char, temp_cli, temp_conv] + self.temp_files
        
        for temp_file in specific_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception as e:
                print(f"Warning: Could not remove temporary file {temp_file}: {e}")

        # Ensuite, nettoyer tous les fichiers du dossier tmp qui correspondent au suffixe unique
        if self.tmp_dir and os.path.exists(self.tmp_dir):
            suffix = globals.get("temp_suffix", "")
            if suffix:
                for file in os.listdir(self.tmp_dir):
                    if suffix in file:
                        try:
                            os.remove(os.path.join(self.tmp_dir, file))
                        except Exception as e:
                            print(f"Warning: Could not remove temporary file {file}: {e}")


def outputPicture(cli: bool = False) -> None:
    temp_files = []
    try:
        # Demander le chemin de sauvegarde uniquement une fois au début en mode GUI
        output_path = None
        if not cli:
            from tkinter import filedialog
            path_save = filedialog.asksaveasfilename(
                initialdir=os.getcwd(),
                title="Select file",
                defaultextension=".png",
                initialfile="vaporwaved.png"
            )
            if not path_save:
                print("Save cancelled by user")
                return
            globals["render"]["output"] = path_save
            output_path = path_save
        else:
            output_path = globals["render"].get("output")

        if not output_path:
            raise ValueError("No output path specified")

        # Créer le dossier de sortie si nécessaire
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Charger et préparer le background
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
        
        # Coller les éléments dans le bon ordre selon misc_above_character
        if not globals.get("misc_above_character", False):
            # Misc en dessous du character
            if misc is not None:
                # Utiliser la même logique de positionnement que le GUI
                bg_width, bg_height = background.size
                misc_width, misc_height = misc.size
                
                center_x = bg_width / 2
                center_y = bg_height / 2
                
                misc_x_percent = int(globals["render"]["val"]["miscPosX"])
                misc_y_percent = int(globals["render"]["val"]["miscPosY"])
                
                x = center_x + (bg_width * misc_x_percent / 100)
                y = center_y + (bg_height * misc_y_percent / 100)
                
                misc_x = int(x - misc_width / 2)
                misc_y = int(y - misc_height / 2)
                
                print(f"Pasting misc at ({misc_x}, {misc_y}) with size {misc.size}")
                alpha_mask = misc.split()[3]
                background.paste(misc, (misc_x, misc_y), alpha_mask)
                
            if character is not None:
                # Utiliser la même logique de positionnement que le GUI
                bg_width, bg_height = background.size
                char_width, char_height = character.size
                
                center_x = bg_width / 2
                center_y = bg_height / 2
                
                char_x_percent = int(globals["render"]["val"]["characterXpos"])
                char_y_percent = int(globals["render"]["val"]["characterYpos"])
                
                x = center_x + (bg_width * char_x_percent / 100)
                y = center_y + (bg_height * char_y_percent / 100)
                
                char_x = int(x - char_width / 2)
                char_y = int(y - char_height / 2)
                
                print(f"Pasting character at ({char_x}, {char_y}) with size {character.size}")
                alpha_mask = character.split()[3]
                background.paste(character, (char_x, char_y), alpha_mask)
        else:
            # Character en dessous du misc
            if character is not None:
                # Utiliser la même logique de positionnement que le GUI
                bg_width, bg_height = background.size
                char_width, char_height = character.size
                
                center_x = bg_width / 2
                center_y = bg_height / 2
                
                char_x_percent = int(globals["render"]["val"]["characterXpos"])
                char_y_percent = int(globals["render"]["val"]["characterYpos"])
                
                x = center_x + (bg_width * char_x_percent / 100)
                y = center_y + (bg_height * char_y_percent / 100)
                
                char_x = int(x - char_width / 2)
                char_y = int(y - char_height / 2)
                
                print(f"Pasting character at ({char_x}, {char_y}) with size {character.size}")
                alpha_mask = character.split()[3]
                background.paste(character, (char_x, char_y), alpha_mask)
                
            if misc is not None:
                # Utiliser la même logique de positionnement que le GUI
                bg_width, bg_height = background.size
                misc_width, misc_height = misc.size
                
                center_x = bg_width / 2
                center_y = bg_height / 2
                
                misc_x_percent = int(globals["render"]["val"]["miscPosX"])
                misc_y_percent = int(globals["render"]["val"]["miscPosY"])
                
                x = center_x + (bg_width * misc_x_percent / 100)
                y = center_y + (bg_height * misc_y_percent / 100)
                
                misc_x = int(x - misc_width / 2)
                misc_y = int(y - misc_height / 2)
                
                print(f"Pasting misc at ({misc_x}, {misc_y}) with size {misc.size}")
                alpha_mask = misc.split()[3]
                background.paste(misc, (misc_x, misc_y), alpha_mask)
        
        # Effet CRT
        if globals["render"]["val"].get("crt", False):
            print("Applying CRT effect")
            crt = Image.open(path_finder("picts/crt/crt.png"))
            if crt.mode != 'RGBA':
                crt = crt.convert('RGBA')
            alpha_mask = crt.split()[3]
            background.paste(crt, (0, 0), alpha_mask)
        
        # Sauvegarder
        print(f"Saving to {output_path}")
        save_as_png(background, output_path)
        
    except Exception as e:
        print(f"Error in outputPicture: {str(e)}")
        raise
    finally:
        # Nettoyage des fichiers temporaires
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception as e:
                print(f"Warning: Could not remove temporary file {temp_file}: {e}")
