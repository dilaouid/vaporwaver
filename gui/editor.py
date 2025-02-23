# editor.py
import os
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
from typing import Union, Optional
from PIL import ImageTk

from data import globals, gui, get_temp_file, path_finder
from lib.elements import Character, Misc
from lib.image_handler import load_and_convert_image, save_temp_png
from lib.output import outputPicture

class EditorGUI:
    def __init__(self):
        self.character_handler: Optional[Character] = None
        self.misc_handler: Optional[Misc] = None

    def setup_gui_frame(self) -> None:
        """Configure la fenêtre principale et ses frames"""
        self.setup_left_frame()
        self.setup_right_frame()

    def setup_left_frame(self) -> None:
        """Configure le frame gauche avec le canvas et les contrôles"""
        gui["frame"]["left"] = tk.Frame(gui["frame"]["window"])
        gui["frame"]["left"].configure(bg="#242424", bd=0, border=1, relief=tk.FLAT, width=560, height=595)
        gui["frame"]["left"].pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)

        self.setup_preview_canvas()
        self.setup_bottom_controls()

    def setup_preview_canvas(self) -> None:
        """Configure le canvas de prévisualisation"""
        gui["frame"]["preview"] = tk.Frame(gui["frame"]["left"], width=460, height=595)
        gui["frame"]["preview"].place(x=50, y=10)

        gui["frame"]["canvas"] = tk.Canvas(gui["frame"]["preview"], width=460, height=595, bg="grey")
        gui["frame"]["canvas"].pack(fill=tk.BOTH, anchor=tk.NW)

        # Background
        preview_bg = tk.PhotoImage(file=globals["render"]["background"])
        gui["frame"]["preview"].preview_bg = preview_bg
        globals["background_container"] = gui["frame"]["canvas"].create_image((0, 0), 
            image=gui["frame"]["preview"].preview_bg, anchor=tk.NW)

        # Misc
        misc = tk.PhotoImage(file=globals["render"]["misc"])
        gui["frame"]["preview"].misc = misc
        globals["misc_container"] = gui["frame"]["canvas"].create_image(
            (gui["frame"]["canvas"].winfo_width() // 2,
            gui["frame"]["canvas"].winfo_height() // 2),
            image=gui["frame"]["preview"].misc,
            anchor=tk.CENTER
        )
                
        self.misc_handler = Misc(gui["frame"]["canvas"], globals["misc_container"])

    def setup_bottom_controls(self) -> None:
        """Configure les boutons Import et Save"""
        import_button = tk.Button(gui["frame"]["left"], text="Import", command=self.import_character)
        import_button.place(x=50, y=555+60, width=300, height=30)

        gui["el"]["save_button"] = tk.Button(gui["frame"]["left"], text="Save", bg="blue", 
            fg="white", state=tk.DISABLED if globals["character"] is None else tk.NORMAL, 
            command=outputPicture)
        gui["el"]["save_button"].place(x=360, y=555+60, width=155, height=30)

        gui["el"]["warning_label"] = tk.Label(gui["frame"]["left"], 
            text="Warning: You need to import a character to start vaporwaving shits.", 
            bg="#242424", fg="red", font=("Helvetica", 10))
        gui["el"]["warning_label"].place(x=50, y=555+60+30, width=460, height=30)

    def setup_right_frame(self) -> None:
        """Configure le frame droit avec tous les contrôles"""
        gui["frame"]["right"] = tk.Frame(gui["frame"]["window"])
        gui["frame"]["right"].configure(bg="#303030", bd=0, border=1, relief=tk.FLAT)
        gui["frame"]["right"].pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        gui["frame"]["right"].place(relx=0.53, rely=0.05)

        self.setup_character_controls()
        self.add_separator()
        self.setup_misc_controls()
        self.add_separator(row=9)
        self.setup_crt_control()

        # Désactiver les contrôles si pas de character
        if globals["character"] is None:
            self.disable_controls()

    def setup_character_controls(self) -> None:
        """Configure les contrôles du character"""
        # Position X/Y
        gui["el"]["char"]["posX"] = self.create_scale_element(-150, 150, "Character X Position:", 0, 0,
            "characterXpos", self.move_character)
        gui["el"]["char"]["posY"] = self.create_scale_element(-150, 150, "Character Y Position:", 0, 1,
            "characterYpos", self.move_character)

        # Scale et effets
        gui["el"]["char"]["scale"] = self.create_scale_element(1, 200, "Character Scale:", 0, 2,
            "characterScale", self.scale_character)
        gui["el"]["char"]["glitch"] = self.create_scale_element(.1, 10, "Character Glitch (.1-10):", 0, 3,
            "characterGlitch", self.glitch_character, .1)
        gui["el"]["char"]["rotate"] = self.create_scale_element(-360, 360, "Character Rotation:", 2, 2,
            "characterRotation", self.rotate_character)
        gui["el"]["char"]["glitchSeed"] = self.create_scale_element(0, 100, "Character Glitch Seed:", 2, 3,
            "characterGlitchSeed", self.glitch_character)

        # Gradient
        self.setup_gradient_control()

    def setup_gradient_control(self) -> None:
        """Configure le contrôle de gradient"""
        gradient_label = tk.Label(gui["frame"]["right"], text="Gradient", bg="#303030", fg="white")
        gradient_label.grid(row=2, column=0)
        gradient_var = tk.StringVar(gui["frame"]["right"])
        gradient_var.set("none")
        gui["el"]["char"]["gradients"] = tk.OptionMenu(gui["frame"]["right"], gradient_var, 
            *globals["gradients"], command=self.gradient_character)
        gui["el"]["char"]["gradients"].grid(row=3, column=0)

    def setup_misc_controls(self) -> None:
        """Configure les contrôles du misc"""
        self.setup_background_control()
        self.setup_misc_item_control()
        self.setup_misc_transform_controls()
        self.setup_misc_layer_control()

    def setup_background_control(self) -> None:
        """Configure le contrôle de background"""
        bglabel = tk.Label(gui["frame"]["right"], text="Background", bg="#303030", fg="white")
        bglabel.grid(row=5, column=0)
        bgvar = tk.StringVar(gui["frame"]["right"])
        bgvar.set(self.get_filename("background"))
        self.bg = tk.OptionMenu(gui["frame"]["right"], bgvar, *globals["backgrounds"], 
            command=self.change_background)
        self.bg.grid(row=6, column=0)

    def setup_misc_item_control(self) -> None:
        """Configure les contrôles du misc item"""
        msclabel = tk.Label(gui["frame"]["right"], text="Misc Item", bg="#303030", fg="white")
        msclabel.grid(row=5, column=1)
        mscvar = tk.StringVar(gui["frame"]["right"])
        mscvar.set("none")
        gui["el"]["misc"]["select"] = tk.OptionMenu(gui["frame"]["right"], mscvar, 
            *globals["miscs"], command=self.change_misc)
        gui["el"]["misc"]["select"].grid(row=6, column=1, pady=10)

    def setup_misc_transform_controls(self) -> None:
        """Configure les contrôles de transformation du misc"""
        gui["el"]["misc"]["posX"] = self.create_scale_element(-100, 100, "Misc X Position:", 5, 2,
            "miscPosX", self.move_misc)
        gui["el"]["misc"]["posY"] = self.create_scale_element(-100, 100, "Misc Y Position:", 5, 3,
            "miscPosY", self.move_misc)
        gui["el"]["misc"]["scale"] = self.create_scale_element(1, 200, "Misc Scale:", 7, 2,
            "miscScale", self.scale_misc)
        gui["el"]["misc"]["rotate"] = self.create_scale_element(-360, 360, "Misc Rotation:", 7, 3,
            "miscRotate", self.rotate_misc)

    def setup_misc_layer_control(self) -> None:
        """Configure le contrôle de layer du misc"""
        misc_layer_var = tk.BooleanVar()
        gui["el"]["misc"]["priority_checkbox"] = tk.Checkbutton(
            gui["frame"]["right"],
            text="Misc Above Character",
            variable=misc_layer_var,
            bg="#303030",
            fg="white",
            selectcolor="#303030",
            activebackground="#303030",
            activeforeground="white",
            highlightbackground="#303030",
            highlightcolor="#303030",
            highlightthickness=1,
            bd=0,
            command=lambda: self.toggle_misc_priority(misc_layer_var.get())
        )
        gui["el"]["misc"]["priority_checkbox"].grid(row=8, column=1, pady=5)

    def setup_crt_control(self) -> None:
        """Configure le contrôle CRT"""
        crt_effect = tk.BooleanVar()
        gui["el"]["crt"]["checkbox"] = tk.Checkbutton(
            gui["frame"]["right"],
            text="CRT Effect",
            variable=crt_effect,
            bg="#303030",
            fg="white",
            selectcolor="#303030",
            activebackground="#303030",
            activeforeground="white",
            highlightbackground="#303030",
            highlightcolor="#303030",
            highlightthickness=1,
            bd=0,
            command=lambda: self.apply_crt(crt_effect.get())
        )
        gui["el"]["crt"]["checkbox"].grid(row=10, column=0, padx=10, pady=10)

    def create_scale_element(self, _from: Union[int, float], _to: Union[int, float], 
            label_text: str, row: int, col: int, value: str, func, resolution=1) -> tk.Scale:
        """Crée un élément Scale avec son label"""
        label = tk.Label(gui["frame"]["right"], text=label_text, bg="#303030", fg="white")
        label.grid(row=row, column=col, padx=10)
        
        element = tk.Scale(
            gui["frame"]["right"],
            from_=_from,
            to=_to,
            orient=tk.HORIZONTAL,
            bg="#303030",
            fg="white",
            resolution=resolution,
            command=lambda x: func(value, x)
        )
        element.set(globals["render"]["val"][value])
        element.grid(row=row+1, column=col, padx=10, pady=10)
        return element

    def add_separator(self, row: int = 4) -> None:
        """Ajoute un séparateur horizontal"""
        separator = tk.Frame(gui["frame"]["right"], bg='white', width=200, height=1)
        separator.grid(row=row, column=0, columnspan=5, sticky=tk.EW, pady=10, padx=5)

    def disable_controls(self) -> None:
        """Désactive tous les contrôles sauf background"""
        for child in gui["frame"]["right"].winfo_children():
            if child not in [self.bg] and not isinstance(child, tk.Frame):  # Ne pas désactiver les séparateurs
                if isinstance(child, (tk.Scale, tk.Button, tk.Checkbutton, tk.OptionMenu)):
                    child.configure(state=tk.DISABLED)
                elif isinstance(child, tk.Label):
                    # Les labels n'ont pas besoin d'être désactivés
                    pass


    # Méthodes de gestion des événements
    def import_character(self) -> None:
        """Gère l'import d'un character"""
        filetypes = [
            ("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.webp;*.tiff;*.gif"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg;*.jpeg"),
            ("BMP files", "*.bmp"),
            ("WebP files", "*.webp"),
            ("TIFF files", "*.tiff"),
            ("GIF files", "*.gif")
        ]
        
        filepath = tkinter.filedialog.askopenfilename(title="Select character image", filetypes=filetypes)
        if not filepath:
            return
            
        try:
            image = load_and_convert_image(filepath)
            # Utiliser "char" comme nom de fichier temporaire
            temp_char = get_temp_file("char")
            save_temp_png(image, temp_char)
            
            globals["render"]["characterPath"] = filepath
            globals["render"]["val"]["characterPath"] = filepath
            
            globals["gcChar"] = tk.PhotoImage(file=temp_char)
            
            # Supprimer l'ancien fichier "char" s'il existe (il sera recréé ensuite)
            if os.path.exists(temp_char):
                os.remove(temp_char)
            
            if globals["character"] is None:
                globals["character"] = gui["frame"]["canvas"].create_image(
                    (gui["frame"]["canvas"].winfo_width() // 2,
                    gui["frame"]["canvas"].winfo_height() // 2),
                    image=globals["gcChar"],
                    anchor=tk.CENTER
                )
                self.character_handler = Character(gui["frame"]["canvas"], globals["character"])
            else:
                gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])
                
            gui["frame"]["canvas"].character = globals["gcChar"]
            
            self.activate_elements()
            self.reset_values()
            
        except Exception as e:
            tkinter.messagebox.showerror("Error", f"Failed to import image: {str(e)}")


    def move_character(self, axis: str, value: str) -> None:
        """Déplace le character"""
        if globals["character"] is None or self.character_handler is None:
            return
        globals["render"]["val"][axis] = value
        x = float(globals["render"]["val"]["characterXpos"])
        y = float(globals["render"]["val"]["characterYpos"])
        self.character_handler.update_position(x, y)


    def scale_character(self, axis: str, value: str) -> None:
        """Redimensionne le character"""
        if globals["character"] is None or self.character_handler is None:
            return
        globals["render"]["val"]["characterScale"] = value
        self.character_handler.apply_transforms()

    def rotate_character(self, axis: str, value: str) -> None:
        """Fait pivoter le character"""
        if globals["character"] is None or self.character_handler is None:
            return
        globals["render"]["val"][axis] = int(value)
        self.character_handler.apply_transforms()

    def glitch_character(self, axis: str, value: str) -> None:
        """Applique l'effet glitch au character"""
        if globals["character"] is None or self.character_handler is None:
            return
        globals["render"]["val"][axis] = value
        self.character_handler.apply_transforms()

    def gradient_character(self, gradient: str) -> None:
        """Applique le gradient au character"""
        if globals["character"] is None or self.character_handler is None:
            return
        globals["render"]["val"]["characterGradient"] = gradient
        self.character_handler.apply_transforms()

    def move_misc(self, axis: str, value: str) -> None:
        """Déplace le misc"""
        if globals["misc_container"] is None or self.misc_handler is None:
            return
        globals["render"]["val"][axis] = value
        self.misc_handler.update_position(
            float(globals["render"]["val"]["miscPosX"]),
            float(globals["render"]["val"]["miscPosY"])
        )

    def scale_misc(self, axis: str, value: str) -> None:
        """Redimensionne le misc"""
        if globals["misc_container"] is None or self.misc_handler is None:
            return
        globals["render"]["val"]["miscScale"] = value
        self.misc_handler.apply_transforms()

    def rotate_misc(self, axis: str, value: str) -> None:
        """Fait pivoter le misc"""
        if globals["misc_container"] is None or self.misc_handler is None:
            return
        globals["render"]["val"]["miscRotate"] = int(value)
        self.misc_handler.apply_transforms()

    def toggle_misc_priority(self, value: bool) -> None:
        """Change la priorité d'affichage du misc"""
        if globals["misc_container"] is None or self.misc_handler is None:
            return
        globals["misc_above_character"] = value
        self.misc_handler.set_layer_priority(
            value,
            globals["character"],
            globals["background_container"]
        )

    def change_background(self, name: str) -> None:
        """Change l'image de fond"""
        bg_path = path_finder(f'picts/backgrounds/{name}.png')
        if not os.path.exists(bg_path):
            tkinter.messagebox.showerror("Error", f"Background file not found: {bg_path}")
            return
        
        globals["render"]["background"] = bg_path
        preview_bg = tk.PhotoImage(file=bg_path)
        gui["frame"]["preview"].preview_bg = preview_bg
        gui["frame"]["canvas"].itemconfig(globals["background_container"], image=preview_bg)

    def change_misc(self, name: str) -> None:
        """Change l'élément misc"""
        misc_path = path_finder(f'picts/miscs/{name}.png')
        if not os.path.exists(misc_path):
            tkinter.messagebox.showerror("Error", f"Misc file not found: {misc_path}")
            return

        globals["render"]["misc"] = misc_path
        try:
            image = load_and_convert_image(misc_path)
            image = self.misc_handler.transform_image(
                image,
                int(globals["render"]["val"].get("miscScale", 100)),
                int(globals["render"]["val"].get("miscRotate", 0))
            )
            
            globals["gcMisc"] = ImageTk.PhotoImage(image)
            # Mettre à jour l'image ET forcer l'ancrage à CENTER
            gui["frame"]["canvas"].itemconfig(
                globals["misc_container"],
                image=globals["gcMisc"],
                anchor="center"
            )

            canvas_width = gui["frame"]["canvas"].winfo_width()
            canvas_height = gui["frame"]["canvas"].winfo_height()
            gui["frame"]["canvas"].coords(globals["misc_container"], canvas_width // 2, canvas_height // 2)
            
            # Appliquer l'ordre des calques
            if globals.get("misc_above_character", False):
                gui["frame"]["canvas"].lift(globals["misc_container"])
            else:
                gui["frame"]["canvas"].lift(globals["misc_container"], globals["background_container"])
                if globals["character"] is not None:
                    gui["frame"]["canvas"].lower(globals["misc_container"], globals["character"])
                        
        except Exception as e:
            tkinter.messagebox.showerror("Error", f"Failed to change misc: {str(e)}")



    def apply_crt(self, value: bool) -> None:
        """Applique l'effet CRT"""
        globals["render"]["val"]["crt"] = value
        if not value and globals["crt_container"] is not None:
            gui["frame"]["canvas"].delete(globals["crt_container"])
            globals["crt_container"] = None
            return
            
        if value:
            crt_path = path_finder("picts/crt/crt.png")
            if not os.path.exists(crt_path):
                tkinter.messagebox.showerror("Error", "CRT overlay not found")
                return
                
            crt = tk.PhotoImage(file=crt_path)
            gui["frame"]["preview"].crt = crt
            if globals["crt_container"] is None:
                globals["crt_container"] = gui["frame"]["canvas"].create_image(
                    0, 0, image=crt, anchor=tk.NW
                )
            else:
                gui["frame"]["canvas"].itemconfig(globals["crt_container"], image=crt)

    def activate_elements(self) -> None:
        """Active tous les éléments de l'interface"""
        try:
            if "warning_label" in gui["el"]:
                gui["el"]["warning_label"].destroy()

            if "save_button" in gui["el"]:
                gui["el"]["save_button"].configure(state=tk.NORMAL)

            for element in gui["el"]["char"]:
                widget = gui["el"]["char"][element]
                if isinstance(widget, (tk.Scale, tk.OptionMenu)):
                    widget.configure(state=tk.NORMAL)

            misc_widgets = ["posX", "posY", "scale", "rotate", "select", "priority_checkbox"]
            for element in misc_widgets:
                if element in gui["el"]["misc"]:
                    widget = gui["el"]["misc"][element]
                    if isinstance(widget, (tk.Scale, tk.OptionMenu, tk.Button, tk.Checkbutton)):
                        widget.configure(state=tk.NORMAL)

            if "crt" in gui["el"] and "checkbox" in gui["el"]["crt"]:
                gui["el"]["crt"]["checkbox"].configure(state=tk.NORMAL)
        except Exception as e:
            tkinter.messagebox.showerror("Error", f"Failed to activate elements: {str(e)}")

    def reset_values(self) -> None:
        """Réinitialise toutes les valeurs"""
        for element in globals["render"]["val"]:
            if element == "characterGradient":
                continue
            if element == "characterScale":
                globals["render"]["val"][element] = 100
            elif element != "characterGlitch":
                globals["render"]["val"][element] = 0
            else:
                globals["render"]["val"][element] = .1

        for element in gui["el"]["char"]:
            if isinstance(gui["el"]["char"][element], tk.Scale):
                if element == "scale":
                    gui["el"]["char"][element].set(100)
                elif element == "glitch":
                    gui["el"]["char"][element].set(.1)
                elif element != "gradients" and element != "glow":
                    gui["el"]["char"][element].set(0)

        for element in gui["el"]["misc"]:
            if isinstance(gui["el"]["misc"][element], tk.Scale):
                if element == "scale":
                    gui["el"]["misc"][element].set(100)
                elif element != "select":
                    gui["el"]["misc"][element].set(0)

    def get_filename(self, pict: str) -> str:
        """Récupère le nom de fichier sans extension"""
        filename = globals["render"][pict].split("/")[-1]
        return filename.split(".")[0]

editor = EditorGUI()

def leftFrame():
    editor.setup_left_frame()

def rightFrame():
    editor.setup_right_frame()