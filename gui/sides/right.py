import tkinter as tk
from gui.sides.frames.field import defineField

def rightFrame(window):
    right_frame = tk.Frame(window)
    right_frame.configure(bg="#303030", bd=0, border=1, relief=tk.FLAT)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    posX = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL)
    posX.pack()

    posY = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL)
    posY.pack()

    width = tk.Scale(right_frame, from_=0, to=100,orient=tk.HORIZONTAL)
    width.pack()

    height = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL)
    height.pack()

    selects = tk.Frame(right_frame)
    selects.pack()

    bglabel = tk.Label(selects, text="Background")
    bglabel.grid(row=0, column=0)

    bgvar = tk.StringVar(selects)
    bgvar.set("Default")
    bgel = tk.OptionMenu(selects, bgvar, "Default", "Option 2", "Option 3")
    bgel.grid(row=1, column=0)

    fglabel = tk.Label(selects, text="Foreground")
    fglabel.grid(row=0, column=1)

    fgvar = tk.StringVar(selects)
    fgvar.set("Nothing")
    fgel = tk.OptionMenu(selects, fgvar, "Nothing", "Option 2", "Option 3")
    fgel.grid(row=1, column=1)

    foregroundX = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL)
    foregroundX.pack()

    foregroundY = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL)
    foregroundY.pack()

    backgroundX = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL)
    backgroundX.pack()

    backgroundY = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL)
    backgroundY.pack()