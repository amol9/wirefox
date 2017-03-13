
from redcmd.api import subcmd

from ..firefox_ui_filter import *
from .base import Subcmd

__all__ = ['TabsSubcmds']


class TabsSubcmd(Subcmd):

    @subcmd
    def tabs(self):
        'Query currently open tabs.'
        pass


class TabsSubcmds(TabsSubcmd):

    @subcmd
    def query(self, title='.*', url='.*', window=None, tab=None):
        '''
        Query currently open tabs.

        title   :
        url     :
        window  :
        tab     :
        '''

        f = FirefoxUIFilter(title=title, url=url, window=window, tab=tab)
        res = f.result()

        for i, r in enumerate(res):
            print(i)
            print(r)

