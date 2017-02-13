
from .firefox_paths import FirefoxPaths
from .firefox_ui_builder import *


def main():
    fpaths = FirefoxPaths()
    recovery_js = None

    with open(fpaths.get_recovery_js_path(), 'rb') as f:
        recovery_js = f.read().decode()

    fub = FirefoxUIBuilder(recovery_js)

