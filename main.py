import os
import pandas as pd
import requests
from datetime import date, timedelta


def get_history(tickers):
    """Pull ticker history from ORAT api."""
    tickers_fmt = ','.join(tickers)
    url = 'https://api.orats.io/datav2/hist/cores'
    params = {
        'token': '8ea8d461-2ce6-4bac-bf67-3f24647efbad',
        'ticker': tickers_fmt,
        # TODO: add trade dates?
        'fields': 'ticker,tradeDate,iv30d,mktWidth'
    }
    res = requests.get(url, params=params)
    res.raise_for_status()
    return res.json()['data']


def get_tickers():
    """Load list of tickers to fetch data for."""
    with open('tickers.txt', 'r') as f:
        return [e.strip() for e in f.readlines()]


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
    print(df)
    df.drop(['tradeDate'], axis=1, inplace=True)
    corr = df['iv30d_x'].corr(df['iv30d_y'])
    return corr


def main():
    today = date.today()
    history_path = os.path.join('output', f'orat_api_result_{today}.csv')

    if not os.path.exists(history_path):
        # we do not have today's data, fetch it
        tickers = get_tickers()
        history = get_history(tickers)
        df = pd.DataFrame(history)
        df.to_csv(history_path, index=False)
    else:
        # we do have today's data, load it from disk
        df = pd.read_csv(history_path)
    
    print(n_day_correlation(df, 'AA', 'AAPL', 60))

if __name__ == '__main__':
    main()