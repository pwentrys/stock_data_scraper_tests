import sys
import pathlib
import os

import requests
from urllib.parse import quote, urlparse
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


today = datetime.now()

offset_int = 5
offset = timedelta(days=offset_int)
today_offset = today-offset
today_offset_ft = today_offset.strftime('%Y%m%d')
date_compare = today_offset.strftime('%b %d, %Y')
days_ago_compare = f'{offset_int} days ago'
day_start = timedelta(seconds=today.timestamp()).days-offset_int
day_end = timedelta(seconds=today.timestamp()).days-offset_int
url = f'https://www.bing.com/search?q=Tesla&filters=ex1%3a%22ez5_{day_start}_{day_end}%22&qs=n&sp=-1&pq=tesla&sc=10-5&qpvt=Tesla'


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


class Statics:
    PARSER = 'html5lib'
    UTF8 = 'utf-8'
    SYSPATH = sys.path[0]
    HTMLS = 'htmls'
    WORK_DIR = pathlib.Path(os.path.join(SYSPATH, HTMLS))

    @staticmethod
    def ensure_work_dir():
        if not Statics.WORK_DIR.is_dir():
            Statics.WORK_DIR.mkdir()

Statics.ensure_work_dir()

res = requests.get(url)
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
        string = string[len(date_compare)+3:]
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
    if _desc.startswith(date_compare):
        _continue = True
    else:
        soup_dt = BeautifulSoup(str(title.parent.parent), Statics.PARSER)
        dt = soup_dt.find_all(TagExtract.a_link_news_dt)
        if len(dt) > 0:
            _dt = OutputFormat.entry(dt[0].text)
            if _dt == days_ago_compare:
                _continue = True

    if _continue:
        _desc = OutputFormat.description(_desc)
        _text = OutputFormat.title(title.text)
        _href = OutputFormat.link(title.get('href'))
        results.append(f'{today_offset_ft}|{_href}|{_text}|{_desc}')

joined = '\n'.join(results)
print(f'Items: {len(results)}\n\n{joined}')
