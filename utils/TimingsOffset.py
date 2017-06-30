from utils.DateTimeFormats import DTFormats
from datetime import datetime, timedelta


class TimingsOffset:
    TODAY = datetime.now()

    def __init__(self):
        self.today = TimingsOffset.TODAY
        self.int = 0
        self.td = self._update_timedelta()
        self.dt = self._update_datetime()
        self.ts = self._update_ts()
        self.ymd = self._update_ymd()
        self.bdy = self._update_bdy()
        self.days_ago = self._update_days_ago()
        self.day_start = self._update_day_start()
        self.day_end = self._update_day_end()
        self.url = self._update_url()

    def _update_url(self) -> str:
        return f'https://www.bing.com/search?q=Tesla&filters=ex1%3a%22ez5_{self.day_start}_{self.day_end}%22&qs=n&sp=-1&pq=tesla&sc=10-5&qpvt=Tesla'

    def url_with_first_offset(self, page: int):
        if page == 0:
            self.url = self._update_url()
            return self.url
        else:
            return f'{self.url}&first={(page*10)+1}'

    def _update_day_start(self) -> int:
        return timedelta(seconds=self.ts).days

    def _update_day_end(self) -> int:
        return timedelta(seconds=self.ts).days

    def _update_days_ago(self) -> str:
        return f'{self.int} days ago'

    def _update_ts(self):
        return self.dt.timestamp()

    def _update_bdy(self) -> str:
        return self.dt.strftime(DTFormats.BDY)

    def _update_ymd(self) -> str:
        return self.dt.strftime(DTFormats.YMD)

    def _update_datetime(self) -> datetime:
        return self.today - self.td

    def _update_timedelta(self) -> timedelta:
        return timedelta(days=self.int)

    def update(self):
        self.td = self._update_timedelta()
        self.dt = self._update_datetime()
        self.ts = self._update_ts()
        self.ymd = self._update_ymd()
        self.bdy = self._update_bdy()
        self.days_ago = self._update_days_ago()
        self.day_start = self._update_day_start()
        self.day_end = self._update_day_end()
        self.url = self._update_url()
