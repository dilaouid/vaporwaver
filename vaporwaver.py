from gui.window import configureWindow
from gui.sides.editor import leftFrame, rightFrame
from data import globals

globals["window"] = configureWindow()
leftFrame()
rightFrame()

# run the main loop
globals["window"].mainloop()