import os, sys
from gui.window import configureWindow
from gui.editor import leftFrame, rightFrame
from data import globals
from lib.cli import apply_args

if len(sys.argv) > 1:
    apply_args()
else:
    globals["window"] = configureWindow()
    leftFrame()
    rightFrame()
    def closeWindow():
        if os.path.exists("tmp/char.png"):
            os.remove("tmp/char.png")
        globals["window"].destroy()

    globals["window"].protocol("WM_DELETE_WINDOW", closeWindow)

    # run the main loop
    globals["window"].mainloop()