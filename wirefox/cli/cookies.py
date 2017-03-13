
from redcmd.api import subcmd

from ..db.moz_cookies import *
from .base import Subcmd

__all__ = ['CookiesSubcmds']


class CookiesSubcmd(Subcmd):

    @subcmd
    def cookies(self):
        'Query, export or import cookies.'
        pass


class CookiesSubcmds(CookiesSubcmd):

    def __init__(self):
        self._domain = None
        self._db_path = None

        self._moz_cookies = None

    
    def common(self, domain, db_path=None):
        '''
        domain  : domain name
        db_path : specify db path explicitly
        '''

        self._domain = domain
        self._db_path = db_path

        self._moz_cookies = MozCookies(db_path=db_path)


    @subcmd(add=[common])
    def query(self):
        '''
        Query cookies.
        '''

        self._moz_cookies.query(self._domain)


    @subcmd
    def load(self, filepath=None, dest_db=None, src_db=None, domain=None, names=None):
        '''
        Import cookies.

        filepath    : path to file containing SQL INSERT statements for cookies
        dest_db     : destination cookies db
        src_db      : source cookies db
        domain      : domain name
        '''

        self._moz_cookies = MozCookies(db_path=dest_db)
        name_list = names.split(',') if names is not None else None
        self._moz_cookies.load(filepath=filepath, dest_db=dest_db, src_db=src_db, domain=domain, names=name_list)


    @subcmd(add=[common])
    def export(self):
        '''
        Export cookies in form of SQL INSERT statements.
        '''

        self._moz_cookies.export(self._domain)


    @subcmd(add=[common])
    def clear(self):
        'Not implemented.'
        
        self._moz_cookies.remove(self._domain)

