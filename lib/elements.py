import os
from PIL import Image, ImageTk
import cv2
import numpy as np
from data import globals, get_temp_file
from glitch_this import ImageGlitcher
from .image_processor import CanvasElement, ImageProcessor

class Character(CanvasElement):
    def __init__(self, canvas, container_id):
        super().__init__(canvas, container_id)
        self.glitcher = ImageGlitcher()
        self.path_key = "characterPath"
        self.scale_key = "characterScale"
        self.rotate_key = "characterRotation"
        self.image_key = "gcChar"

    def apply_gradient(self, image: Image.Image, gradient_name: str) -> Image.Image:
        if gradient_name == "none":
            return image

        image = ImageProcessor.ensure_rgba(image)
        arr = np.array(image)
        alpha = arr[:, :, 3].copy()

        gray = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
        colored = cv2.applyColorMap(gray, getattr(cv2, f"COLORMAP_{gradient_name.upper()}"))
        colored = cv2.cvtColor(colored, cv2.COLOR_BGR2BGRA)
        colored[:, :, 3] = alpha

        return Image.fromarray(colored)

    def apply_glitch(self, image: Image.Image, amount: float, seed: int) -> Image.Image:
        image = ImageProcessor.ensure_rgba(image)
        alpha = image.split()[-1]

        glitched = self.glitcher.glitch_image(
            image.convert('RGB'),
            color_offset=True,
            glitch_amount=amount,
            seed=seed
        )

        glitched = glitched.convert('RGBA')
        glitched.putalpha(alpha)
        return glitched

    def apply_transforms(self) -> None:
        """Applique toutes les transformations à l'élément et sauvegarde le résultat dans un fichier tmp unique."""
        if not hasattr(self, 'canvas') or not self.canvas:
            return

        try:
            # Utiliser le fichier "char" comme base convertie (si présent) sinon partir du chemin d'origine
            temp_char = get_temp_file("char")
            # On ne lit pas le fichier existant, on le recrée systématiquement
            if os.path.exists(temp_char):
                os.remove(temp_char)

            # Charger l'image de base directement depuis le fichier temporaire "char"
            image = Image.open(temp_char) if os.path.exists(temp_char) else Image.open(globals["render"]["characterPath"])

            # Appliquer le gradient si nécessaire
            if globals["render"]["val"]["characterGradient"] != "none":
                image = self.apply_gradient(image, globals["render"]["val"]["characterGradient"])

            # Appliquer scale et rotation
            image = self.transform_image(
                image,
                int(globals["render"]["val"]["characterScale"]),
                int(globals["render"]["val"]["characterRotation"])
            )

            # Appliquer le glitch si nécessaire
            if float(globals["render"]["val"]["characterGlitch"]) != 0.1:
                image = self.apply_glitch(
                    image,
                    float(globals["render"]["val"]["characterGlitch"]),
                    int(globals["render"]["val"]["characterGlitchSeed"])
                )

            # Sauvegarder le résultat dans "char"
            image.save(temp_char, "PNG")
            globals["gcChar"] = ImageTk.PhotoImage(image)
            self.canvas.itemconfig(
                self.container_id,
                image=globals["gcChar"],
                anchor="center"
            )
        except Exception as e:
            print(f"Error applying transforms: {str(e)}")


class Misc(CanvasElement):
    def __init__(self, canvas, container_id):
        super().__init__(canvas, container_id)
        self.path_key = "misc"
        self.scale_key = "miscScale"
        self.rotate_key = "miscRotate"
        self.image_key = "gcMisc"
    
    def set_layer_priority(self, above_character: bool, character_id: str, background_id: str):
        """Set misc layer priority relative to character"""
        if above_character:
            self.canvas.lift(self.container_id)
        else:
            self.canvas.lift(self.container_id, background_id)
            self.canvas.lower(self.container_id, character_id)