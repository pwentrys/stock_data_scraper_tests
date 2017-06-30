import sys
import pathlib
import time
import os
from typing import Tuple

import requests
from urllib.parse import quote, urlparse
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


class Statics:
    PARSER = 'html5lib'
    UTF8 = 'utf-8'
    SYSPATH = sys.path[0]
    HTMLS = 'htmls'
    DATA = 'data'
    WORK_DIR = pathlib.Path(os.path.join(SYSPATH, HTMLS))
    DATA_DIR = pathlib.Path(os.path.join(SYSPATH, DATA))
    TODAY = datetime.now()
    SLEEP_TIME = 2

    @staticmethod
    def ensure_work_dir():
        if not Statics.WORK_DIR.is_dir():
            Statics.WORK_DIR.mkdir()

    @staticmethod
    def ensure_data_dir():
        if not Statics.DATA_DIR.is_dir():
            Statics.DATA_DIR.mkdir()

    @staticmethod
    def ensure_dirs():
        Statics.ensure_work_dir()
        Statics.ensure_data_dir()


Statics.ensure_dirs()


class DTFormats:
    BDY = '%b %d, %Y'  # Jun 1st, 2017
    YMD = '%Y%m%d'  # 20170601


class TimingsOffset:
    TODAY = Statics.TODAY

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

timings_offset = TimingsOffset()


class URLFormat:
    @staticmethod
    def _format(scheme, netloc, path, query):
        if query == '':
            return f'{scheme}://{netloc}{path}'
        else:
            return f'{scheme}://{netloc}{path}?{query}'

    @staticmethod
    def from_parsed(parsed_url) -> str:
        return URLFormat._format(parsed_url.scheme, parsed_url.netloc, parsed_url.path, quote(parsed_url.query, safe='=&'))

    @staticmethod
    def from_string(string: str) -> str:
        return URLFormat.from_parsed(urlparse(string))


class TagExtract:
    @staticmethod
    def li__b_algo(tag):
        return tag.name == 'li' and tag.has_attr('class') and tag.get('class') == ['b_algo']

    @staticmethod
    def a_link_title(tag):
        return tag.name == 'a' and tag.has_attr('h') and tag.parent.name == 'h2'

    @staticmethod
    def a_link_desc(tag):
        return tag.name == 'p'

    @staticmethod
    def a_link_news_dt(tag):
        return tag.name == 'span' and tag.has_attr('class') and tag.get('class') == ['news_dt'] and tag.parent.name == 'div' and tag.parent.parent.name == 'div'


class OutputFormat:
    BEGINS = []
    CONTAINS = ['|', '·']
    ENDS = ['…', '...', '-']

    @staticmethod
    def entry(string: str) -> str:
        string = string.strip()

        for begin in OutputFormat.BEGINS:
            if string.startswith(begin):
                string = string[len(begin):].strip()

        for end in OutputFormat.ENDS:
            if string.endswith(end):
                string = string[:-len(end)].strip()

        for contain in OutputFormat.CONTAINS:
            if string.__contains__(contain):
                string = string.replace(contain, '').strip()

        return string

    @staticmethod
    def title(string: str) -> str:
        string = OutputFormat.entry(string)
        return string

    @staticmethod
    def description(string: str) -> str:
        string = string.replace(timings_offset.bdy, '')
        string = OutputFormat.entry(string)
        return string

    @staticmethod
    def link(string: str) -> str:
        return URLFormat.from_string(string)


class Timings:
    SLEEP = Statics.SLEEP_TIME
    ESTIMATE_MULTI = 1.15

    def __init__(self):
        self._start = 0.0
        self._stop = 0.0
        self._stop_estimate = 0.0
        self._duration_actual = 0.0
        self._duration_estimate = 0.0
        self._duration_error = 0.0
        self._op_its = 0  # operation iterations
        self._counter = 0  # count which op we're at.

    def start(self):
        """
        Start timer.
        :return:
        """
        self._counter, self._start, self._stop_estimate = Timings._calculate_stop_estimate(time.time(), self._duration_estimate)

    @staticmethod
    def _calculate_stop_estimate(start: float, duration: float) -> Tuple[int, float, float]:
        """
        Calculate stop estimates.
        :param start:
        :param duration:
        :return:
        """
        return 0, start, start + duration

    def start_logged(self):
        """
        Run start and return log print.
        :return:
        """
        self.start()
        print('\n'.join([
            f'Start Time: {self._start}',
            f'Est Run: {self._duration_estimate}',
            f'Est Stop: {self._stop_estimate}',
            f'Op Its: {self._op_its}'
        ]))

    def stop(self):
        """
        Stop timer.
        :return:
        """
        self._stop, self._duration_actual, self._duration_error = Timings._calculate_duration(self._start, time.time(), self._duration_estimate)

    def stop_logged(self):
        """
        Run stop and return log print.
        :return:
        """
        self.stop()
        print('\n'.join([
            f' ---- Times  ---- ',
            f'Started: {self._start}',
            f'Finished: {self._stop}',
            f'Estimated: {self._stop_estimate}',
            f' ----- Run  ----- ',
            f'Actual: {self._duration_actual}',
            f'Estimated: {self._duration_estimate}',
            f'Error: {self._duration_error}',
            f' ---------------- '
        ]))

    @staticmethod
    def _calculate_duration_and_diff(estimate: float, actual: float) -> Tuple[float, float]:
        """
        Calculate duration and errors.
        :param estimate:
        :param actual:
        :return:
        """
        return actual, (estimate - actual) if estimate > actual else (actual - estimate)

    @staticmethod
    def _calculate_duration(start: float, stop: float, estimate: float) -> Tuple[float, float, float]:
        """
        Get duration and errors calculated.
        :param start:
        :param stop:
        :param estimate:
        :return:
        """
        duration, difference = Timings._calculate_duration_and_diff(estimate, stop - start)
        return stop, duration, difference

    @staticmethod
    def _estimate_duration(op_its: int, offset_multi: float) -> Tuple[float, float]:
        """
        Calculate run time estimate.

        (Operations x Iterations) x (Sleep Time x Offset Multi)
        :param op_its:
        :param offset_multi:
        :return:
        """
        return op_its, op_its * offset_multi

    def estimate_duration(self, operations: int, iterations: int):
        """
        Get run time estimate.
        :param operations:
        :param iterations:
        :return:
        """
        self._op_its, self._duration_estimate = Timings._estimate_duration(operations * iterations, self.SLEEP * self.ESTIMATE_MULTI)

    @staticmethod
    def _operation_logged(counter: int, total: int, start: float) -> int:
        """
        Print log and return incremented counter.
        :param counter:
        :param total:
        :param start:
        :return:
        """
        print(f'{counter} / {total}     -     Elapsed: {time.time() - start}')
        return counter

    def operation_logged(self):
        """
        Increment counter and log progress.
        :return:
        """
        self._counter = Timings._operation_logged(self._counter + 1, self._op_its, self._start)


