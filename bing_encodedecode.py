import requests
import time

from utils.OutputFormats import OutputFormats
from utils.SoupTags import SoupTags
from utils.Statics import Statics
from utils.TSVer import TSVer
from utils.Timings import Timings
from utils.TimingsOffset import TimingsOffset


data = {
    'AMD': {
        'symbol': 'AMD',
        'days': 14428
    },
    'Apple': {
        'symbol': 'AAPL',
        'days': 6756
    },
    'iRobot': {
        'symbol': 'IRBT',
        'days': 5000
    },
    'Microsoft': {
        'symbol': 'MSFT',
        'days': 6756
    },
    'Nvidia': {
        'symbol': '6756',
        'days': 6756
    },
    'SpaceX': {
        'symbol': 'SPACEX',
        'days': 3000
    },
    'Tesla': {
        'symbol': 'TSLA',
        'days': 3000
    },
    'active': 'Apple'
}

active = data['active']
data = data[active]
Statics.ensure_dirs()
timings_offset = TimingsOffset(active)
timer = Timings()
tsver = TSVer(data['symbol'])


def _get_stripped_item(div):
    try:
        stripped = div.p.text.strip()
    except Exception as error:
        stripped = div
        print(error)
        # print(dir(stripped))
        # print(f'stripped: {stripped}\n{error}')
    return stripped


def run_item(string: str, stripped) -> bool:
    try:
        if stripped.startswith(timings_offset.bdy):
            return True
        else:
            b_dt = SoupTags.using_type_and_class_one(string, 'span', 'news_dt')
            if b_dt is not None:
                dt = OutputFormats.entry(b_dt.text)
                if dt == timings_offset.days_ago:
                    return True
    except Exception as error:
        print(f'{error}')
    return False


def run(offset_start: int, offset_end: int, pages: int):
    """
    # TODO Split this apart.
    :param offset_start:
    :param offset_end:
    :param pages:
    """
    timer.estimate_duration(offset_end - offset_start, pages)
    timer.start_logged()
    current_runs = 0
    counter_items = 0
    sleep_time = timer.SLEEP_TIME
    final_results = []
    for i in range(offset_start, offset_end):
        timings_offset.update_num(i)
        for j in range(0, pages):
            current_runs += 1
            timer.operation_logged()
            time.sleep(sleep_time)
            res = requests.get(timings_offset.url_with_first_offset(j))
            text = res.text

            # requests_html = pathlib.Path(os.path.join(Statics.WORK_DIR, 'requests_bing.html'))
            # requests_html.write_text(text, encoding=Statics.UTF8)

            b_results = SoupTags.using_type_and_id(text, 'ol', 'b_results')
            b_algo = SoupTags.using_type_and_class(str(b_results), 'li', 'b_algo')

            for item in b_algo:
                _desc = _get_stripped_item(item)
                item_str = str(item)
                if run_item(item_str, _desc):
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
            tsver.append_current(final_results)
            counter_items = 0

    if len(final_results) > 0:
        tsver.append_current(final_results)

    timer.stop_logged()


if __name__ == '__main__':
    run(0, data['days'], 3)
