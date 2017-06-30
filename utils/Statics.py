from datetime import datetime
from os.path import join
from pathlib import Path

from sys import path as syspath


class Statics:
    EMPTY = f''
    PARSER = 'html5lib'
    UTF8 = 'utf-8'
    SYSPATH = syspath[0]
    HTMLS = 'htmls'
    DATA = 'data'
    WORK_DIR = Path(join(SYSPATH, HTMLS))
    DATA_DIR = Path(join(SYSPATH, DATA))
    TODAY = datetime.now()
    SLEEP_TIME = 2

    @staticmethod
    def _get_tsv_path(symbol: str):
        return Path(join(f'{Statics.DATA_DIR}', f'{symbol}.tsv'))

    @staticmethod
    def get_tsv_path(symbol: str):
        return Statics._get_tsv_path('TSLA'), Statics._get_tsv_path('TSLA_PREV')

    @staticmethod
    def ensure(directory):
        if not directory.is_dir():
            directory.mkdir()

    @staticmethod
    def ensure_work_dir():
        Statics.ensure(Statics.WORK_DIR)

    @staticmethod
    def ensure_data_dir():
        Statics.ensure(Statics.DATA_DIR)

    @staticmethod
    def ensure_dirs():
        Statics.ensure_work_dir()
        Statics.ensure_data_dir()