import requests
from pprint import pprint
from bs4 import BeautifulSoup


initial_url = f'https://finance.yahoo.com/quote/TSLA/history?p=TSLA'
crumb_url = 'http://query2.finance.yahoo.com/v1/test/getcrumb'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'en-US,en;q=0.5',
    'connection': 'keep-alive',
    'upgrade-insecure-requests': '1'
}


def get_url(offset):
    offset = offset * 30
    return f'http://www.google.com/finance/historical?cid=12607212&startdate=Jun+1%2C+2009&enddate=Jun+29%2C+2017&num=30&start={offset}&output=csv'


def get_crumb():
    res = requests.get(initial_url, headers)
    return res.content

result = get_crumb()
soup = BeautifulSoup(result, 'html.parser')
pprint(soup.find_all('a'))
