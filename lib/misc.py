import os

from data import globals, gui, path_finder
from PIL import Image, ImageTk
from gui.error import error_dialog
import tkinter as tk

def toggle_misc_priority(value: bool) -> None:
    """Change la priorité d'affichage du misc (devant/derrière le character)"""
    try:
        if globals["misc_container"] is None or globals["character"] is None:
            return
            
        globals["misc_above_character"] = value
        
        # Si le misc doit être au-dessus du character
        if value:
            gui["frame"]["canvas"].lift(globals["misc_container"])
        else:
            # Sinon, le mettre derrière le character mais devant le background
            gui["frame"]["canvas"].lift(globals["misc_container"], globals["background_container"])
            gui["frame"]["canvas"].lower(globals["misc_container"], globals["character"])
            
    except Exception as e:
        error_dialog("Error", f"Failed to change misc priority: {str(e)}")


def changeMisc(filename: str) -> None:
    """Change le misc actuel avec les valeurs préservées ou par défaut"""
    try:
        misc_path = path_finder('picts/miscs/' + filename + '.png')
        if not os.path.exists(misc_path):
            error_dialog("Error", f"Misc file not found: {misc_path}")
            return
            
        globals["render"]["misc"] = misc_path
        
        # Charger et préparer l'image
        image = Image.open(misc_path)
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # S'assurer que les valeurs par défaut sont présentes
        if "miscScale" not in globals["render"]["val"]:
            globals["render"]["val"]["miscScale"] = 100
            globals["render"]["val"]["miscPosX"] = 0
            globals["render"]["val"]["miscPosY"] = 0
            globals["render"]["val"]["miscRotate"] = 0
        
        # Récupérer les valeurs actuelles
        scale = int(globals["render"]["val"]["miscScale"])
        rotate = int(globals["render"]["val"]["miscRotate"])
        
        # Appliquer le scale
        new_width = int(image.size[0] * scale / 100)
        new_height = int(image.size[1] * scale / 100)
        if new_width > 0 and new_height > 0:
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Appliquer la rotation
        image = image.rotate(rotate, expand=True)
        
        # Convertir en PhotoImage et mettre à jour l'affichage
        globals["gcMisc"] = ImageTk.PhotoImage(image)
        
        # Get canvas dimensions for centering
        canvas_width = gui["frame"]["canvas"].winfo_width()
        canvas_height = gui["frame"]["canvas"].winfo_height()
        
        # Position calculations with the current values
        x = float(canvas_width) * float(globals["render"]["val"]["miscPosX"]) / 100.0
        y = float(canvas_height) * float(globals["render"]["val"]["miscPosY"]) / 100.0
        
        # Update the image and ensure it's centered
        gui["frame"]["canvas"].coords(globals["misc_container"], x, y)
        gui["frame"]["canvas"].itemconfig(
            globals["misc_container"],
            image=globals["gcMisc"],
            anchor="center"
        )
        
        # Appliquer l'ordre des calques correct
        if globals.get("misc_above_character", False):
            gui["frame"]["canvas"].lift(globals["misc_container"])
        else:
            gui["frame"]["canvas"].lift(globals["misc_container"], globals["background_container"])
            gui["frame"]["canvas"].lower(globals["misc_container"], globals["character"])
                
    except Exception as e:
        error_dialog("Error", f"Failed to change misc: {str(e)}")


def moveMisc(axis, value) -> None:
    try:
        if globals["misc_container"] is None:
            return
        globals["render"]["val"][axis] = value
        canvas_width = gui["frame"]["canvas"].winfo_width()
        canvas_height = gui["frame"]["canvas"].winfo_height()
        x = float(canvas_width) * float(globals["render"]["val"]["miscPosX"]) / 100.0
        y = float(canvas_height) * float(globals["render"]["val"]["miscPosY"]) / 100.0
        gui["frame"]["canvas"].coords(globals["misc_container"], x, y)
        gui["frame"]["canvas"].itemconfig(globals["misc_container"], anchor="center")
    except Exception as e:
        error_dialog("Error", f"Failed to move misc: {str(e)}")

def scaleMisc(axis, value) -> None:
    try:
        if globals["misc_container"] is None:
            return
        globals["render"]["val"]["miscScale"] = value
        image = Image.open(globals["render"]["misc"])
        image = image.resize((
            int(image.size[0] * int(globals["render"]["val"]["miscScale"]) / 100),
            int(image.size[1] * int(globals["render"]["val"]["miscScale"]) / 100)
        ), Image.Resampling.LANCZOS)
        image = image.rotate(int(globals["render"]["val"]["miscRotate"]), expand=True)
        globals["gcMisc"] = ImageTk.PhotoImage(image)
        gui["frame"]["canvas"].itemconfig(globals["misc_container"], image=globals["gcMisc"], anchor="center")
    except Exception as e:
        error_dialog("Error", f"Failed to scale misc: {str(e)}")

def rotateMisc(axis, value) -> None:
    try:
        if globals["misc_container"] is None:
            return
            
        globals["render"]["val"]["miscRotate"] = int(value)
        image = Image.open(globals["render"]["misc"])
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # Récupérer et convertir les valeurs en nombres
        scale = int(globals["render"]["val"].get("miscScale", 100))
        rotate = int(globals["render"]["val"]["miscRotate"])
        
        # Redimensionner si nécessaire
        new_width = int(image.size[0] * scale / 100)
        new_height = int(image.size[1] * scale / 100)
        
        if new_width > 0 and new_height > 0:
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
        # Appliquer la rotation
        image = image.rotate(rotate, expand=True)
        
        # Mettre à jour l'affichage
        globals["gcMisc"] = ImageTk.PhotoImage(image)
        gui["frame"]["canvas"].itemconfig(
            globals["misc_container"],
            image=globals["gcMisc"],
            anchor="center"
        )
            
    except Exception as e:
        error_dialog("Error", f"Failed to rotate misc: {str(e)}")