timer = Timings()
# Timings.START = time.time()  # datetime.now()
tsv_path = pathlib.Path(os.path.join(f'{Statics.DATA_DIR}', 'TSLA.tsv'))
tsv_path_previous = pathlib.Path(os.path.join(f'{Statics.DATA_DIR}', 'TSLA_PREV.tsv'))
if not tsv_path.is_file():
    tsv_path.write_text('', encoding=Statics.UTF8)

cur_text = tsv_path.read_text(encoding=Statics.UTF8)
tsv_path_previous.write_text(cur_text, encoding=Statics.UTF8)
tsv_path.write_text('', encoding=Statics.UTF8)


def do_update_file_write(additions: list):
    active_text = tsv_path.read_text(encoding=Statics.UTF8)
    active_text_split = active_text.splitlines()
    for addition in additions:
        active_text_split.append(addition)
    updated_text = '\n'.join(set(active_text_split))
    tsv_path.write_text(updated_text, encoding=Statics.UTF8)


def run(offset_start: int, offset_end: int, pages: int):
    timer.estimate_duration(offset_end - offset_start, pages)
    # total_runs = ((offset_end - offset_start) * pages)
    timer.start_logged()
    # print(f'Start Time: {Timings.START}')
    # Timings.END_EST_SECS = total_runs * (Statics.SLEEP_TIME * 1.15)
    # Timings.END_EST = Timings.START + timedelta(seconds=Timings.END_EST_SECS)
    # print(f'Finish Est: {Timings.END_EST}   -   ({Timings.END_EST - Timings.START})')
    current_runs = 0
    final_results = []
    for i in range(offset_start, offset_end):
        timings_offset.int = i
        timings_offset.update()
        for j in range(0, pages):
            current_runs += 1
            # print(f'Starting {current_runs} / {total_runs}   -   ({datetime.now() - Timings.START}).')
            time.sleep(Statics.SLEEP_TIME)
            res = requests.get(timings_offset.url_with_first_offset(j))
            txt = res.text

            requests_html = pathlib.Path(os.path.join(Statics.WORK_DIR, 'requests_bing.html'))
            requests_html.write_text(txt, encoding=Statics.UTF8)

            soup_b_results = BeautifulSoup(txt, Statics.PARSER)
            b_results = soup_b_results.find(id='b_results')

            # 'html.parser'
            # Each entry is in an LI class called 'b_algo'
            soup_li__b_algo = BeautifulSoup(str(b_results), Statics.PARSER)
            soupr_algo = soup_li__b_algo.find_all(TagExtract.li__b_algo)

            soup_link = BeautifulSoup(str(soupr_algo), Statics.PARSER)
            soupr_t = soup_link.find_all(TagExtract.a_link_title)
            soupr_d = soup_link.find_all(TagExtract.a_link_desc)

            for i in range(0, len(soupr_t)):
                _continue = False
                title = soupr_t[i]
                desc = soupr_d[i]

                _desc = f'{desc.text}'.strip()
                if _desc.startswith(timings_offset.bdy):
                    _continue = True
                else:
                    soup_dt = BeautifulSoup(str(title.parent.parent), Statics.PARSER)
                    dt = soup_dt.find_all(TagExtract.a_link_news_dt)
                    if len(dt) > 0:
                        _dt = OutputFormat.entry(dt[0].text)
                        if _dt == timings_offset.days_ago:
                            _continue = True

                if _continue:
                    _desc = OutputFormat.description(_desc)
                    _text = OutputFormat.title(title.text)
                    _href = OutputFormat.link(title.get('href'))
                    final_results.append(f'{timings_offset.ymd}|{_href}|{_text}|{_desc}')

        if len(final_results) > 1000:
            do_update_file_write(final_results)
            final_results.clear()
            if len(final_results) > 0:
                final_results = []

    do_update_file_write(final_results)
    timer.stop_logged()

if __name__ == '__main__':
    run(0, 3, 3)

