import os

def get_package_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_tmp_dir():
    """Récupérer le chemin du dossier tmp depuis l'environnement"""
    return os.environ.get('VAPORWAVER_TMP') or os.path.join(get_package_root(), 'tmp')

def get_asset_path(relative_path):
    return os.path.join(get_package_root(), relative_path)