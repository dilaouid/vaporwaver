import tkinter as tk
from data import globals, gui

def changeBackground(filename: str) -> None:
    preview_bg = tk.PhotoImage(file='picts/backgrounds/' + filename + '.png')
    gui["frame"]["canvas"].preview_bg = preview_bg
    gui["frame"]["canvas"].itemconfig(globals["background_container"], image=preview_bg)