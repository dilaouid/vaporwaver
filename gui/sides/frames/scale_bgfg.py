import tkinter as tk

def scales(right_frame):
        foregroundX = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL)
        foregroundX.pack()

        foregroundY = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL)
        foregroundY.pack()

        backgroundX = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL)
        backgroundX.pack()

        backgroundY = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL)
        backgroundY.pack()