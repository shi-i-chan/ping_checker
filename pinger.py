import os
import re
import time
import numpy as np
import pandas as pd
from datetime import datetime

from pinger_chart import plot

from typing import NoReturn


def get_latency(url: str) -> float:
    response = os.popen(f'ping -n 1 {url}')
    last_line = response.readlines()[-1]
    regex = re.compile(r'Average = (\d*)')
    find = regex.findall(last_line)
    if len(find) > 0:
        return float(find[0])
    else:
        return np.nan


def save_data(data: dict) -> NoReturn:
    new_df = pd.DataFrame(data)
    old_df = pd.read_csv(fn, index_col=0)
    df = pd.concat([old_df, new_df]).reset_index(drop=True)
    df.to_csv(fn)


def start() -> NoReturn:
    counter = 0
    data = {
        'date': [],
        'google': [],
        'wiki': [],
        'youtube': []
    }

    if not os.path.isfile(fn):
        pd.DataFrame(columns=list(data.keys())).to_csv(fn)

    while True:
        try:
            counter += 1
            date = datetime.fromtimestamp(time.time())
            data['date'].append(date)
            print(date)
            for key, url in urls.items():
                latency = get_latency(url)
                print('    ', key, latency)
                data[key].append(latency)

            if counter % SAVE_EVERY == 0:
                save_data(data)
                plot(fn)
                counter = 0
                data = {'date': [], 'google': [], 'wiki': [], 'youtube': []}
            time.sleep(SLEEP)
        except Exception as e:
            print(e)


fn = 'latency.csv'
SAVE_EVERY = 50
SLEEP = 10

urls = {
    'google': 'google.com',
    'wiki': 'wikipedia.org',
    'youtube': 'youtube.com',
}

start()
