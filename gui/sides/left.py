import tkinter as tk
from tkinter import ttk

def leftFrame(window):
    left_frame = tk.Frame(window)
    left_frame.configure(bg="#242424", bd=0, border=1, relief=tk.FLAT, width=560, height=555)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, anchor=tk.NW, padx=5, pady=5)

    image = tk.PhotoImage(file="picts/background/default.png")
    preview_label = tk.Label(left_frame)
    preview_label.configure(image=image, border=1, relief=tk.RAISED)
    preview_label.image = image
    preview_label.place(x=50, y=50, width=460, height=555)
    
    s = ttk.Style()
    s.configure("Dark.TButton", bg="red", fg="white", font=("Helvetica", 10), borderwidth=10, borderradius=20)
    s.configure("Save.TButton", bg="red", fg="white", font=("Helvetica", 10), borderwidth=10, borderradius=20)
    import_button = tk.Button(left_frame, text="Import")
    import_button.place(x=50, y=555+60, width=300, height=30)

    save_button = tk.Button(left_frame, text="Save", bg="blue", fg="white", state=tk.DISABLED)
    save_button.place(x=360, y=555+60, width=150, height=30)

    # add a warning label
    warning_label = tk.Label(left_frame, text="Warning: You need to import a character to start vaporwaving shits.", bg="#242424", fg="red", font=("Helvetica", 10))
    warning_label.place(x=50, y=555+60+30, width=460, height=30)