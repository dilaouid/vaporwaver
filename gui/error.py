import tkinter as tk
from tkinter import messagebox

def error_dialog(title: str, message: str) -> None:
    """Affiche une boîte de dialogue d'erreur"""
    messagebox.showerror(title, message)