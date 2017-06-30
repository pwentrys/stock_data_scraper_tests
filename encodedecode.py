import re
import sys
import pathlib
import os
from pprint import pprint

import requests
from urllib.request import urlopen
from urllib.parse import urlencode, quote, urlparse
from bs4 import BeautifulSoup


url = f'https://www.google.com/search?q=Tesla&safe=off&biw=1922&bih=1008&source=lnt&tbs=cdr:1&cd_min=6/28/2017&cd_max=6/28/2017&tbm=nws'
gen = f'https://www.google.com/search?q=Tesla&safe=off&biw=1922&bih=1008&source=lnt&tbs=cdr%3A1%2Ccd_min%3A6%2F28%2F2017%2Ccd_max%3A6%2F28%2F2017&tbm=nws'
man = f'https://www.google.com/search?q=Tesla&safe=off&biw=1922&bih=1008&source=lnt&tbs=sbd%3A1%2Ccdr%3A1%2Ccd_min%3A6%2F28%2F2017%2Ccd_max%3A6%2F28%2F2017&tbm=nws'
#     f'https://www.google.com/search?q=Tesla&safe=off&biw=1922&bih=1008&source=lnt&tbs=cdr%3A1%2Ccd_min%3A6%2F28%2F2017%2Ccd_max%3A6%2F28%2F2017&tbm='

#
parsed = urlparse(url)


def create_url(scheme, netloc, path, query):
    return f'{scheme}://{netloc}{path}?{query}'

quoted_url = create_url(
    parsed.scheme,
    parsed.netloc,
    parsed.path,
    quote(parsed.query, safe='=&')
)

# print(parsed.geturl())
print(quoted_url)

res = requests.get(quoted_url)
work_dir = pathlib.Path(os.path.join(sys.path[0], 'htmls'))
if not work_dir.is_dir():
    work_dir.mkdir()

requests_html = pathlib.Path(os.path.join(work_dir, 'requests.html'))
requests_html.write_text(res.text, encoding='utf-8')

res_raw = requests.get(url)
requests_raw_html = pathlib.Path(os.path.join(work_dir, 'requests_raw.html'))
requests_raw_html.write_text(res_raw.text, encoding='utf-8')

res_gen = requests.get(gen)
requests_gen_html = pathlib.Path(os.path.join(work_dir, 'requests_gen.html'))
requests_gen_html.write_text(res_gen.text, encoding='utf-8')

urllib_html = pathlib.Path(os.path.join(work_dir, 'urllib.html'))
urllibopen_html = urlopen(quoted_url)
print(dir(urllibopen_html))
urllib_html.write_text(urllibopen_html.read(), encoding='utf-8')
# print(res)
# print(res.apparent_encoding)
# print(res.content)
# print(res.links)
# print(res.ok)
# print(res.text)


def class_g(tag):
    # pprint(dir(tag))
    # print(f'name: {tag.name}')
    # print(f'namespace: {tag.namespace}')
    if tag.name == 'a' and tag.has_attr('class'):
        print(tag)
    return tag.name == 'a' and tag.has_attr('class') and (tag.get('class').__contains__('l _PMs') or tag.get('class').__contains__('_pJs'))
    # and tag.get('class') == ['rc']
    # and tag.get('class') == 'g'


print('')
print(res.content)
print('')
txt = res.content.decode(res.encoding)
if txt.__contains__('TheStreet'):
    print("FOOL EXISTS")
else:
    print("NO FOOL")
soup = BeautifulSoup(txt, 'html.parser')
res = soup.find_all(class_g)
pprint(res)
# divs = soup.find(id='res')
# print(divs)
# divs_soup = BeautifulSoup(str(divs), 'html.parser')
# h3s = divs_soup.find_all('h3')
# pprint(h3s)
# res = soup.find_all(class_g)
# print(res)
# print(len(res))
