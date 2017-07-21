from datetime import datetime, timedelta
from utils.DateTimeFormats import DTFormats


class Stock:
    def __init__(self, display: str, symbol: str, day: int, pages: int):
        self.display = display
        self.symbol = symbol
        self.pages = pages
        self.day = day
        self.dt = Stock._get_dt(self.day)

    @staticmethod
    def _dts2dt(dt: str) -> datetime:
        return datetime.strptime(dt, DTFormats.YMD)

    @staticmethod
    def _get_dt(day: int) -> datetime:
        return datetime(year=1970, month=1, day=1) + timedelta(days=day)
