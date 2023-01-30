import tkinter as tk
from data import path_finder

def configureWindow() -> tk.Tk:
    window = tk.Tk()
    window.title("vaporwaver")
    # define the window icon
    window.iconbitmap(path_finder("picts/icon.ico"))
    window.configure(bg="#303030")
    window.geometry("1280x720")
    window.resizable(width=False, height=False)
    return window