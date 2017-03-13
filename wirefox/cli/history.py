
from redcmd.api import subcmd

from ..db.moz_places import *
from .base import Subcmd

#__all__ = ['HistorySubcmd', 'HistorySubcmds']


class HistorySubcmd(Subcmd):

    @subcmd
    def history(self):
        'Query history.'
        pass


class HistorySubcmds(HistorySubcmd):

    @subcmd
    def query(self, url=None, title=None, start=None, end=None, period=None):
        '''
        Query the firefox history database.

        url     : 
        title   :
        start   :
        end     :
        period  :
        '''

        mp = MozPlaces()
        mp.query(url=url, title=title, start_time=start, end_time=end, period=period)

