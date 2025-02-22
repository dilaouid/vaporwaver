import os
from data import globals, gui, get_temp_file
from PIL import Image, ImageTk, ImageFilter
from glitch_this import ImageGlitcher
import cv2
import numpy as np

def get_centered_position(container_width: int, container_height: int, x_percent: int, y_percent: int) -> tuple:
    """
    Calculate centered position for an element
    
    Args:
        container_width: Width of container (canvas/background)
        container_height: Height of container (canvas/background)
        x_percent: X position percentage (-150 to 150)
        y_percent: Y position percentage (-150 to 150)
    
    Returns:
        tuple: (x, y) coordinates for centered position
    """
    # Calculate center of container
    container_center_x = container_width / 2
    container_center_y = container_height / 2
    
    # Calculate offset from center based on percentage
    offset_x = container_width * x_percent / 100
    offset_y = container_height * y_percent / 100
    
    # Return position relative to center
    return (container_center_x + offset_x, container_center_y + offset_y)

def moveCharacter(axis, value) -> None:
    if globals["character"] is None:
        return
        
    globals["render"]["val"][axis] = value
    
    # Always ensure center anchoring
    gui["frame"]["canvas"].itemconfigure(globals["character"], anchor="center")
    
    # Get canvas dimensions
    canvas_width = gui["frame"]["canvas"].winfo_width()
    canvas_height = gui["frame"]["canvas"].winfo_height()
    
    # Get centered position
    x, y = get_centered_position(
        canvas_width,
        canvas_height,
        int(globals["render"]["val"]["characterXpos"]),
        int(globals["render"]["val"]["characterYpos"])
    )
    
    # Update position
    gui["frame"]["canvas"].coords(globals["character"], x, y)

def resizeCharacter(image):
    # Assurer que l'image est en mode RGBA
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    return image.resize((
        int(image.size[0] * int(globals["render"]["val"]["characterScale"]) / 100),
        int(image.size[1] * int(globals["render"]["val"]["characterScale"]) / 100)
    ), Image.Resampling.LANCZOS)

def min_rotateCharacter(image):
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    rotation_angle = int(globals["render"]["val"]["characterRotation"])
    if rotation_angle == 0:
        return image

    return image.rotate(
        rotation_angle,
        expand=True,
        resample=Image.Resampling.BICUBIC
    )

# Application optimisée de toutes les transformations
def applyAllTransformations():
    try:
        original_image = Image.open(globals["render"]["characterPath"])
        if original_image.mode != 'RGBA':
            original_image = original_image.convert('RGBA')

        # Appliquer le gradient si nécessaire
        if globals["render"]["val"]["characterGradient"] != "none":
            # Préparer le gradient sans redimensionner ni faire la rotation
            image = prepareGradientImage(original_image)
        else:
            image = original_image.copy()

        # Redimensionner
        image = resizeCharacter(image)

        # Rotation
        if globals["render"]["val"]["characterRotation"] != 0:
            image = min_rotateCharacter(image)

        # Glitch si nécessaire (mais sans encore créer la PhotoImage)
        if globals["render"]["val"]["characterGlitch"] != .1:
            image = applyGlitchEffect(image)

        # Sauvegarder l'image transformée
        tmp_dir = os.path.dirname(get_temp_file("char"))
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir, exist_ok=True)

        temp_char = get_temp_file("char")
        image.save(temp_char, 'PNG')

        # Créer la PhotoImage finale pour l'affichage
        globals["gcChar"] = ImageTk.PhotoImage(image)

        # Mettre à jour l'affichage
        if globals["character"] is not None:
            gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])

        return image

    except Exception as e:
        print(f"Erreur lors de l'application des transformations: {e}")
        return None

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
            # Pour les images sans alpha (rare dans ce contexte)
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

def glitchingCLI(image) -> Image:
    return applyGlitchEffect(image)

def glitching(image) -> Image:
    # Cette fonction est maintenant simplifiée pour retourner directement un PhotoImage
    temp_char = get_temp_file("char")
    try:
        glitched_image = applyGlitchEffect(image)
        glitched_image.save(temp_char, 'PNG')
        return ImageTk.PhotoImage(glitched_image)
    except Exception as e:
        print(f"Error in glitching: {e}")
        image.save(temp_char, 'PNG')
        return ImageTk.PhotoImage(image)

def applygradient(path: str = './tmp/char-cli.png'):
    image = prepareGradientImage(None)  # Utilise le chemin stocké dans globals
    
    # Appliquer les transformations supplémentaires
    image = resizeCharacter(image)
    if globals["render"]["val"]["characterRotation"] != 0:
        image = min_rotateCharacter(image)

    # Vérifier que le dossier tmp existe
    tmp_dir = os.path.dirname(path)
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir, exist_ok=True)

    image.save(path, 'PNG')
    return image

def gradientCharacter(gradient: str):
    # Mettre à jour la valeur du gradient
    globals["render"]["val"]["characterGradient"] = gradient
    
    # Réappliquer toutes les transformations avec le nouveau gradient
    applyAllTransformations()

def resizeAndUpdate() -> Image:
    # Cette fonction est maintenant remplacée par le pipeline complet
    return applyAllTransformations()

def scaleCharacter(axis, value) -> None:
    if globals["character"] is None:
        return
    globals["render"]["val"]["characterScale"] = value
    applyAllTransformations()

def glitchCharacter(axis, value) -> None:
    if globals["character"] is None:
        return
    globals["render"]["val"][axis] = value
    applyAllTransformations()

def rotateCharacter(axis: str, value: int) -> None:
    if globals["character"] is None:
        return
    globals["render"]["val"][axis] = int(value)
    applyAllTransformations()