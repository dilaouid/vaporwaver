import tkinter as tk
from tkinter import ttk
from gui.sides.frames.field import defineField

def rightFrame(window):
    right_frame = tk.Frame(window)
    right_frame.configure(bg="#303030", bd=0, border=1, relief=tk.FLAT)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    right_frame.place(relx=0.53, rely=0.05)

    # Character edition (width, height, position, etc.)
    posX_label = tk.Label(right_frame, text="Character X Position:", bg="#303030", fg="white")
    posX_label.grid(row=0, column=0, padx=10)
    posX = tk.Scale(right_frame, from_=-100, to=100, orient=tk.HORIZONTAL, bg="#303030", fg="white")
    posX.set(0)
    posX.grid(row=1, column=0, padx=10, pady=10)

    posY_label = tk.Label(right_frame, text="Character Y Position", bg="#303030", fg="white")
    posY_label.grid(row=0, column=1, padx=10)
    posY = tk.Scale(right_frame, from_=-100, to=100, orient=tk.HORIZONTAL, bg="#303030", fg="white")
    posY.set(0)
    posY.grid(row=1, column=1, padx=10, pady=10)

    width_label = tk.Label(right_frame, text="Character Width", bg="#303030", fg="white")
    width_label.grid(row=0, column=2, padx=10)
    width = tk.Scale(right_frame, from_=-100, to=100, orient=tk.HORIZONTAL, bg="#303030", fg="white")
    width.set(0)
    width.grid(row=1, column=2, padx=10, pady=10)

    height_label = tk.Label(right_frame, text="Character Height", bg="#303030", fg="white")
    height_label.grid(row=0, column=3, padx=10)
    height = tk.Scale(right_frame, from_=-100, to=100, orient=tk.HORIZONTAL, bg="#303030", fg="white")
    height.set(0)
    height.grid(row=1, column=3, padx=10, pady=10)

    glitch_label = tk.Label(right_frame, text="Character Glitch (0-10)", bg="#303030", fg="white")
    glitch_label.grid(row=2, column=0, padx=10)
    glitch = tk.Scale(right_frame, from_=0.0, to=10.0, orient=tk.HORIZONTAL, bg="#303030", fg="white", resolution=.1)
    glitch.set(0)
    glitch.grid(row=3, column=0, padx=10, pady=10)

    gradient_label = tk.Label(right_frame, text="Gradient", bg="#303030", fg="white")
    gradient_label.grid(row=2, column=1)
    gradient_var = tk.StringVar(right_frame)
    gradient_var.set("None")
    gradient = tk.OptionMenu(right_frame, gradient_var, "None", "Option 1", "Option 2")
    gradient.grid(row=3, column=1)

    # Separator end of character edition
    separator = tk.Frame(right_frame, bg='white', width=200, height=1)
    separator.grid(row=4, column=0, columnspan=5, sticky=tk.EW, pady=10, padx=5)
    ##############################

    # Background and misc item management
    bglabel = tk.Label(right_frame, text="Background", bg="#303030", fg="white")
    bglabel.grid(row=5, column=0)
    bgvar = tk.StringVar(right_frame)
    bgvar.set("Default")
    bg = tk.OptionMenu(right_frame, bgvar, "Default", "Option 2", "Option 3")
    bg.grid(row=6, column=0)

    msclabel = tk.Label(right_frame, text="Misc Item", bg="#303030", fg="white")
    msclabel.grid(row=5, column=1)
    mscvar = tk.StringVar(right_frame)
    mscvar.set("None")
    msc = tk.OptionMenu(right_frame, mscvar, "None", "Option 1", "Option 2")
    msc.grid(row=6, column=1, pady=10)

    msc_width_label = tk.Label(right_frame, text="Misc Width", bg="#303030", fg="white")
    msc_width_label.grid(row=5, column=2, padx=10)
    msc_width = tk.Scale(right_frame, from_=-100, to=100, orient=tk.HORIZONTAL, bg="#303030", fg="white")
    msc_width.set(0)
    msc_width.grid(row=6, column=2, padx=10, pady=10)

    msc_height_label = tk.Label(right_frame, text="Misc Height", bg="#303030", fg="white")
    msc_height_label.grid(row=5, column=3, padx=10)
    msc_height = tk.Scale(right_frame, from_=-100, to=100, orient=tk.HORIZONTAL, bg="#303030", fg="white")
    msc_height.set(0)
    msc_height.grid(row=6, column=3, padx=10, pady=10)
    
    msc_posX_label = tk.Label(right_frame, text="Misc X Position", bg="#303030", fg="white")
    msc_posX_label.grid(row=7, column=2, padx=10)
    msc_posX = tk.Scale(right_frame, from_=-100, to=100, orient=tk.HORIZONTAL, bg="#303030", fg="white")
    msc_posX.set(0)
    msc_posX.grid(row=8, column=2, padx=10, pady=10)

    msc_posY_label = tk.Label(right_frame, text="Misc Y Position", bg="#303030", fg="white")
    msc_posY_label.grid(row=7, column=3, padx=10)
    msc_posY = tk.Scale(right_frame, from_=-100, to=100, orient=tk.HORIZONTAL, bg="#303030", fg="white")
    msc_posY.set(0)
    msc_posY.grid(row=8, column=3, padx=10, pady=10)

    # Separator end of background and misc item edition
    separator_second = tk.Frame(right_frame, bg='white', width=200, height=1)
    separator_second.grid(row=9, column=0, columnspan=5, sticky=tk.EW, pady=10, padx=5)
    ##############################

    # Visual options

    crt_effect = tk.BooleanVar()
    check_crt = tk.Checkbutton(right_frame, text="CRT Effect", variable=crt_effect, bg="#303030", fg="white", selectcolor="#303030", activebackground="#303030", activeforeground="white", highlightbackground="#303030", highlightcolor="#303030", highlightthickness=1, bd=0)
    check_crt.grid(row=10, column=0, padx=10, pady=10)

    animate = tk.BooleanVar()
    check_animate = tk.Checkbutton(right_frame, text="Animate", variable=animate, bg="#303030", fg="white", selectcolor="#303030", activebackground="#303030", activeforeground="white", highlightbackground="#303030", highlightcolor="#303030", highlightthickness=1, bd=0)
    check_animate.grid(row=10, column=1, padx=10, pady=10)


    # disable all the widgets in the right frame except the separator and bgvar
    for child in right_frame.winfo_children():
        if child != separator and child != bg and child != separator_second:
            child.configure(state=tk.DISABLED)