import tkinter as tk
from data import globals, gui

def changeBackground(filename: str) -> None:
    globals["render"]["background"] = 'picts/backgrounds/' + filename + '.png'
    preview_bg = tk.PhotoImage(file=globals["render"]["background"])
    gui["frame"]["canvas"].preview_bg = preview_bg
    gui["frame"]["canvas"].itemconfig(globals["background_container"], image=preview_bg)