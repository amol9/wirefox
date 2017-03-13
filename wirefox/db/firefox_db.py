from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from ..firefox_paths import *


class FirefoxDB:

    def __init__(self):
        self._base = automap_base()
        self._engine = None
        self._session = None


    def open_places_db(self):
        db_path = FirefoxPaths().get_profile_path() + '/places.sqlite'
        self.open_db(db_path)


    def open_cookies_db(self, db_path=None):
        if db_path is None:
            db_path = FirefoxPaths().get_profile_path() + '/cookies.sqlite'
        self.open_db(db_path)


    def open_db(self, db_path):
        self._engine = create_engine("sqlite:///" + db_path)

        self._base.prepare(self._engine, reflect=True)
        self._session = Session(self._engine)


    def get_moz_places(self):
        return self._base.classes.moz_places


    def get_moz_cookies(self):
        return self._base.classes.moz_cookies


    def get_session(self):
        return self._session


    session = property(get_session)
