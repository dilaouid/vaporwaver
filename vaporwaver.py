import os, sys, uuid
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from PIL import ImageFile
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    print("PIL configured to load truncated images")
except ImportError:
    print("PIL import error - image loading optimizations not applied")

from data import globals
from lib.paths import get_package_root, get_asset_path

globals["temp_suffix"] = uuid.uuid4().hex

package_root = get_package_root()

def get_tmp_dir():
    """Get tmp directory from environment variable or default"""
    return os.environ.get('VAPORWAVER_TMP') or os.path.join(get_package_root(), 'tmp')

def on_closing():
    """À appeler quand la fenêtre GUI se ferme"""
    from data import cleanup_temp_files
    cleanup_temp_files()
    globals["window"].destroy()

globals["tmp_dir"] = get_tmp_dir()

# Créer les dossiers nécessaires
os.makedirs(globals["tmp_dir"], exist_ok=True)  # dossier tmp pour les fichiers temporaires
os.makedirs(get_asset_path('picts/backgrounds'), exist_ok=True)  # assets
os.makedirs(get_asset_path('picts/miscs'), exist_ok=True)  # assets

if len(sys.argv) > 1:
    # Mode CLI
    try:
        from lib.cli import apply_args
        apply_args()
    finally:
        # Nettoyage à la fin en mode CLI
        from data import cleanup_temp_files
        cleanup_temp_files()
else:
    # Mode GUI
    from gui.window import configureWindow
    from gui.editor import leftFrame, rightFrame
    
    globals["window"] = configureWindow()
    leftFrame()
    rightFrame()
    
    def closeWindow():
        from data import cleanup_temp_files
        from lib.output import OutputHandler
        cleanup_temp_files()
        globals["window"].destroy()

    globals["window"].protocol("WM_DELETE_WINDOW", closeWindow)
    globals["window"].mainloop()