import tkinter as tk

def configureWindow():
    window = tk.Tk()
    window.title("Vaporwaver")
    window.geometry("1280x720")
    window.resizable(width=False, height=False)
    return window