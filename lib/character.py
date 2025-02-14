import os
from data import globals, gui, path_finder, get_temp_file
from PIL import Image, ImageTk, ImageFilter
from glitch_this import ImageGlitcher
import cv2
import numpy as np

rotateCharacterBool = False

def resizeCharacter(image):
    return image.resize((
        int(image.size[0] * int(globals["render"]["val"]["characterScale"]) / 100),
        int(image.size[1] * int(globals["render"]["val"]["characterScale"]) / 100)
    ), Image.LANCZOS)

def min_rotateCharacter(image):
    return image.rotate(globals["render"]["val"]["characterRotation"], expand=True)

def glitchingCLI(image) -> Image:
    glitcher = ImageGlitcher()
    try:
        if image.mode == 'RGBA':
            alpha = image.split()[-1]
            image_rgb = image.convert('RGB')
            print("Glitching (RGBA -> RGB) with glitch_amount:", globals["render"]["val"]["characterGlitch"])
            glitched_rgb = glitcher.glitch_image(
                image_rgb, 
                color_offset=True, 
                glitch_amount=float(globals["render"]["val"]["characterGlitch"]), 
                seed=int(globals["render"]["val"]["characterGlitchSeed"])
            )
            glitched_image = glitched_rgb.convert('RGBA')
            glitched_image.putalpha(alpha)
        else:
            print("Glitching non-RGBA image with glitch_amount:", globals["render"]["val"]["characterGlitch"])
            glitched_image = glitcher.glitch_image(
                image, 
                color_offset=True, 
                glitch_amount=float(globals["render"]["val"]["characterGlitch"]), 
                seed=int(globals["render"]["val"]["characterGlitchSeed"])
            )
        temp_cli = get_temp_file("char-cli")
        print("Saving glitched image to", temp_cli)

        glitched_image.save(temp_cli, 'PNG')
        return glitched_image
    except Exception as e:
        print(f"Error in glitchingCLI: {e}")
        return image

def glitching(image) -> Image:
    glitcher = ImageGlitcher()
    temp_char = get_temp_file("char")
    glitched_image = glitcher.glitch_image(
        image, 
        color_offset=True, 
        glitch_amount=float(globals["render"]["val"]["characterGlitch"]), 
        seed=int(globals["render"]["val"]["characterGlitchSeed"])
    )
    glitched_image.save(temp_char)
    return ImageTk.PhotoImage(glitched_image)

def applygradient(path: str = './tmp/char-cli.png'):
    # Utiliser le chemin défini dans 'val' si présent, sinon utiliser celui dans 'render'
    character_path = globals["render"]["val"].get("characterPath") or globals["render"].get("characterPath")
    if not character_path:
        raise ValueError("Le chemin de l'image du personnage n'est pas défini.")
    original = cv2.imread(character_path, cv2.IMREAD_UNCHANGED)
    if original is None:
        raise ValueError("Impossible de lire l'image du personnage.")
    if original.shape[2] < 4:
        alpha = 255 * np.ones((original.shape[0], original.shape[1], 1), dtype=original.dtype)
        original = np.concatenate((original, alpha), axis=2)
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    colored = cv2.applyColorMap(gray, getattr(cv2, "COLORMAP_" + globals["render"]["val"]["characterGradient"].upper()))
    colored = cv2.cvtColor(colored, cv2.COLOR_BGR2BGRA)
    colored[:, :, 3] = original[:, :, 3]
    image = Image.fromarray(colored)
    image = resizeCharacter(image)
    image = min_rotateCharacter(image)
    image.save(path)
    return image



def gradientCharacter(gradient: str):
    globals["render"]["val"]["characterGradient"] = gradient
    temp_file = get_temp_file("char-cli")  # Utilisation d'un nom unique pour le gradient
    if globals["render"]["val"]["characterGradient"] == "none":
        image: Image = Image.open(globals["render"]["characterPath"])
        image = resizeCharacter(image)
        if rotateCharacterBool:
            image = min_rotateCharacter(image)
        # Ici, on utilise un fichier temporaire dédié pour le mode "none"
        temp_char = get_temp_file("char")
        image.save(temp_char)
        globals["gcChar"] = ImageTk.PhotoImage(image)
        if globals["render"]["val"]["characterGlitch"] != .1:
            globals["gcChar"] = glitching(Image.open(temp_char))
        gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])
        return image

    # Pour un gradient autre que "none"
    globals["gcChar"] = None
    gui["frame"]["canvas"].character = None
    # Appliquer le gradient et enregistrer dans temp_file
    image = applygradient(temp_file)
    globals["gcChar"] = ImageTk.PhotoImage(image)
    gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])

    # Si un effet de glitch est demandé, l'appliquer sur le même fichier temporaire
    if globals["render"]["val"]["characterGlitch"] != .1:
        globals["gcChar"] = glitching(Image.open(temp_file))
        gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])
    return image

def resizeAndUpdate() -> Image:
    image: Image = Image.open(globals["render"]["characterPath"])
    if globals["render"]["val"]["characterGradient"] != "none":
        image = applygradient(get_temp_file("char-cli"))
    image = resizeCharacter(image)
    if rotateCharacterBool:
        image = min_rotateCharacter(image)
    temp_char = get_temp_file("char")
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'tmp')):
        os.makedirs(os.path.join(os.path.dirname(__file__), 'tmp'))
    image.save(temp_char)
    return Image.open(temp_char)

def moveCharacter(axis, value) -> None:
    if globals["character"] is None:
        return
    globals["render"]["val"][axis] = value
    # change the position of the character according to % of the canvas
    gui["frame"]["canvas"].coords(globals["character"], gui["frame"]["canvas"].winfo_width() * int(globals["render"]["val"]["characterXpos"]) / 100, gui["frame"]["canvas"].winfo_height() * int(globals["render"]["val"]["characterYpos"]) / 100)

def scaleCharacter(axis, value) -> None:
    if globals["character"] is None:
        return
    globals["render"]["val"]["characterScale"] = value
    image: Image = resizeAndUpdate()
    globals["gcChar"] = glitching(image)
    gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])

def glitchCharacter(axis, value) -> None:
    if globals["character"] is None:
        return
    globals["render"]["val"][axis] = value
    image = resizeAndUpdate()
    globals["gcChar"] = glitching(image)
    gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])

# rotate the character by a given angle (in degrees) keeping the transparency
def rotateCharacter(axis: str, value: int) -> None:
    global rotateCharacterBool
    rotateCharacterBool = True
    if globals["character"] is None:
        return
    globals["render"]["val"][axis] = int(value)
    image: Image = resizeAndUpdate()
    # image = image.rotate(int(globals["render"]["val"]["characterRotation"]), expand=True)
    image.save('./tmp/char.png')
    globals["gcChar"] = ImageTk.PhotoImage(image)
    gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])
    rotateCharacterBool = False

def glowCharacter(color: str) -> None:
    # apply a contour around transparent pixels of the character with keep alpha
    if globals["character"] is None:
        return
    image = resizeAndUpdate()
    image = image.filter(ImageFilter.CONTOUR)
    globals["gcChar"] = glitching(image)
    gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])