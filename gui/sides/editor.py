import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
from data import globals, gui

""" L'astuce c'est de découper ton gui en plusieurs
petites fonctions sombre merde que tu es """

# get the filename of the background
def getFilename(pict: str):
    filename = globals[pict].split("/")[-1]
    filename = filename.split(".")[0]
    return filename[0].upper() + filename[1:]

def import_png():
    filepath = tkinter.filedialog.askopenfilename(title = "Select file" ,filetypes = [("png files","*.png")])
    with open(filepath, "rb") as f:
        globals["character"] = filepath
        gui["element"]["warning_label"].destroy()
        gui["element"]["save_button"].configure(state=tk.NORMAL)

def scaleElement(element, _from, _to, frame, labelText, row, col, value, resolution=1):
    label = tk.Label(frame, text=labelText, bg="#303030", fg="white")
    label.grid(row=row, column=col, padx=10)
    element = tk.Scale(frame, from_=_from, to=_to, orient=tk.HORIZONTAL, bg="#303030", fg="white", resolution=resolution)
    element.set(value)
    element.grid(row=row+1, column=col, padx=10, pady=10)

def leftFrame():
    globals["leftFrame"] = tk.Frame(globals["window"])
    globals["leftFrame"].configure(bg="#242424", bd=0, border=1, relief=tk.FLAT, width=560, height=555)
    globals["leftFrame"].pack(side=tk.LEFT, fill=tk.BOTH, anchor=tk.NW, padx=5, pady=5)

    preview_frame = tk.Frame(globals["leftFrame"], width=460, height=555)
    preview_frame.place(x=50, y=50)

    image = tk.PhotoImage(file=globals["background"])
    preview_bg = tk.Label(preview_frame)
    preview_bg.configure(image=image, border=1, relief=tk.RAISED)
    preview_bg.image = image
    preview_bg.place(width=460, height=555)
    
    s = ttk.Style()
    s.configure("Dark.TButton", bg="red", fg="white", font=("Helvetica", 10), borderwidth=10, borderradius=20)
    s.configure("Save.TButton", bg="red", fg="white", font=("Helvetica", 10), borderwidth=10, borderradius=20)
    import_button = tk.Button(globals["leftFrame"], text="Import", command=import_png)
    import_button.place(x=50, y=555+60, width=300, height=30)

    gui["element"]["save_button"] = tk.Button(globals["leftFrame"], text="Save", bg="blue", fg="white", state=tk.DISABLED if globals["character"] == None else tk.NORMAL)
    gui["element"]["save_button"].place(x=360, y=555+60, width=150, height=30)

    # enable the save button if a character is imported
    if globals["character"] != None:
        gui["element"]["save_button"].configure(state=tk.NORMAL)


    # add a warning label
    gui["element"]["warning_label"] = tk.Label(globals["leftFrame"], text="Warning: You need to import a character to start vaporwaving shits.", bg="#242424", fg="red", font=("Helvetica", 10))
    gui["element"]["warning_label"].place(x=50, y=555+60+30, width=460, height=30)

