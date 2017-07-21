import os
import pathlib

import datetime

datas = {
    'Arca_Biopharma': {
        'symbol': 'ABIO',
        'days': 3105,
        'pages': 1
    },
    'AMD': {
        'symbol': 'AMD',
        'days': 14428,
        'pages': 3
    },
    'Apple': {
        'symbol': 'AAPL',
        'days': 6756,
        'pages': 3
    },
    'Preferred_Apartment_Communities': {
        'symbol': 'APTS',
        'days': 2375,
        'pages': 1
    },
    'Cisco_Systems': {
        'symbol': 'CSCO',
        'days': 10045,
        'pages': 3
    },
    'Dow_Chemical_Co': {
        'symbol': 'DOW',
        'days': 14428,
        'pages': 1
    },
    'Creative_Edge_Nutrition_Inc': {
        'symbol': 'FITX',
        'days': 2740,
        'pages': 1
    },
    'General_Electric_Company': {
        'symbol': 'GE',
        'days': 14428,
        'pages': 3
    },
    'Golden_River_Resources_Corporation': {
        'symbol': 'GORV',
        'days': 2740,
        'pages': 1
    },
    'Johnson_and_Johnson': {
        'symbol': 'JNJ',
        'days': 14428,
        'pages': 1
    },
    'iRobot': {
        'symbol': 'IRBT',
        'days': 5000,
        'pages': 3
    },
    'Microsoft': {
        'symbol': 'MSFT',
        'days': 6756,
        'pages': 3
    },
    'Nvidia': {
        'symbol': 'NVDA',
        'days': 6756,
        'pages': 3
    },
    'Reaves_Utility_Income_Fund': {
        'symbol': 'UTG',
        'days': 4932,
        'pages': 1
    },
    'SpaceX': {
        'symbol': 'SPACEX',
        'days': 3000,
        'pages': 3
    },
    'Tesla': {
        'symbol': 'TSLA',
        'days': 3000,
        'pages': 3
    },
    'Virtus_Oil_and_Gas_Corp': {
        'symbol': 'VOIL',
        'days': 1644,
        'pages': 1
    },
    'Westport_Fuel_Systems_Inc': {
        'symbol': 'WPRT',
        'days': 1644,
        'pages': 1
    },
    'WindStream_Tech_RG': {
        'symbol': 'WSTI',
        'days': 1380,
        'pages': 1
    },
}

dest = os.path.realpath(__file__)
root = pathlib.Path(dest).parent
csv_path = os.path.join(root, 'stocks.csv')
print(root)
print(csv_path)

lines = []
for dkey in datas:
    data = datas[dkey]
    symbol = data['symbol']
    days = data['days']
    days = datetime.datetime.now() - datetime.timedelta(days=days)

    if days.year < 1970:
        while days.year < 1970:
            days += datetime.timedelta(days=365)

    if days.month != 1:
        while days.month != 1:
            days -= datetime.timedelta(days=1)

    if days.day != 1:
        while days.day != 1:
            days -= datetime.timedelta(days=1)

    if days.hour != 0:
        while days.hour != 0:
            days -= datetime.timedelta(hours=1)

    if days.minute != 0:
        while days.minute != 0:
            days -= datetime.timedelta(minutes=1)

    if days.second != 0:
        while days.second != 0:
            days -= datetime.timedelta(seconds=1)

    days_int = int(days.timestamp()/60/60/24)
    pages = data['pages']
    # ,{datetime.datetime.fromtimestamp(days.timestamp())}
    lines.append(f'{days_int},{dkey},{symbol},{pages}')

lines = sorted(lines, key=lambda x: int(x.split(',')[0]))
csv_path = pathlib.Path(csv_path)
csv_path.write_text('\n'.join(lines), encoding='utf-8')
