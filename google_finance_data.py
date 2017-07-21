import os
import pathlib
import requests
import sys
from bs4 import BeautifulSoup
from datetime import datetime


today = datetime.now()
month = today.strftime('%b')
today_formatted = f'{month}+{int(today.day)}%2C+{today.year}'
output_format = 'csv'

cids = {
    'AAPL': 22144,
    'ABIO': 660731,
    'AMD': 327,
    'APTS': 10691360,
    'CC': 681339,
    'CSCO': 99624,
    'DD': 10261,
    'DOW': 983582,
    'FITX': 729731,
    'GE': 14135,
    'GORV': 38213,
    'IRBT': 701970,
    'IRT': 236803873679290,
    'JNJ': 666601,
    'MSFT': 358464,
    'NVDA': 662925,
    'TSLA': 12607212,
    'UTG': 696997,
    'VOIL': 15405086,
    'WPRT': 729542,
    'WSTI': 1115179957885739,
}


def get_historical_url(uid, form):
    return f'http://www.google.com/finance/historical?' \
           f'cid={uid}&' \
           f'startdate=Jan+1%2C+1970&' \
           f'enddate={today_formatted}&' \
           f'output={form}'


def get_historical_csv(uid, form):
    res = requests.get(get_historical_url(uid, form))
    return res.text


def format_year(string):
    year = int(string)
    if year <= 17:
        year += 100
    year += 1900
    return f'{year}'


def format_day(string):
    if len(string) == 1:
        return f'0{string}'
    return string


def _format_line(string: str) -> str:
    string_split = string.split(',')
    date = string_split[0]
    date_split = date.split('-')
    date_split[0] = format_day(date_split[0])
    date_split[2] = format_year(date_split[2])
    date_combined = ''.join(date_split)
    date_formatted = datetime.strptime(date_combined, '%d%b%Y')
    string_split[0] = date_formatted.strftime('%Y%m%d')
    joined_split = ''.join([f'{item},' for item in string_split])
    joined_split = joined_split[:-1]
    return f"{joined_split}"

    
def _format_lines(string_list: list) -> list:
    return [_format_line(line) for line in string_list]


def _run(stock, uid, form):
    text = get_historical_csv(uid, form)
    data_split = text.splitlines()
    headers = data_split[0]
    texts = data_split[1:-1]
    new_texts = _format_lines(texts)
    new_text = '\n'.join(sorted(set(new_texts)))
    new_text = f'{headers}\n{new_text}'
    path = pathlib.Path(sys.path[0])
    path_data = pathlib.Path(os.path.join(path, 'data'))
    if not path_data.is_dir():
        path_data.mkdir()
    write_path = pathlib.Path(os.path.join(path_data, f'{stock}.{form}'))
    write_path.write_text(new_text, encoding='utf-8')


def run():
    keys = cids.keys()
    for key in keys:
        _run(key, cids.get(key), output_format)


run()
