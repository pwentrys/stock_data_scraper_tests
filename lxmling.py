import pathlib
import os
import sys
import re
import requests
import lxml
import xml


project_path = sys.path[0]
write_dir = pathlib.Path(os.path.join(project_path, 'out'))
if not write_dir.is_dir():
    write_dir.mkdir()


def write_to_file(text, name, extension):
    if type(text) is not type(''):
        text = str(text)

    path = pathlib.Path(os.path.join(str(write_dir), f'{name}.{extension}'))
    path.write_text(text, encoding='utf-8')


def write_texts():
    url = f'https://finance.yahoo.com/quote/TSLA/history?p=TSLA'
    res = requests.get(url)
    write_to_file(res.text, "text", "html")
    write_to_file(res.content, "content", "html")
    write_to_file(res.headers, "headers", "txt")
    write_to_file(res.cookies, "cookies", "txt")
    write_to_file(res.elapsed, "elapsed", "txt")
    write_to_file(res.history, "history", "txt")
    write_to_file(res.encoding, "encoding", "txt")
    write_to_file(res.raw, "raw", "html")


def find_in_text(text, match):
    return True


def _get_text(path):
    return path.read_text(encoding='utf-8')


def _get_texts(path):
    if type(path) is type(''):
        path = pathlib.Path(path)

    texts = {}
    if path.is_dir():
        for item in path.iterdir():
            if item.is_file():
                texts.update({os.path.basename(item): _get_text(item)})
    return texts


url_search = re.compile(r"https://query1.finance.yahoo.com/v7/finance/download/TSLA?period1=(?P<period1>\d+)&period2=(?P<period2>\d+)&interval=(?P<interval>\w+)&events=history&crumb=(?P<crumb>\w+)")


def get_texts():
    texts = _get_texts(write_dir)
    matches = []
    for text in texts.values():
        print(len(text))
        match = url_search.search(text)
        print(match)
        if not (match is None):
            groups = match.groups()
            if len(groups) > 0:
                matches.append(groups)
    print(matches)

get_texts()

