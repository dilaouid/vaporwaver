from gui.window import configureWindow
from gui.sides.left import leftFrame
from gui.sides.right import rightFrame
from data import globals

globals["window"] = configureWindow()
leftFrame()
rightFrame()

# run the main loop
globals["window"].mainloop()