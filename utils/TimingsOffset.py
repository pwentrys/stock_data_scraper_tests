from datetime import datetime, timedelta

from utils.DateTimeFormats import DTFormats


class TimingsOffset:
    """

    """
    TODAY = datetime.now()

    def __init__(self, name: str):
        self.name = name
        self.today = TimingsOffset.TODAY
        self.num = 1
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
        name = self.name
        start = self.day_start
        end = self.day_end
        return f'https://www.bing.com/search?' \
               f'q={name}&' \
               f'filters=ex1%3a%22ez5_{start}_{end}%22&' \
               f'qs=n&' \
               f'sp=-1&' \
               f'pq={name.lower()}&' \
               f'sc=10-5&' \
               f'qpvt={name}'

    def url_with_first_offset(self, page: int) -> str:
        """

        :param page:
        :return:
        """
        if page == 0:
            self.url = self._update_url()
            return self.url

        offset = (page * 10) + 1

        if offset > 1:
            return f'{self.url}&first={offset}'

        self.url = self._update_url()
        return self.url

    def _update_day_start(self) -> int:
        return timedelta(seconds=self.ts).days

    def _update_day_end(self) -> int:
        return timedelta(seconds=self.ts).days

    def _update_days_ago(self) -> str:
        num = self.num
        return f'{num} days ago'

    def _update_ts(self):
        return self.dt.timestamp()

    def _update_bdy(self) -> str:
        return self.dt.strftime(DTFormats.BDY)

    def _update_ymd(self) -> str:
        return self.dt.strftime(DTFormats.YMD)

    def _update_datetime(self) -> datetime:
        int_sec = int(self.td.total_seconds())
        return datetime.utcfromtimestamp(int_sec)

    def _update_timedelta(self) -> timedelta:
        return timedelta(days=self.num)

    def update_num(self, num: int):
        self.num = num + 1
        self.update()

    def update(self):
        """

        """
        self.td = self._update_timedelta()
        self.dt = self._update_datetime()
        self.ts = self._update_ts()
        self.ymd = self._update_ymd()
        self.bdy = self._update_bdy()
        self.days_ago = self._update_days_ago()
        self.day_start = self._update_day_start()
        self.day_end = self._update_day_end()
        self.url = self._update_url()
