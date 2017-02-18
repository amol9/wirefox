

from .time_window import TimeWindow
from .firefox_db import FirefoxDB


class MozPlaces:

    def __init__(self):
        self._firefox_db = None

    def query(self, url=None, title=None, start_time=None, end_time=None, period=None):
        if self._firefox_db is None:
            self._firefox_db = FirefoxDB()
            self._firefox_db.open_places_db()

        session = self._firefox_db.session
        moz_places = self._firefox_db.get_moz_places()

        q = session.query(moz_places)
        
        if url is not None:
            q = q.filter(moz_places.url.like('%s'%url))
        if title is not None:
            q = q.filter(moz_places.title.like('%%%s%%'%title))
        if start_time is not None or end_time is not None or period is not None:
            tw = TimeWindow(start=start_time, end=end_time, period=period)
            q = q.filter(moz_places.last_visit_date >= (tw.start_time.timestamp() * 1000000))
            q = q.filter(moz_places.last_visit_date <= (tw.end_time.timestamp() * 1000000))

        for r in q:
            print(r.url, '|', r.visit_count)
