import os

def get_package_root():
    """Retourne le chemin racine du package"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_asset_path(relative_path):
    """Convertit un chemin relatif en chemin absolu par rapport à la racine du package"""
    return os.path.join(get_package_root(), relative_path)