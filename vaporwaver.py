import os, sys, uuid
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data import globals
from lib.paths import get_package_root, get_asset_path

globals["temp_suffix"] = uuid.uuid4().hex

package_root = get_package_root()

def get_tmp_dir():
    """Get tmp directory from environment variable or default"""
    return os.environ.get('VAPORWAVER_TMP') or os.path.join(get_package_root(), 'tmp')

globals["tmp_dir"] = get_tmp_dir()

os.makedirs(globals["tmp_dir"], exist_ok=True)  # dossier tmp pour les fichiers temporaires
os.makedirs(get_asset_path('picts/backgrounds'), exist_ok=True)  # assets
os.makedirs(get_asset_path('picts/miscs'), exist_ok=True)  # assets


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