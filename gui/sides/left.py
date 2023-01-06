import tkinter as tk
from tkinter import ttk

def leftFrame(window):
    left_frame = tk.Frame(window)
    left_frame.configure(bg="#242424", bd=0, border=1, relief=tk.FLAT)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    image = tk.PhotoImage(file="picts/background/default.png")
    preview_label = tk.Label(left_frame)
    preview_label.configure(image=image, border=1, relief=tk.RAISED)
    preview_label.image = image
    preview_label.place(x=60, y=50, width=460, height=555)
    
    s = ttk.Style()
    s.configure("Dark.TButton", bg="red", fg="white", font=("Helvetica", 10), borderwidth=10, borderradius=20)
    s.configure("Save.TButton", bg="red", fg="white", font=("Helvetica", 10), borderwidth=10, borderradius=20)
    import_button = tk.Button(left_frame, text="Import")
    import_button.place(x=60, y=555+60, width=300, height=30)

    save_button = tk.Button(left_frame, text="Save", bg="blue", fg="white", state=tk.DISABLED)
    save_button.place(x=370, y=555+60, width=150, height=30)