import os
import pandas as pd


def get_correlation(df_full: pd.DataFrame) -> pd.DataFrame:
    """
    Given a dataframe with results for all tickers from the ORATS api, create a correlation dataframe.
    """
    df = df_full.copy()

    df = df.pivot(values=['iv30d'], index=['tradeDate'], columns=['ticker']).reset_index()

    # convert from multindex back to flat column names
    df.columns = df.columns.to_flat_index()
    df.columns = [column[0] if column[0] == 'tradeDate' else column[1] for column in df.columns]

    df.sort_values('tradeDate', inplace=True)
    df.drop('tradeDate', axis=1, inplace=True)

    df = df.corr('pearson')
    return df


if __name__ == '__main__':
    df = pd.read_csv(os.path.join('output', 'full.csv'))
    df_corr = get_correlation(df)
    df_corr.to_csv(os.path.join('output', 'correlation.csv'))