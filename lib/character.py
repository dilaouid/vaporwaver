import os
from data import globals, get_temp_file
from PIL import Image
from glitch_this import ImageGlitcher
import cv2
import numpy as np

def prepareGradientImage(image):
    try:
        # Convertir en OpenCV pour appliquer le gradient
        if isinstance(image, Image.Image):
            # Sauvegarder temporairement pour la conversion
            temp_path = get_temp_file("temp-gradient-input")
            image.save(temp_path, 'PNG')
            original = cv2.imread(temp_path, cv2.IMREAD_UNCHANGED)
            # Supprimer le fichier temporaire
            if os.path.exists(temp_path):
                os.remove(temp_path)
        else:
            # Si un chemin est fourni directement
            character_path = globals["render"]["val"].get("characterPath") or globals["render"].get("characterPath")
            original = cv2.imread(character_path, cv2.IMREAD_UNCHANGED)

        if original is None:
            raise ValueError("Impossible de lire l'image du personnage pour le gradient.")

        # S'assurer que l'image a un canal alpha
        if original.shape[2] < 4:
            alpha = 255 * np.ones((original.shape[0], original.shape[1], 1), dtype=original.dtype)
            original = np.concatenate((original, alpha), axis=2)

        # Préserver le canal alpha original
        alpha_channel = original[:, :, 3].copy()

        gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        colored = cv2.applyColorMap(gray, getattr(cv2, "COLORMAP_" + globals["render"]["val"]["characterGradient"].upper()))
        colored = cv2.cvtColor(colored, cv2.COLOR_BGR2BGRA)

        # Restaurer le canal alpha original
        colored[:, :, 3] = alpha_channel

        # Convertir en PIL Image
        return Image.fromarray(colored)

    except Exception as e:
        print(f"Erreur lors de la préparation du gradient: {e}")
        # En cas d'échec, retourner l'image originale
        return image

def applyGlitchEffect(image):
    try:
        glitcher = ImageGlitcher()

        # Préserver le canal alpha
        if image.mode == 'RGBA':
            alpha = image.split()[-1]
            image_rgb = image.convert('RGB')

            glitched_rgb = glitcher.glitch_image(
                image_rgb, 
                color_offset=True, 
                glitch_amount=float(globals["render"]["val"]["characterGlitch"]), 
                seed=int(globals["render"]["val"]["characterGlitchSeed"])
            )

            glitched_image = glitched_rgb.convert('RGBA')
            glitched_image.putalpha(alpha)
            return glitched_image
        else:
            # Pour les images sans alpha
            glitched_image = glitcher.glitch_image(
                image, 
                color_offset=True, 
                glitch_amount=float(globals["render"]["val"]["characterGlitch"]), 
                seed=int(globals["render"]["val"]["characterGlitchSeed"])
            )
            return glitched_image.convert('RGBA')

    except Exception as e:
        print(f"Erreur lors de l'application du glitch: {e}")
        return image