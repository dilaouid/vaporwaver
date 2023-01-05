import tkinter as tk
from gui.sides.frames.field import defineField
from gui.sides.frames.scale_bgfg import scales

def rightFrame(window):
    right_frame = tk.Frame(window)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    posX = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL)
    posX.pack()

    posY = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL)
    posY.pack()

    width = tk.Scale(right_frame, from_=0, to=100,orient=tk.HORIZONTAL)
    width.pack()

    height = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL)
    height.pack()

    selects = tk.Frame(right_frame)
    selects.pack()

    defineField("Foreground", selects)
    defineField("Background", selects)
    scales(right_frame)