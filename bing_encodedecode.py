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


def create_url(scheme, netloc, path, query):
    if query == '':
        return f'{scheme}://{netloc}{path}'
    else:
        return f'{scheme}://{netloc}{path}?{query}'


def create_url_from_parsed(parsed_url):
    return create_url(parsed_url.scheme, parsed_url.netloc, parsed_url.path, quote(parsed_url.query, safe='=&'))


print(f'URL: {url}')
res = requests.get(url)
txt = res.text
work_dir = pathlib.Path(os.path.join(sys.path[0], 'htmls'))
if not work_dir.is_dir():
    work_dir.mkdir()

requests_html = pathlib.Path(os.path.join(work_dir, 'requests_bing.html'))
requests_html.write_text(txt, encoding='utf-8')


parser_string = 'html5lib'
soup_b_results = BeautifulSoup(txt, parser_string)
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
soup_li__b_algo = BeautifulSoup(str(b_results), parser_string)
soupr_algo = soup_li__b_algo.find_all(TagExtract.li__b_algo)


soup_link = BeautifulSoup(str(soupr_algo), parser_string)
soupr_t = soup_link.find_all(TagExtract.a_link_title)
soupr_d = soup_link.find_all(TagExtract.a_link_desc)
#  soupr_dt = soup_link.find_all(TagExtract.a_link_news_dt)


_format_entries_list = ['…', '...', '-']


def _format_entry(string: str) -> str:
    string = string.strip()

    for item in _format_entries_list:
        if string.endswith(item):
            string = string[:-len(item)].strip()
    if string.__contains__('|'):
        string = string.replace('|', '').strip()

    return string


def _format_title(string: str) -> str:
    string = _format_entry(string)
    return string


def _format_desc(string: str) -> str:
    string = string[len(date_compare)+3:]
    string = _format_entry(string)
    return string


def _format_href(string: str) -> str:
    string = urlparse(string)
    string = create_url_from_parsed(string)
    return string


results = []
for i in range(0, len(soupr_t)):
    _continue = False
    title = soupr_t[i]
    desc = soupr_d[i]

    _desc = f'{desc.text}'.strip()
    if _desc.startswith(date_compare):
        _continue = True
    else:
        soup_dt = BeautifulSoup(str(title.parent.parent), parser_string)
        dt = soup_dt.find_all(TagExtract.a_link_news_dt)
        if len(dt) > 0:
            _dt = _format_entry(dt[0].text)
            if _dt == days_ago_compare:
                _continue = True

    if _continue:
        _desc = _format_desc(_desc)
        _text = _format_title(title.text)
        _href = _format_href(title.get('href'))
        results.append(f'{today_offset_ft}|{_href}|{_text}|{_desc}')

joined = '\n'.join(results)
print(f'Items: {len(results)}\n\n{joined}')
