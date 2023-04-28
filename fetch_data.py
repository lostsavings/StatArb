import os
import click
import pandas as pd
import requests

from db import get_db_con


def get_history(ticker):
    """Pull ticker history from ORAT api."""
    url = 'https://api.orats.io/datav2/hist/cores'
    params = {
        'token': '8ea8d461-2ce6-4bac-bf67-3f24647efbad',
        'ticker': ticker,
        # TODO: add trade dates?
        'fields': 'ticker,tradeDate,iv30d,mktWidthVol,sector,sectorName'
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


@click.command()
@click.option('--save-db', is_flag=True, help='Set this flag to save results to the database')
def fetch_data(save_db):
    tickers = get_tickers()
    df_full = pd.DataFrame()
    for ticker in tickers:
        history = get_history(ticker)
        df = pd.DataFrame(history)
        df_full = pd.concat([df_full, df])

    if save_db:
        with get_db_con() as con:
            df_full.to_sql('history', con, if_exists='replace', index=False)

    df_full.to_csv(os.path.join('output', 'full.csv'))


if __name__ == '__main__':
    fetch_data()
