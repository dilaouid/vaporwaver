import os

def get_package_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_tmp_dir():
    tmp_env = os.environ.get('VAPORWAVER_TMP')
    if tmp_env:
        return tmp_env
    return os.path.join(get_package_root(), 'tmp')

def get_asset_path(relative_path):
    return os.path.join(get_package_root(), relative_path)