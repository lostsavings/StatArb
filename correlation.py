import os
import pandas as pd
from datetime import timedelta


def format_tickers(r):
    """
    Create a string of "ticker_a,ticker_b" (tickers ordered alphabetically) for a given row.
    Used to drop duplicate combos after df.corr.
    """
    ordered = [r.ticker_a, r.ticker_b]
    ordered.sort()
    return ','.join(ordered)


default_correlation_window = 120


def get_correlation(n_days: int = default_correlation_window) -> pd.DataFrame:
    """
    Use saved ORAT data to get correlation between all tickers over the last n days
    """
    df = pd.read_csv(os.path.join('output', 'full.csv'))

    df['tradeDate'] = pd.to_datetime(df['tradeDate'])
    start_date = df['tradeDate'].max() - timedelta(days=n_days)
    df = df[df['tradeDate'] >= start_date].reset_index(drop=True)

    df = df.pivot(values=['orIvXern20d'], index=['tradeDate'], columns=['ticker']).reset_index()

    # convert from multindex back to flat column names
    df.columns = df.columns.to_flat_index()
    df.columns = [column[0] if column[0] == 'tradeDate' else column[1] for column in df.columns]

    df.sort_values('tradeDate', inplace=True)
    df.drop('tradeDate', axis=1, inplace=True)

    df = df.corr('pearson')

    # convert to long format
    df.reset_index(inplace=True)
    df = df.melt(id_vars='index', var_name='ticker_b', value_name='correlation')
    df.rename({'index': 'ticker_a'}, axis=1, inplace=True)

    # remove rows that will always be correlation 1
    df = df.query('ticker_a != ticker_b')
    df.sort_values('correlation', inplace=True, ascending=False)

    # remove AA,BB - BB,AA duplicates created by df.corr
    df['tickers_formatted'] = df.apply(format_tickers, axis=1)
    df = df.drop_duplicates('tickers_formatted')
    df.drop('tickers_formatted', axis=1, inplace=True)

    df.to_csv(os.path.join('output', 'correlation.csv'), index=False)
    return df


if __name__ == '__main__':
    get_correlation()
