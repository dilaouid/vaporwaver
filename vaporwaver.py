import tkinter as tk
from gui.window import configureWindow
from gui.sides.left import leftFrame
from gui.sides.right import rightFrame

window = configureWindow()
leftFrame(window)
rightFrame(window)

# run the main loop
window.mainloop()