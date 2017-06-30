import os
import pathlib
import requests
import time

from utils.OutputFormats import OutputFormats
from utils.SoupTags import SoupTags
from utils.Statics import Statics
from utils.TSVer import TSVer
from utils.Timings import Timings
from utils.TimingsOffset import TimingsOffset

Statics.ensure_dirs()
timings_offset = TimingsOffset()
timer = Timings()
tsver = TSVer('TSLA')


def run(offset_start: int, offset_end: int, pages: int):
    timer.estimate_duration(offset_end - offset_start, pages)
    timer.start_logged()
    current_runs = 0
    counter_items = 0
    final_results = []
    for i in range(offset_start, offset_end):
        timings_offset.int = i
        timings_offset.update()
        for j in range(0, pages):
            current_runs += 1
            timer.operation_logged()
            time.sleep(Statics.SLEEP_TIME)
            res = requests.get(timings_offset.url_with_first_offset(j))
            text = res.text

            requests_html = pathlib.Path(os.path.join(Statics.WORK_DIR, 'requests_bing.html'))
            requests_html.write_text(text, encoding=Statics.UTF8)

            b_results = SoupTags.using_type_and_id(text, 'ol', 'b_results')
            b_algo = SoupTags.using_type_and_class(str(b_results), 'li', 'b_algo')

            for _item in b_algo:
                item = str(_item)
                _continue = False
                _desc = f'{_item.div.p.text}'.strip()
                if _desc.startswith(timings_offset.bdy):
                    _continue = True
                else:
                    b_dt = SoupTags.using_type_and_class_one(item, 'span', 'news_dt')
                    if b_dt is not None:
                        _dt = OutputFormats.entry(b_dt.text)
                        if _dt == timings_offset.days_ago:
                            _continue = True

                if _continue:
                    title = SoupTags.using_h_re_compile(item, 'ID=SERP,')
                    _text, _desc, _href = OutputFormats.get_result(
                        title.text,
                        _desc.replace(timings_offset.bdy, ''),
                        title.get('href')
                    )
                    final_results.append(f'{timings_offset.ymd}|{_href}|{_text}|{_desc}')
                    counter_items += 1

        if counter_items > 10:
            counter_items = 0
            tsver.append_current(final_results)

    if len(final_results) > 0:
        tsver.append_current(final_results)

    timer.stop_logged()

if __name__ == '__main__':
    run(0, 3, 3)

