import re
import sys
import pathlib
import os
from pprint import pprint

import requests
from urllib.request import urlopen
from urllib.parse import urlencode, quote, urlparse
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


today = datetime.now()
day_start = timedelta(seconds=today.timestamp()).days-5
day_end = timedelta(seconds=today.timestamp()).days-5
url = f'https://www.bing.com/search?q=Tesla&filters=ex1%3a%22ez5_{day_start}_{day_end}%22&qs=n&sp=-1&pq=tesla&sc=10-5&qpvt=Tesla'

# parsed = urlparse(url)


# def create_url(scheme, netloc, path, query):
#     return f'{scheme}://{netloc}{path}?{query}'

# quoted_url = create_url(
#     parsed.scheme,
#     parsed.netloc,
#     parsed.path,
#     quote(parsed.query, safe='=&')
# )

# print(parsed.geturl())
# print(quoted_url)

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
    return tag.name == 'a' and tag.has_attr('h')


def a_link_desc(tag):
    return tag.name == 'p'


soup_li__b_algo = BeautifulSoup(str(b_results), 'html.parser')
soup_li__b_algo_res = soup_li__b_algo.find_all(li__b_algo)


soup_link = BeautifulSoup(str(soup_li__b_algo_res), 'html.parser')
soup_link_title_res = soup_link.find_all(a_link_title)
soup_link_desc_res = soup_link.find_all(a_link_desc)


for i in range(0, len(soup_link_title_res)):
    title = soup_link_title_res[i]
    desc = soup_link_desc_res[i]

    _href = title.get('href')
    _text = title.text
    _desc = desc.text
    print(f'{_text}\n\t{_desc}\nURL: {_href}\n\n')
