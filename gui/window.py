import tkinter as tk

def configureWindow() -> tk.Tk:
    window = tk.Tk()
    window.title("vaporwaver")
    # define the window icon
    window.iconbitmap("picts/icon.ico")
    window.configure(bg="#303030")
    window.geometry("1280x720")
    window.resizable(width=False, height=False)
    return window