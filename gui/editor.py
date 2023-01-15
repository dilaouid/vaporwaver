import os
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import tkinter.messagebox
from typing import Union
from data import globals, gui
from PIL import Image
from lib.background import changeBackground
from lib.character import moveCharacter, scaleCharacter, glitchCharacter, gradientCharacter, glowCharacter
from lib.crt import crt
from lib.misc import changeMisc, moveMisc, scaleMisc, rotateMisc
from lib.output import outputPicture

def RBGAImage(path: str) -> Image:
    return Image.open(path).convert("RGBA")

# get the filename of the background
def getFilename(pict: str) -> str:
    filename = globals[pict].split("/")[-1]
    filename = filename.split(".")[0]
    return filename

def activateElements() -> None:
    gui["el"]["warning_label"].destroy()
    gui["el"]["save_button"].configure(state=tk.NORMAL)
    for element in gui["el"]["char"]:
        gui["el"]["char"][element].configure(state=tk.NORMAL)
    for element in gui["el"]["misc"]:
        gui["el"]["misc"][element].configure(state=tk.NORMAL)
    gui["el"]["crt"]["checkbox"].configure(state=tk.NORMAL)

def resetValues() -> None:
    for element in globals["val"]:
        if element == "characterGradient":
            continue
        if element == "characterScale":
            globals["val"][element] = 100
        elif element != "characterGlitch":
            globals["val"][element] = 0
        else:
            globals["val"][element] = .1
    for element in gui["el"]["char"]:
        if element == "scale":
            gui["el"]["char"][element].set(100)
        elif element == "glitch":
            gui["el"]["char"][element].set(.1)
        elif element != "gradients" and element != "glow":
            gui["el"]["char"][element].set(0)
    for element in gui["el"]["misc"]:
        if element == "scale":
            gui["el"]["misc"][element].set(100)
        elif element != "select":
            gui["el"]["misc"][element].set(0)

def import_png() -> None:
    filepath: str = tkinter.filedialog.askopenfilename(title = "Select file" ,filetypes = [("png files","*.png")])
    if filepath == "":
        return
    with open(filepath, "rb") as f:
        globals["characterPath"] = filepath
        try:
            globals["gcChar"] = tk.PhotoImage(file=globals["characterPath"])
        except tk.TclError:
            # show a window with an error message
            tkinter.messagebox.showerror("Error", "The selected file is not a valid PNG file.")
            return

        if os.path.exists("tmp/char.png"):
            os.remove("tmp/char.png")

        # center the character according to the canvas
        globals["character"] = gui["frame"]["canvas"].create_image((0, 0), image=globals["gcChar"], anchor=tk.NW)
        gui["frame"]["canvas"].character = globals["gcChar"]
        gui["frame"]["canvas"].itemconfig(globals["character"], image=globals["gcChar"])

        activateElements()
        resetValues()

def scaleElement(element, _from: Union[int, float], _to: Union[int, float], frame: tk.Frame, labelText: str, row: int, col: int, value: Union[int, float], func, resolution=1) -> tk.Scale:
    label = tk.Label(frame, text=labelText, bg="#303030", fg="white")
    label.grid(row=row, column=col, padx=10)
    element = tk.Scale(frame, from_=_from, to=_to, orient=tk.HORIZONTAL, bg="#303030", fg="white", resolution=resolution, command=lambda x: func(value, x))
    element.set(globals["val"][value])
    element.grid(row=row+1, column=col, padx=10, pady=10)
    return element

def leftFrame() -> None:
    gui["frame"]["left"] = tk.Frame(gui["frame"]["window"])
    gui["frame"]["left"].configure(bg="#242424", bd=0, border=1, relief=tk.FLAT, width=560, height=595)
    gui["frame"]["left"].pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)

    gui["frame"]["preview"] = tk.Frame(gui["frame"]["left"], width=460, height=595)
    gui["frame"]["preview"].place(x=50, y=10)

    gui["frame"]["canvas"] = tk.Canvas(gui["frame"]["preview"], width=460, height=595, bg="grey")
    gui["frame"]["canvas"].pack(fill=tk.BOTH, anchor=tk.NW)

    preview_bg = tk.PhotoImage(file=globals["background"])
    gui["frame"]["preview"].preview_bg = preview_bg
    globals["background_container"] = gui["frame"]["canvas"].create_image((0, 0), image=gui["frame"]["preview"].preview_bg, anchor=tk.NW)

    misc = tk.PhotoImage(file=globals["misc"])
    gui["frame"]["preview"].misc = misc
    globals["misc_container"] = gui["frame"]["canvas"].create_image((0, 0), image=gui["frame"]["preview"].misc, anchor=tk.NW)
    
    s = ttk.Style()
    s.configure("Dark.TButton", bg="red", fg="white", font=("Helvetica", 10), borderwidth=10, borderradius=20)
    s.configure("Save.TButton", bg="red", fg="white", font=("Helvetica", 10), borderwidth=10, borderradius=20)
    import_button = tk.Button(gui["frame"]["left"], text="Import", command=import_png)
    import_button.place(x=50, y=555+60, width=300, height=30)

    gui["el"]["save_button"] = tk.Button(gui["frame"]["left"], text="Save", bg="blue", fg="white", state=tk.DISABLED if globals["character"] == None else tk.NORMAL, command=outputPicture)
    gui["el"]["save_button"].place(x=360, y=555+60, width=155, height=30)

    # enable the save button if a character is imported
    if globals["character"] != None:
        gui["el"]["save_button"].configure(state=tk.NORMAL)


    # add a warning label
    gui["el"]["warning_label"] = tk.Label(gui["frame"]["left"], text="Warning: You need to import a character to start vaporwaving shits.", bg="#242424", fg="red", font=("Helvetica", 10))
    gui["el"]["warning_label"].place(x=50, y=555+60+30, width=460, height=30)

