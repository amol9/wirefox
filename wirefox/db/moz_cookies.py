
from sqlalchemy.types import TEXT
from sqlalchemy.orm.session import make_transient

from .time_window import TimeWindow
from .firefox_db import FirefoxDB


class MozCookies:

    def __init__(self, db_path=None):
        self._firefox_db = None
        self._db_path = db_path


    def open_db(self):    
        if self._firefox_db is None:
            self._firefox_db = FirefoxDB()
            self._firefox_db.open_cookies_db(db_path=self._db_path)

        session = self._firefox_db.session
        moz_cookies = self._firefox_db.get_moz_cookies()

        return session, moz_cookies
         

    def query(self, domain):
        session, moz_cookies = self.open_db()
        q = session.query(moz_cookies)
        
        q = q.filter(moz_cookies.baseDomain == domain)

        for r in q:
            print('%-20s: %s'%(r.name, r.value))


    def export(self, domain):
        session, moz_cookies = self.open_db()
        q = session.query(moz_cookies)
        
        q = q.filter(moz_cookies.baseDomain == domain)

        insert_st = "INSERT INTO moz_cookies (%s) VALUES(%s);\n"
        count = 0

        with open('cookies.sql', 'w') as f:
            for r in q:
                columns = ''
                values = ''
                for c in r.__table__.columns:
                    col_name = c.name.split('.')[-1]
                    if col_name == 'id':
                        continue

                    columns += (', ' + col_name) if len(columns) > 0 else col_name

                    value = str(getattr(r, col_name))
                    if type(c.type) == TEXT:
                        value = '"' + value + '"'

                    values += (', ' + value) if len(values) > 0 else value

                f.write(insert_st%(columns, values))
                count += 1

        print('%d cookies exported.'%count)


    def load(self, filepath=None, dest_db=None, src_db=None, domain=None, names=None):
            session, moz_cookies = self.open_db()

            if src_db is not None:
                fxdb = FirefoxDB()
                fxdb.open_cookies_db(db_path=src_db)
                src_session = fxdb.session
                src_mc = fxdb.get_moz_cookies()

                q = src_session.query(src_mc)
                q = q.filter(src_mc.baseDomain == domain)

                count = 0
                for r in q:
                    if names is not None and not r.name in names:
                        continue

                    src_session.expunge(r)
                    make_transient(r)
                    r.id = None
                    session.add(r)
                    count += 1

                session.flush()
                print('copied %d cookies'%count)
                

    def remove(self, domain):
        session, moz_cookies = self.open_db()
        q = session.query(moz_cookies)
        
        q = q.filter(moz_cookies.baseDomain == domain)

        count = 0

        for r in q:
            session.delete(r)
            count += 1

        session.commit()
        print('%d cookies deleted'%count)    
 
