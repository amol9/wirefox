
from redcmd.api import maincmd, execute_commandline

from .firefox_paths import FirefoxPaths
from .firefox_ui_builder import *
from .firefox_ui_filter import *
from .db.moz_places import *


def main2():
    fpaths = FirefoxPaths()
    recovery_js = None

    with open(fpaths.get_recovery_js_path(), 'rb') as f:
        recovery_js = f.read().decode()

    fub = FirefoxUIBuilder(recovery_js)
    fui = fub.build()

    print(fui)

#@maincmd
def filter(title='.*', url='.*', window=None, tab=None):
    f = FirefoxUIFilter(title=title, url=url, window=window, tab=tab)
    res = f.result()

    for i, r in enumerate(res):
        print(i)
        print(r)


def main():
    execute_commandline()


@maincmd
def db(url=None, title=None, start=None, end=None, period=None):
    mp = MozPlaces()
    mp.query(url=url, title=title, start_time=start, end_time=end, period=period)
