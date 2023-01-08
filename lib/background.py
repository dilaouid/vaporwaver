import tkinter as tk
from data import globals, gui

def changeBackground(file):
    preview_bg = tk.PhotoImage(file='picts/backgrounds/' + file + '.png')
    gui["frame"]["canvas"].preview_bg = preview_bg
    gui["frame"]["canvas"].itemconfig(globals["background_container"], image=preview_bg)