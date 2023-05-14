import os
import pandas as pd
import requests
import datetime
from tqdm import tqdm


def get_date_data(date: datetime.date):
    """Pull ticker history from ORAT api."""
    url = 'https://api.orats.io/datav2/hist/cores'
    params = {
        'token': '8ea8d461-2ce6-4bac-bf67-3f24647efbad',
        'tradeDate': date.isoformat(),
        'fields': 'ticker,tradeDate,orIvXern20d,mktWidthVol,sector,sectorName'
    }
    res = requests.get(url, params=params)
    res.raise_for_status()
    return res.json()['data']


def get_tickers():
    """Load list of tickers to fetch data for."""
    with open('tickers.txt', 'r') as f:
        tickers = [e.strip() for e in f.readlines()]
        # prevent duplicates
        return list(set(tickers))


def fetch_data():
    tickers = get_tickers()
    df_full = pd.DataFrame()

    today = datetime.date.today()
    # how many days of history to fetch
    history_length = 60
    for i in tqdm(range(history_length)):
        date = today - datetime.timedelta(days=i)
        try:
            history = get_date_data(date)
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                # 404s are generally ok, we just don't have data for that day
                continue
            else:
                raise e
        df = pd.DataFrame(history)
        df_full = pd.concat([df_full, df])

    df_full = df_full[df_full['ticker'].isin(tickers)].reset_index(drop=True)
    df_full.to_csv(os.path.join('output', 'full.csv'), index=False)


if __name__ == '__main__':
    fetch_data()
