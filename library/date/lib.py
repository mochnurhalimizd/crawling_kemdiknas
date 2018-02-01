from time import mktime

from datetime import datetime as d
from datetime import timedelta as t


class DateClass:
    def __init__(self, date = None):
        if date:
            self.date = date
        else:
            self.date = d.now()


    @staticmethod
    def prefix_month(index):
        return '{}'.format(index) if index > 9 else '0{}'.format(index)

    def get_date(self, mode):
        result = {
            'month': lambda x: x.month,
            'date': lambda x: x.day,
            'year': lambda x: x.year,
            'hours': lambda x: x.hour,
            'minute': lambda x: x.minute,
            'second': lambda x: x.second,
            'full': lambda x: self.set_format('full_1')(x),
            'custom': lambda x: self.set_format('custom')(x),
            'current_day': lambda x: self.set_format('isodate')(x),
            'current_day_timestamp': lambda x: int(mktime(self.set_format('isodate')(x).timetuple())) * 1000,
            'last_days': lambda x: self.set_range(x, 1),
            'last_3_days': lambda x: self.set_range(x, 3),
            'last_5_days': lambda x: self.set_range(x, 5),
            'last_weeks': lambda x: self.set_range(x, 7),
            'last_days_timestamp': lambda x: int(mktime(self.set_range(x, 1).timetuple())) * 1000,
            'last_3_days_timestamp': lambda x: int(mktime(self.set_range(x, 3).timetuple())) * 1000,
            'last_5_days_timestamp': lambda x: int(mktime(self.set_range(x, 5).timetuple())) * 1000,
            'last_weeks_timestamp': lambda x: int(mktime(self.set_range(x, 7).timetuple())) * 1000,
            'object': lambda x: x,
        }

        return result.get(mode, lambda x: str('Oops key is not found'))(self.date)

    def set_date(self, date, formula):
        self.date = d.strptime(date, formula)

    def get_headline_info(self, mode):
        result = {
            'date': lambda x: self.set_format('date_2')(x),
            'isodate': lambda x: d.strptime('{}-{}-{}'.format(x.day, x.month, x.year), '%d-%m-%Y'),
        }

        return result.get(mode, lambda x: str('Oops key is not found'))(self.date)

    def set_format(self, mode):
        result = {
            'date_1': lambda x: '{}-{}-{}'.format(x.year, self.prefix_month(x.month), self.prefix_month(x.day)),
            'date_2': lambda x: '{}{}{}'.format(x.year, self.prefix_month(x.month), self.prefix_month(x.day)),
            'full_1': lambda x: '{}{}{} 000000'.format(x.year, self.prefix_month(x.month), self.prefix_month(x.day)),
            'full_2': lambda x: '{}{}{}00000000'.format(x.year, self.prefix_month(x.month), self.prefix_month(x.day)),
            'custom': lambda x: '{}{}{}{}{}{}'.format(
                x.year,
                self.prefix_month(x.month),
                self.prefix_month(x.day),
                self.prefix_month(x.hour),
                self.prefix_month(x.minute),
                self.prefix_month(x.second),
            ),
            'isodate': lambda x: d.strptime(self.set_format('full_1')(x), '%Y%m%d %H%M%S')
        }

        return result.get(mode, lambda x: str('Oops key is not found'))

    def set_range(self, date, ranges):
        return self.set_format('isodate')(date) - t(days=ranges)

    def get_data(self):
        return {
            'month': self.get_date('month'),
            'date': self.get_date('date'),
            'year': self.get_date('year'),
            'headline': {
                'date': self.get_headline_info('date'),
                'isoDate': self.get_headline_info('isodate'),
                'source_type': self.get_headline_info('source_type'),
            },
            'full': self.get_date('full'),
            'current_day': self.get_date('current_day'),
            'current_day_timestamp': self.get_date('current_day_timestamp'),
            'last_week': self.get_date('last_3_days'),
            'last_week_timestamp': self.get_date('last_3_days_timestamp'),
        }
