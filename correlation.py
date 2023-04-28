import os
import click
import pandas as pd
from datetime import date, timedelta


@click.command()
@click.option('--n-days', default=60, help='Number of days of history when checking correlation.')
def get_correlation(n_days: int) -> pd.DataFrame:
    """
    Use saved ORAT data to get correlation between all tickers over the last n days
    """
    df = pd.read_csv(os.path.join('output', 'full.csv'))

    df['tradeDate'] = pd.to_datetime(df['tradeDate'])
    start_date = df['tradeDate'].max() - timedelta(days=n_days)
    df = df[df['tradeDate'] >= start_date].reset_index(drop=True)

    df = df.pivot(values=['iv30d'], index=['tradeDate'], columns=['ticker']).reset_index()

    # convert from multindex back to flat column names
    df.columns = df.columns.to_flat_index()
    df.columns = [column[0] if column[0] == 'tradeDate' else column[1] for column in df.columns]

    df.sort_values('tradeDate', inplace=True)
    df.drop('tradeDate', axis=1, inplace=True)

    df = df.corr('pearson')

    df.to_csv(os.path.join('output', 'correlation.csv'))
    return df


if __name__ == '__main__':
    get_correlation()
