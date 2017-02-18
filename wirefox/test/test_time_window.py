from unittest import TestCase, main as ut_main
from datetime import datetime


from ..db.time_window import TimeWindow

class TestTimeWindow(TestCase):

    def gen_test(self, twparams, start_dt, end_dt):
        tw = TimeWindow(**twparams)
        self.assertEqual(tw._start_dt, start_dt)
        self.assertEqual(tw._end_dt, end_dt)

    
    def test(self):
        self.gen_test({'start' : '01feb2017'},
            datetime(day=1, month=2, year=2017), datetime(day=2, month=2, year=2017))

        self.gen_test({'start' : '01feb2017', 'end': '02feb2017'},
            datetime(day=1, month=2, year=2017), datetime(day=2, month=2, year=2017))

        self.gen_test({'start' : '01feb2017', 'period' : '1s'},
            datetime(day=1, month=2, year=2017, second=0), datetime(day=1, month=2, year=2017, second=1))

        self.gen_test({'start' : '01feb2017', 'period' : '1Y'},
            datetime(day=1, month=2, year=2017), datetime(day=1, month=2, year=2018))

        self.gen_test({'start' : 'feb2017'},
            datetime(day=1, month=2, year=2017), datetime(day=1, month=3, year=2017))

        self.gen_test({'start' : '01feb2017', 'period' : '1M'},
            datetime(day=1, month=2, year=2017), datetime(day=3, month=3, year=2017))

        self.gen_test({'start' : '2017'},
            datetime(day=1, month=1, year=2017), datetime(day=1, month=1, year=2018))

        self.gen_test({'start' : '01feb2017-12:00'},
            datetime(day=1, month=2, year=2017, hour=12, minute=0),
            datetime(day=2, month=2, year=2017, hour=12, minute=0))

            
if __name__ == '__main__':
    ut_main()
