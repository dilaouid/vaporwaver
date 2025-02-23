import os, sys, uuid
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from data import globals
from lib.paths import get_package_root, get_asset_path

globals["temp_suffix"] = uuid.uuid4().hex


package_root = get_package_root()
os.makedirs(get_asset_path('tmp'), exist_ok=True)
os.makedirs(get_asset_path('picts/backgrounds'), exist_ok=True)
os.makedirs(get_asset_path('picts/miscs'), exist_ok=True)

if len(sys.argv) > 1:
    from lib.cli import apply_args
    apply_args()
else:
    from gui.window import configureWindow
    from gui.editor import leftFrame, rightFrame

    globals["window"] = configureWindow()

    leftFrame()
    rightFrame()

    def closeWindow():
        from lib.output import OutputHandler
        handler = OutputHandler(cli_mode=False)
        handler.cleanup()
        globals["window"].destroy()

    globals["window"].protocol("WM_DELETE_WINDOW", closeWindow)
    globals["window"].mainloop()