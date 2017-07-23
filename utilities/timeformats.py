from datetime import datetime, timedelta
from pathlib import Path
from utilities.typesext import Types as t


class TimeFormats:
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    FILETIME_FORMAT = '%Y%m%d_%H%M%S'
    DATESTRING_FORMAT = '%Y%m%d'

    @staticmethod
    def now2ft() -> str:
        """
        Returns now formatted to FILETIME_FORMAT.
        :return:
        """
        return datetime.now().strftime(TimeFormats.FILETIME_FORMAT)

    @staticmethod
    def now2f() -> str:
        """
        Returns now formatted to DATETIME_FORMAT.
        :return:
        """
        return datetime.now().strftime(TimeFormats.DATETIME_FORMAT)

    @staticmethod
    def dtMINts(dt: datetime, x: int):
        return dt - timedelta(days=x)

    @staticmethod
    def nowMINdays2dt(x: int) -> str:
        offset = TimeFormats.dtMINts(datetime.now(), x)
        return TimeFormats.ts2dt(offset).strftime(
            TimeFormats.DATESTRING_FORMAT)

    @staticmethod
    def utcnow2ft() -> str:
        """
        Returns utcnow formatted to FILETIME_FORMAT.
        :return:
        """
        return datetime.utcnow().strftime(TimeFormats.FILETIME_FORMAT)

    @staticmethod
    def utcnow2f() -> str:
        """
        Returns utcnow formatted to DATETIME_FORMAT.
        :return:
        """
        return datetime.utcnow().strftime(TimeFormats.DATETIME_FORMAT)

    @staticmethod
    def dt2ft(x) -> str:
        """
        Datetime to Filetime Datetime.
        Ex Out: 2500-01-01 23:59:59
        :param x:
        :return:
        """
        return x.strftime(TimeFormats.FILETIME_FORMAT)

    @staticmethod
    def dt2ts(x: datetime):
        return x.timestamp()

    @staticmethod
    def d2ts(x: str) -> float:
        return TimeFormats.dt2ts(TimeFormats.d2dt(x))

    @staticmethod
    def d2dt(x: str) -> datetime:
        return datetime.strptime(x, TimeFormats.DATESTRING_FORMAT)

    @staticmethod
    def dt2f(x) -> str:
        """
        Datetime to Formatted Datetime.
        Ex Out: 2500-01-01 23:59:59
        :param x:
        :return:
        """
        return x.strftime(TimeFormats.DATETIME_FORMAT)

    @staticmethod
    def ts2dt(x):
        """
        Timestamp to DateTime.
        :param x:
        :return:
        """
        return datetime.fromtimestamp(x)

    @staticmethod
    def ts2dt2ft(x) -> str:
        """
        Timestamp to Filetime Datetime... because lazy.
        :param x:
        :return:
        """
        return TimeFormats.dt2ft(TimeFormats.ts2dt(x))

    @staticmethod
    def ts2dt2f(x) -> str:
        """
        Timestamp to Formatted Datetime... because lazy.
        :param x:
        :return:
        """
        return TimeFormats.dt2f(TimeFormats.ts2dt(x))

    @staticmethod
    def _path2atime(path):
        """
        Path to Access Time
        :param path:
        :return:
        """
        try:
            return path.stat().st_atime
        except Exception as error:
            print(error)
            return 0

    @staticmethod
    def _path2ctime(path):
        """
        Path to Create Time
        :param path:
        :return:
        """
        try:
            return path.stat().st_ctime
        except Exception as error:
            print(error)
            return 0

    @staticmethod
    def _path2mtime(path):
        """
        Path to Modify Time
        :param path:
        :return:
        """
        try:
            return path.stat().st_mtime
        except Exception as error:
            print(error)
            return 0

    @staticmethod
    def _ensure_format(path):
        """
        Ensure object format.
        :param path:
        :return:
        """
        if isinstance(path, t.StringType):
            return Path(path)
        return path

    @staticmethod
    def path2mft(path):
        """
        Path to Modify Filetime
        :param path:
        :return:
        """
        try:
            path = TimeFormats._ensure_format(path)

            ts = TimeFormats._path2mtime(path)
            if ts == 0:
                return TimeFormats.now2ft()
            else:
                return TimeFormats.ts2dt2ft(ts)
        except Exception as error:
            print(error)
            return TimeFormats.now2ft()
