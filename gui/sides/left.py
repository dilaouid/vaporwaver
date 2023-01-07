import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
from data import globals

def import_png():
    filepath = tkinter.filedialog.askopenfilename(title = "Select file" ,filetypes = [("png files","*.png")])
    with open(filepath, "rb") as f:
        global globals
        globals["character"] = f.read()
        # update the preview
        leftFrame()

def leftFrame():
    # if left frame already exists, destroy it
    if globals["window"].winfo_children():
        globals["window"].winfo_children()[0].destroy()
    left_frame = tk.Frame(globals["window"])
    left_frame.configure(bg="#242424", bd=0, border=1, relief=tk.FLAT, width=560, height=555)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, anchor=tk.NW, padx=5, pady=5)

    image = tk.PhotoImage(file=globals["background"])
    preview_label = tk.Label(left_frame)
    preview_label.configure(image=image, border=1, relief=tk.RAISED)
    preview_label.image = image
    preview_label.place(x=50, y=50, width=460, height=555)
    
    s = ttk.Style()
    s.configure("Dark.TButton", bg="red", fg="white", font=("Helvetica", 10), borderwidth=10, borderradius=20)
    s.configure("Save.TButton", bg="red", fg="white", font=("Helvetica", 10), borderwidth=10, borderradius=20)
    import_button = tk.Button(left_frame, text="Import", command=import_png)
    import_button.place(x=50, y=555+60, width=300, height=30)

    save_button = tk.Button(left_frame, text="Save", bg="blue", fg="white", state=tk.DISABLED)
    save_button.place(x=360, y=555+60, width=150, height=30)

    # add a warning label
    if globals["character"] == None:
        warning_label = tk.Label(left_frame, text="Warning: You need to import a character to start vaporwaving shits.", bg="#242424", fg="red", font=("Helvetica", 10))
        warning_label.place(x=50, y=555+60+30, width=460, height=30)