def rightFrame() -> None:
    gui["frame"]["right"] = tk.Frame(gui["frame"]["window"])
    gui["frame"]["right"].configure(bg="#303030", bd=0, border=1, relief=tk.FLAT)
    gui["frame"]["right"].pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    gui["frame"]["right"].place(relx=0.53, rely=0.05)

    # Character edition (width, height, position, etc.)

    gui["el"]["char"]["posX"] = scaleElement(gui["el"]["char"]["posX"], -100, 100, gui["frame"]["right"], "Character X Position:", 0, 0, "characterXpos", moveCharacter)
    gui["el"]["char"]["posY"] = scaleElement(gui["el"]["char"]["posY"], -100, 100, gui["frame"]["right"], "Character Y Position:", 0, 1, "characterYpos", moveCharacter)
    gui["el"]["char"]["scale"] = scaleElement(gui["el"]["char"]["scale"], 1, 200, gui["frame"]["right"], "Character Scale:", 0, 2, "characterScale", scaleCharacter)
    gui["el"]["char"]["glitch"] = scaleElement(gui["el"]["char"]["glitch"], .1, 10, gui["frame"]["right"], "Character Glitch (.1-10):", 0, 3, "characterGlitch", glitchCharacter, .1)
    gui["el"]["char"]["glitchSeed"] = scaleElement(gui["el"]["char"]["glitchSeed"], 0, 100, gui["frame"]["right"], "Character Glitch Seed:", 2, 3, "characterGlitchSeed", glitchCharacter)

    gradient_label = tk.Label(gui["frame"]["right"], text="Gradient", bg="#303030", fg="white")
    gradient_label.grid(row=2, column=0)
    gradient_var = tk.StringVar(gui["frame"]["right"])
    gradient_var.set("none")
    gui["el"]["char"]["gradients"] = tk.OptionMenu(gui["frame"]["right"], gradient_var, *globals["gradients"], command=lambda x: gradientCharacter(x))
    gui["el"]["char"]["gradients"].grid(row=3, column=0)

    gradient_label = tk.Label(gui["frame"]["right"], text="Glow", bg="#303030", fg="white")
    gradient_label.grid(row=2, column=1)
    gradient_var = tk.StringVar(gui["frame"]["right"])
    gradient_var.set("none")
    gui["el"]["char"]["glow"] = tk.OptionMenu(gui["frame"]["right"], gradient_var, *globals["glow"], command=lambda x: glowCharacter(x))
    gui["el"]["char"]["glow"].grid(row=3, column=1)

    # Separator end of character edition
    separator = tk.Frame(gui["frame"]["right"], bg='white', width=200, height=1)
    separator.grid(row=4, column=0, columnspan=5, sticky=tk.EW, pady=10, padx=5)
    ##############################

    # Background and misc item management
    bglabel = tk.Label(gui["frame"]["right"], text="Background", bg="#303030", fg="white")
    bglabel.grid(row=5, column=0)
    bgvar = tk.StringVar(gui["frame"]["right"])
    bgvar.set(getFilename("background"))
    # create an option menu with all the values in the backgrounds list
    bg = tk.OptionMenu(gui["frame"]["right"], bgvar, *globals["backgrounds"], command=changeBackground)
    bg.grid(row=6, column=0)

    msclabel = tk.Label(gui["frame"]["right"], text="Misc Item", bg="#303030", fg="white")
    msclabel.grid(row=5, column=1)
    mscvar = tk.StringVar(gui["frame"]["right"])
    mscvar.set("none")
    gui["el"]["misc"]["select"] = tk.OptionMenu(gui["frame"]["right"], mscvar, *globals["miscs"], command=changeMisc)
    gui["el"]["misc"]["select"].grid(row=6, column=1, pady=10)

    gui["el"]["misc"]["posX"] = scaleElement(gui["el"]["misc"]["posX"], -100, 100, gui["frame"]["right"], "Misc X Position:", 5, 2, "miscPosX", moveMisc)
    gui["el"]["misc"]["posY"] = scaleElement(gui["el"]["misc"]["posY"], -100, 100, gui["frame"]["right"], "Misc Y Position:", 5, 3, "miscPosY", moveMisc)
    gui["el"]["misc"]["scale"] = scaleElement(gui["el"]["misc"]["scale"], 1, 200, gui["frame"]["right"], "Misc Scale:", 7, 2, "miscScale", scaleMisc)
    gui["el"]["misc"]["rotate"] = scaleElement(gui["el"]["misc"]["rotate"], -360, 360, gui["frame"]["right"], "Misc Rotation:", 7, 3, "miscRotate", rotateMisc)

    # Separator end of background and misc item edition
    separator_second = tk.Frame(gui["frame"]["right"], bg='white', width=200, height=1)
    separator_second.grid(row=9, column=0, columnspan=5, sticky=tk.EW, pady=10, padx=5)
    ##############################

    # Visual options

    crt_effect = tk.BooleanVar()
    gui["el"]["crt"]["checkbox"] = tk.Checkbutton(gui["frame"]["right"], text="CRT Effect", variable=crt_effect, bg="#303030", fg="white", selectcolor="#303030", activebackground="#303030", activeforeground="white", highlightbackground="#303030", highlightcolor="#303030", highlightthickness=1, bd=0, command=lambda: crt(crt_effect.get()))
    gui["el"]["crt"]["checkbox"].grid(row=10, column=0, padx=10, pady=10)

    # disable all the widgets in the right frame except the separator and bgvar
    if globals["character"] == None:
        for child in gui["frame"]["right"].winfo_children():
            if child != separator and child != bg and child != separator_second:
                child.configure(state=tk.DISABLED)