def rightFrame():
    gui["frame"]["right"] = tk.Frame(globals["window"])
    gui["frame"]["right"].configure(bg="#303030", bd=0, border=1, relief=tk.FLAT)
    gui["frame"]["right"].pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    gui["frame"]["right"].place(relx=0.53, rely=0.05)

    # Character edition (width, height, position, etc.)

    scaleElement(gui["element"]["character"]["posX"], -100, 100, gui["frame"]["right"], "Character X Position:", 0, 0, globals["characterXpos"])
    scaleElement(gui["element"]["character"]["posY"], -100, 100, gui["frame"]["right"], "Character Y Position:", 0, 1, globals["characterYpos"])
    scaleElement(gui["element"]["character"]["width"], -100, 100, gui["frame"]["right"], "Character Width:", 0, 2, globals["characterWidth"])
    scaleElement(gui["element"]["character"]["height"], -100, 100, gui["frame"]["right"], "Character Height:", 0, 3, globals["characterHeight"])
    scaleElement(gui["element"]["character"]["glitch"], 0, 10, gui["frame"]["right"], "Character Glitch (0-10):", 2, 0, globals["characterGlitch"], .1)

    gradient_label = tk.Label(gui["frame"]["right"], text="Gradient", bg="#303030", fg="white")
    gradient_label.grid(row=2, column=1)
    gradient_var = tk.StringVar(gui["frame"]["right"])
    gradient_var.set("None" if globals["characterGradient"] == 0 else globals["characterGradient"])
    gradient = tk.OptionMenu(gui["frame"]["right"], gradient_var, "None", "Option 1", "Option 2")
    gradient.grid(row=3, column=1)

    # Separator end of character edition
    separator = tk.Frame(gui["frame"]["right"], bg='white', width=200, height=1)
    separator.grid(row=4, column=0, columnspan=5, sticky=tk.EW, pady=10, padx=5)
    ##############################

    # Background and misc item management
    bglabel = tk.Label(gui["frame"]["right"], text="Background", bg="#303030", fg="white")
    bglabel.grid(row=5, column=0)
    bgvar = tk.StringVar(gui["frame"]["right"])
    bgvar.set(getFilename("background"))
    bg = tk.OptionMenu(gui["frame"]["right"], bgvar, "Default", "Option 2", "Option 3")
    bg.grid(row=6, column=0)

    msclabel = tk.Label(gui["frame"]["right"], text="Misc Item", bg="#303030", fg="white")
    msclabel.grid(row=5, column=1)
    mscvar = tk.StringVar(gui["frame"]["right"])
    mscvar.set("None")
    msc = tk.OptionMenu(gui["frame"]["right"], mscvar, "None", "Option 1", "Option 2")
    msc.grid(row=6, column=1, pady=10)

    scaleElement(gui["element"]["misc"]["posX"], -100, 100, gui["frame"]["right"], "Misc X Position:", 5, 2, globals["miscPosX"])
    scaleElement(gui["element"]["misc"]["posY"], -100, 100, gui["frame"]["right"], "Misc Y Position:", 5, 3, globals["miscPosY"])
    scaleElement(gui["element"]["misc"]["width"], -100, 100, gui["frame"]["right"], "Misc Width:", 7, 2, globals["miscWidth"])
    scaleElement(gui["element"]["misc"]["height"], -100, 100, gui["frame"]["right"], "Misc Height:", 7, 3, globals["miscHeight"])

    # Separator end of background and misc item edition
    separator_second = tk.Frame(gui["frame"]["right"], bg='white', width=200, height=1)
    separator_second.grid(row=9, column=0, columnspan=5, sticky=tk.EW, pady=10, padx=5)
    ##############################

    # Visual options

    crt_effect = tk.BooleanVar()
    check_crt = tk.Checkbutton(gui["frame"]["right"], text="CRT Effect", variable=crt_effect, bg="#303030", fg="white", selectcolor="#303030", activebackground="#303030", activeforeground="white", highlightbackground="#303030", highlightcolor="#303030", highlightthickness=1, bd=0)
    check_crt.grid(row=10, column=0, padx=10, pady=10)

    animate = tk.BooleanVar()
    check_animate = tk.Checkbutton(gui["frame"]["right"], text="Animate", variable=animate, bg="#303030", fg="white", selectcolor="#303030", activebackground="#303030", activeforeground="white", highlightbackground="#303030", highlightcolor="#303030", highlightthickness=1, bd=0)
    check_animate.grid(row=10, column=1, padx=10, pady=10)


    # disable all the widgets in the right frame except the separator and bgvar
    if globals["character"] == None:
        for child in gui["frame"]["right"].winfo_children():
            if child != separator and child != bg and child != separator_second:
                child.configure(state=tk.DISABLED)