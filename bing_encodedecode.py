import sys
import pathlib
import os

import requests
from urllib.parse import quote, urlparse
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


today = datetime.now()
offset = timedelta(days=5)
today_offset = today-offset
today_offset_ft = today_offset.strftime('%Y%m%d')
date_compare = today_offset.strftime('%b %d, %Y')
day_start = timedelta(seconds=today.timestamp()).days-5
day_end = timedelta(seconds=today.timestamp()).days-5
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


soup_b_results = BeautifulSoup(txt, 'html.parser')
b_results = soup_b_results.find(id='b_results')


def li__b_algo(tag):
    return tag.name == 'li' and tag.has_attr('class') and tag.get('class') == ['b_algo']


def a_link_title(tag):
    return tag.name == 'a' and tag.has_attr('h') and tag.parent.name == 'h2'


def a_link_desc(tag):
    return tag.name == 'p'


soup_li__b_algo = BeautifulSoup(str(b_results), 'html.parser')
soup_li__b_algo_res = soup_li__b_algo.find_all(li__b_algo)


soup_link = BeautifulSoup(str(soup_li__b_algo_res), 'html.parser')
soup_link_title_res = soup_link.find_all(a_link_title)
soup_link_desc_res = soup_link.find_all(a_link_desc)


def format_entry(string: str) -> str:
    string = string.strip()

    if string.endswith('…'):
        string = string[:-1].strip()
    if string.endswith('...'):
        string = string[:-3].strip()
    if string.endswith('-'):
        string = string[:-1].strip()

    return string


def _format_title(string: str) -> str:
    string = format_entry(string)
    return string


def _format_desc(string: str) -> str:
    string = string[len(date_compare)+3:]
    string = format_entry(string)
    return string


def _format_href(string: str) -> str:
    string = urlparse(string)
    string = create_url_from_parsed(string)
    return string


results = []
for i in range(0, len(soup_link_title_res)):
    title = soup_link_title_res[i]
    desc = soup_link_desc_res[i]

    _desc = f'{desc.text}'.strip()
    if _desc.startswith(date_compare):
        _desc = _format_desc(_desc)
        _text = _format_title(title.text)
        _href = _format_href(title.get('href'))
        results.append(f'{today_offset_ft}|{_href}|{_text}|{_desc}')

joined = '\n'.join(results)
print(f'Items: {len(results)}\n\n{joined}')
