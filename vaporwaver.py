import os, sys, uuid
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.window import configureWindow
from gui.editor import leftFrame, rightFrame

from data import globals
globals["temp_suffix"] = uuid.uuid4().hex

from lib.cli import apply_args

os.makedirs(os.path.join(os.path.dirname(__file__), 'tmp'), exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), 'picts/backgrounds'), exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), 'picts/miscs'), exist_ok=True)

if len(sys.argv) > 1:
    apply_args()
else:
    globals["window"] = configureWindow()
    leftFrame()
    rightFrame()
    def closeWindow():
        temp_char = os.path.join("tmp", f"char_{globals['temp_suffix']}.png")
        if os.path.exists(temp_char):
            os.remove(temp_char)
        globals["window"].destroy()

    globals["window"].protocol("WM_DELETE_WINDOW", closeWindow)
    globals["window"].mainloop()
