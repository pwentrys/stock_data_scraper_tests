import sys
import pathlib
import os

import requests
from urllib.parse import quote, urlparse
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


class Statics:
    PARSER = 'html5lib'
    UTF8 = 'utf-8'
    SYSPATH = sys.path[0]
    HTMLS = 'htmls'
    WORK_DIR = pathlib.Path(os.path.join(SYSPATH, HTMLS))
    TODAY = datetime.now()

    @staticmethod
    def ensure_work_dir():
        if not Statics.WORK_DIR.is_dir():
            Statics.WORK_DIR.mkdir()

Statics.ensure_work_dir()


class TimingsOffset:
    TODAY = Statics.TODAY

    def __init__(self):
        self.today = TimingsOffset.TODAY
        self.int = 5
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

    def _update_day_start(self) -> int:
        return timedelta(seconds=self.ts).days

    def _update_day_end(self) -> int:
        return timedelta(seconds=self.ts).days

    def _update_days_ago(self) -> str:
        return f'{self.int} days ago'

    def _update_ts(self):
        return self.dt.timestamp()

    def _update_bdy(self) -> str:
        return self.dt.strftime('%b %d, %Y')

    def _update_ymd(self) -> str:
        return self.dt.strftime('%Y%m%d')

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

timings = TimingsOffset()


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


res = requests.get(timings.url)
txt = res.text

requests_html = pathlib.Path(os.path.join(Statics.WORK_DIR, 'requests_bing.html'))
requests_html.write_text(txt, encoding=Statics.UTF8)


soup_b_results = BeautifulSoup(txt, Statics.PARSER)
b_results = soup_b_results.find(id='b_results')


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


# 'html.parser'
# Each entry is in an LI class called 'b_algo'
soup_li__b_algo = BeautifulSoup(str(b_results), Statics.PARSER)
soupr_algo = soup_li__b_algo.find_all(TagExtract.li__b_algo)


soup_link = BeautifulSoup(str(soupr_algo), Statics.PARSER)
soupr_t = soup_link.find_all(TagExtract.a_link_title)
soupr_d = soup_link.find_all(TagExtract.a_link_desc)


class OutputFormat:
    BEGINS = []
    CONTAINS = ['|']
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
        string = string[len(timings.bdy)+3:]
        string = OutputFormat.entry(string)
        return string

    @staticmethod
    def link(string: str) -> str:
        return URLFormat.from_string(string)


results = []
for i in range(0, len(soupr_t)):
    _continue = False
    title = soupr_t[i]
    desc = soupr_d[i]

    _desc = f'{desc.text}'.strip()
    if _desc.startswith(timings.bdy):
        _continue = True
    else:
        soup_dt = BeautifulSoup(str(title.parent.parent), Statics.PARSER)
        dt = soup_dt.find_all(TagExtract.a_link_news_dt)
        if len(dt) > 0:
            _dt = OutputFormat.entry(dt[0].text)
            if _dt == timings.days_ago:
                _continue = True

    if _continue:
        _desc = OutputFormat.description(_desc)
        _text = OutputFormat.title(title.text)
        _href = OutputFormat.link(title.get('href'))
        results.append(f'{timings.ymd}|{_href}|{_text}|{_desc}')

joined = '\n'.join(results)
print(f'Items: {len(results)}\n\n{joined}')
