import os
import pathlib
import requests
import sys
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


today = datetime.now()
month = today.strftime('%b')
today_formatted = f'{month}+{int(today.day)}%2C+{today.year}'

cids = {
    'TSLA': 12607212,
    'IRBT': 701970,
    'NVDA': 662925
}

output_format = 'csv'
active_stock = 'NVDA'  # 'TSLA'


def get_historical_url():
    return f'http://www.google.com/finance/historical?cid={cids[active_stock]}&startdate=Jan+1%2C+1970&enddate={today_formatted}&output={output_format}'


def get_historical_csv():
    res = requests.get(get_historical_url())
    return res.text

# result = get_crumb()
# soup = BeautifulSoup(result, 'html.parser')
# pprint(soup.find_all('a'))
text = get_historical_csv()
data_split = text.splitlines()
headers = data_split[0]
texts = data_split[1:-1]
new_texts = []
for line in texts:
    line_split = line.split(',')
    date = line_split[0]
    date_split = date.split('-')
    if len(date_split[0]) == 1:
        date_split[0] = f'0{date_split[0]}'
    date_split[2] = int(date_split[2])
    if date_split[2] > 17:
        date_split[2] += 1900
    else:
        date_split[2] += 2000
    date_split[2] = f'{date_split[2]}'
    date_combined = ''.join(date_split)
    date_formatted = datetime.strptime(date_combined, '%d%b%Y')
    date_yyyymmdd = date_formatted.strftime('%Y%m%d')
    line_split[0] = date_yyyymmdd
    line_split = [f'{item},' for item in line_split]
    line_split[len(line_split)-1] = line_split[len(line_split)-1][:-1]
    joined_split = ''.join(line_split)
    new_texts.append(f"{joined_split}")
new_text = '\n'.join(sorted(set(new_texts)))
new_text = f'{headers}\n{new_text}'
path = pathlib.Path(sys.path[0])
path_data = pathlib.Path(os.path.join(path, 'data'))
if not path_data.is_dir():
    path_data.mkdir()
write_path = pathlib.Path(os.path.join(path_data, f'{active_stock}.{output_format}'))
write_path.write_text(new_text, encoding='utf-8')
