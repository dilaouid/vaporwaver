import tkinter as tk

def leftFrame(window):
    left_frame = tk.Frame(window)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    image = tk.PhotoImage(file="picts/background/default.png")
    preview_label = tk.Label(left_frame)
    preview_label.configure(image=image)
    preview_label.image = image
    preview_label.place(x=40, y=50, width=460, height=555)

    import_button = tk.Button(left_frame, text="Import")
    import_button.place(x=40, y=555+60, width=460)