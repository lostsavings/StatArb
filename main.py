import yaml
from itertools import combinations
import os
import pandas as pd
import requests
from datetime import date, timedelta
from sqlalchemy import create_engine, URL


def get_psql_config():
    config_path = os.path.join('configs', 'psql.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


PSQL_CONFIG = get_psql_config()


def get_db_con():
    url = URL.create(
        "postgresql+psycopg2",
        **PSQL_CONFIG
    )
    return create_engine(url, echo=True).connect()


def get_history(ticker):
    """Pull ticker history from ORAT api."""
    url = 'https://api.orats.io/datav2/hist/cores'
    params = {
        'token': '8ea8d461-2ce6-4bac-bf67-3f24647efbad',
        'ticker': ticker,
        # TODO: add trade dates?
        'fields': 'ticker,tradeDate,iv30d,mktWidth,sector,sectorName'
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


def get_ts(df_full: pd.DataFrame, ticker: str, start_date: date):
    """Get a dataframe with two columns, tradeDate and iv30d, since start_date, ordered by date."""
    df = df_full[df_full.ticker == ticker]
    df = df[df['tradeDate'] >= start_date.isoformat()]
    df = df.sort_values('tradeDate')
    df = df.reset_index(drop=True)
    return df[['tradeDate', 'iv30d']]


def n_day_correlation(df_full, ticker_a, ticker_b, days):
    """Get the n day pearson correlation for two tickers."""
    start_date = date.today() - timedelta(days=days)
    df_ts_a = get_ts(df_full, ticker_a, start_date)
    df_ts_b = get_ts(df_full, ticker_b, start_date)
    df = df_ts_a.merge(df_ts_b, on='tradeDate')
    df.drop(['tradeDate'], axis=1, inplace=True)
    corr = df['iv30d_x'].corr(df['iv30d_y'])
    return corr


def main():
    tickers = get_tickers()
    df_full_path = os.path.join('output', 'full.csv')

    if not os.path.exists(df_full_path):
        df_full = pd.DataFrame()
        for ticker in tickers:
            history_path = os.path.join('output', f'orat_api_result_{ticker}.csv')

            if not os.path.exists(history_path):
                # we do not have today's data, fetch it
                history = get_history(ticker)
                df = pd.DataFrame(history)
                df.to_csv(history_path, index=False)
            else:
                df = pd.read_csv(history_path)

            df_full = pd.concat([df_full, df])

        df_full.to_csv(df_full_path, index=False)
    else:
        df_full = pd.read_csv(df_full_path)

    with get_db_con() as con:
        df_full.to_sql('history', con, if_exists='replace', index=False)

    tickers = list(df_full.ticker.unique())
    # : uncomment this for sanity check
    # tickers = ['AA', 'GOOG']

    tickers_product = combinations(tickers, r=2)

    df_corr = pd.DataFrame()
    for ticker_a, ticker_b in tickers_product:
        if ticker_a == ticker_b:
            continue
        print (f"{ticker_a},{ticker_b}")
        corr = n_day_correlation(df_full, ticker_a, ticker_b, 60)
        df_new = pd.DataFrame([{
            'ticker_a': ticker_a,
            'ticker_b': ticker_b,
            'corr': corr
        }])
        df_corr = pd.concat([df_corr, df_new])

    corr_path = os.path.join('output', 'corr.csv')
    df_corr.to_csv(corr_path, index=False)

    with get_db_con() as con:
        df_corr.to_sql('corr', con, if_exists='replace', index=False)


if __name__ == '__main__':
    main()