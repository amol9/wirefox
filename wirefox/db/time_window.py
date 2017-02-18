from datetime import datetime, timedelta
import re
import itertools
from copy import copy


class TimeWindow:
    

    def __init__(self, start=None, end=None, period=None):
        self.start = start
        self.end = end

        self._start_dt  = None
        self._end_dt    = None
        self._period_td = None

        if end is None and period is not None:
            self._period_td = self.get_period_td(period)

        self.parse()


    def parse_period(self, period):
        period_regex = re.compile("(\d{1,3})((s|m|h|d|w|M|Y|D|C))")
        match = period_regex.match(period)

        if match is None:
            raise PeriodError('time period invalid')

        num = int(match.group(1))
        if num <= 0:
            raise TimeWindowError('bad value: %d'%num)
        period = match.group(2)

        return num, period


    def get_period_td(self, period):
        num, unit = self.parse_period(period)
        return self.get_timedelta(num, unit)


    def get_timedelta(self, num, unit):
        p = self.period_to_params(num, unit)
        return timedelta(**p)


    def period_to_params(self, num, unit):
        map = {
            's' :   { 'seconds' : num },
            'm' :   { 'minutes' : num },
            'h' :   { 'hours'   : num },
            'd' :   { 'days'    : num },
            'w' :   { 'weeks'   : num },
            'M' :   { 'days'    : num * 30},
            'Y' :   { 'days'    : num * 365},
            'D' :   { 'days'    : num * 3650},
            'C' :   { 'days'    : num * 36500}
        }
        return map[unit]


    def parse(self):
        if self.start is not None:
            self._start_dt = self.parse_time(self.start)
        else:
            if self._period_td is None:
                raise TimeWindowError()

            if self.end is not None:
                self._end_dt, _ = self.parse_time(self.end)
            else:
                self._end_dt = datetime.now()

            self._start_dt = self._end_dt - self._period_td
                
            return

        if self.end is not None:
            self._end_dt = self.parse_time(self.end)
        else:
            if self._period_td is not None:
                self._end_dt = self._start_dt + self._period_td
            else:
                self._end_dt = datetime.now()

        if self._end_dt < self._start_dt:
            raise  TimeWindowError()


    def parse_time(self, value):
        parts = value.split('-')
        date = parts[0]
        time = parts[1] if len(parts) > 1 else None

        date_fmts = [('%d%b%Y', {'day' : True}), ('%b%Y', {'month' : True}), ('%Y', {'year' : True})]
        time_fmts = ['%H:%M:%S', '%H:%M'] if time is not None else [None]
        
        for ((df, p), tf) in itertools.product(date_fmts, time_fmts):
            f = df + ('' if tf is None else '-' + tf)
            dt = self.match_time_fmt(value, f)

            if dt is not None:
                if self._period_td is None:
                    self._period_td = self.add_one_unit(dt, **p) - dt

                return dt


    def add_one_unit(self, dt, day=False, month=False, year=False):
        if day:
            return dt + timedelta(days=1)
        elif month:
            dec = dt.month == 12
            params = self.dt_params(dt)
            params['month'] = 1 if dec else dt.month + 1
            params['year'] = dt.year + 1 if dec else dt.year
            return datetime(**params)
        else:
            params = self.dt_params(dt)
            params['year'] = dt.year + 1
            return datetime(**params)


    def dt_params(self, dt):
        return {
            'day'   :   dt.day,
            'month' :   dt.month,
            'year'  :   dt.year,
            'hour'  :   dt.hour,
            'minute':   dt.minute,
            'second':   dt.second
        }


    def days_in_month(self, month, year):
        leap_year = year % 4 == 0
        if month == 2:
            return 29 if leap_year else 28
        elif month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        else:
            return 30

    def match_time_fmt(self, value, fmt):
        try:
            dt = datetime.strptime(value, fmt)
            return dt
        except ValueError:
            return None


    def get_start_time(self):
        return self._start_dt


    def get_end_time(self):
        return self._end_dt


    start_time = property(get_start_time)
    end_time = property(get_end_time)
