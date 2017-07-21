import os
import pathlib

import datetime
import requests
import time

from models.stocks import Stocks
from utils.DateTimeFormats import DTFormats
from utils.OutputFormats import OutputFormats
from utils.SoupTags import SoupTags
from utils.Statics import Statics
from utils.TSVer import TSVer
from utils.Timings import Timings
from utils.TimingsOffset import TimingsOffset


path = os.path.join(Statics.SYSPATH, Statics.MODELS)
path = os.path.join(path, Statics.STOCKS)
path = pathlib.Path(path)

if not path.is_file():
    path = path.write_text('', encoding='utf-8')

stocks = Stocks(path.read_text())
Statics.ensure_dirs()


def _get_stripped_item(div):
    try:
        stripped = div.p.text.strip()
    except Exception as error:
        stripped = div
        print(error)
    return stripped


def run_item(string: str, stripped, timings_offset) -> bool:
    try:
        print(f'CHECK - STRING: {string}')
        print(f'CHECK - STRIPPED: {stripped}')
        print(f'Offset Body: {timings_offset.bdy}')
        if stripped.startswith(timings_offset.bdy):
            print(f'RETURNING TRUE')
            return True
        else:
            b_dt = SoupTags.using_type_and_class_one(string, 'span', 'news_dt')
            if b_dt is not None:
                dt = OutputFormats.entry(b_dt.text)
                if dt == timings_offset.days_ago:
                    print(f'RETURNING TRUE')
                    return True
    except Exception as error:
        print(f'{error}')
    print(f'RETURNING FALSE')
    return False


def _run(offset_start: int, offset_end: int, pages: int, symbol, stock_name):
    """
    # TODO Split this apart.
    :param offset_start:
    :param offset_end:
    :param pages:
    """
    timer = Timings()
    tsver = TSVer(symbol)
    timings_offset = TimingsOffset(stock_name)
    if type(pages) != type(int):
        pages = int(pages)
    timer.estimate_duration(offset_end - offset_start, pages)
    timer.start_logged()
    current_runs = 0
    counter_items = 0
    sleep_time = timer.SLEEP_TIME
    final_results = []
    print(f'offset_start: {offset_start}')
    print(f'offset_end: {offset_end}')
    for _i in range(offset_start, offset_end):
        i = _i + 1
        __counter = i
        print(f'RUNNING I: {__counter}')
        timings_offset.update_num(_i)
        for j in range(0, pages):
            current_runs += 1
            timer.operation_logged()
            time.sleep(sleep_time)
            get_url = timings_offset.url_with_first_offset(j)
            print(f'URL: {get_url}\nTS: {i*60*60*24}\nI: {i}')
            res = requests.get(get_url)
            text = res.text

            # requests_html = pathlib.Path(os.path.join(Statics.WORK_DIR, 'requests_bing.html'))
            # requests_html.write_text(text, encoding=Statics.UTF8)

            b_results = SoupTags.using_type_and_id(text, 'ol', 'b_results')
            b_algo = SoupTags.using_type_and_class(str(b_results), 'li', 'b_algo')

            for item in b_algo:
                _desc = _get_stripped_item(item)
                item_str = str(item)
                item_str = item_str.replace(' H=', ' h=')
                if run_item(item_str, _desc, timings_offset):
                    try:
                        title = SoupTags.using_h_re_compile(item_str, 'ID=SERP,')
                        _text, _desc, _href = OutputFormats.get_result(
                            title.text,
                            _desc.replace(timings_offset.bdy, ''),
                            title.get('href')
                        )
                        final_results.append(f'{timings_offset.ymd}|{_href}|{_text}|{_desc}')
                        counter_items += 1
                    except Exception as error:
                        print(error)

        if counter_items > 50:
            print(f'Adding {counter_items} for {symbol}.')
            tsver.append_current(final_results)
            counter_items = 0

    if len(final_results) > 0:
        print(f'Adding {len(final_results)} for {symbol}.')
        tsver.append_current(final_results)

    timer.stop_logged()


def get_today():
    dt = datetime.datetime.now() - datetime.timedelta(days=1)

    if dt.year < 1970:
        while dt.year < 1970:
            dt += datetime.timedelta(days=365)

    if dt.hour != 0:
        while dt.hour != 0:
            dt -= datetime.timedelta(hours=1)

    if dt.minute != 0:
        while dt.minute != 0:
            dt -= datetime.timedelta(minutes=1)

    if dt.second != 0:
        while dt.second != 0:
            dt -= datetime.timedelta(seconds=1)

    return int(dt.timestamp()/60/60/24)


def run():
    _stocks = stocks.stocks
    today = get_today()
    for stock in _stocks:
        symbol = stock.symbol
        path = pathlib.Path(os.path.join(Statics.DATA_DIR, f'{symbol}.tsv'))
        if not path.is_file():
            # print(
            #     f'Day: {stock.day}\n'
            #     f'Today-1: {today - 1}\n'
            #     f'Pages: {stock.pages}\n'
            #     f'Symbol: {stock.symbol}\n'
            #     f'Display: {stock.display}'
            # )
             _run(stock.day, today, stock.pages, stock.symbol, stock.display)
        else:
            data = path.read_text(encoding='utf-8')
            data_split = data.splitlines()
            data_split = sorted(data_split, key=lambda x: int(x.split('|')[0]))
            data_joined = '\n'.join(data_split)
            if data_joined != data:
                path.write_text(data_joined, encoding='utf-8')

            dt_max = data_split[len(data_split)-1]
            dt_max = dt_max.split('|')[0]
            dt_max = datetime.datetime.strptime(dt_max, DTFormats.YMD)
            dt_max = dt_max.timestamp()/60/60/24
            dt_max = int(dt_max)
            if dt_max < today and today - dt_max != 0:
                print(
                    f'Day: {dt_max}\n'
                    f'Today-1: {today}\n'
                    f'Pages: {stock.pages}\n'
                    f'Symbol: {stock.symbol}\n'
                    f'Display: {stock.display}'
                )
                _run(dt_max, today, stock.pages, stock.symbol, stock.display)
            else:
                print(f'No need to run {stock.symbol}.')


if __name__ == '__main__':
    run()
