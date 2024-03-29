import os
import pandas as pd

import datetime
import matplotlib.pyplot as plt
from tqdm import tqdm


def get_comparison(df: pd.DataFrame, ticker_a, ticker_b):
    """
    Compare two tickers.
    Return plots and metrics.
    """
    # filter down to only provided tickers
    df = df[df['ticker'].isin([ticker_a, ticker_b])]
    df.reset_index(drop=True, inplace=True)

    cols_to_keep = ['ticker','tradeDate','orIvXern20d','mktWidthVol']
    df = df[cols_to_keep]

    df["tradeDate"] = pd.to_datetime(df["tradeDate"])

    df = df[df.tradeDate > datetime.datetime.now() - pd.to_timedelta('200Day')]

    #Formating GME data and adding some columns)
    df = pd.pivot_table(df, index = 'tradeDate', columns = 'ticker', values = ['ticker','tradeDate','orIvXern20d','mktWidthVol']).reset_index()

    #Calculating the metrics we wanna see
    df['ratio'] = df['orIvXern20d'][ticker_a] / df['orIvXern20d'][ticker_b]
    df['meanRatio'] = abs(df['ratio'].rolling(40).mean())
    df['absSpread'] = abs(df['orIvXern20d'][ticker_a] - df['orIvXern20d'][ticker_b])
    df['stdDev'] = df['ratio'].rolling(40).std()
    df['zScore'] = (df['ratio'] - df['meanRatio']) / df['stdDev']
    df['upBand'] = df['meanRatio'] + (df['stdDev'] * 3)
    df['downBand'] = df['meanRatio'] - (df['stdDev'] * 3)
    df['upHurdle'] = df['upBand'] + (df['mktWidthVol'][ticker_b] / df['orIvXern20d'][ticker_b])
    df['downHurdle'] = df['downBand'] - (df['mktWidthVol'][ticker_b] / df['orIvXern20d'][ticker_b])

    df.columns = df.columns.map('_'.join)
    return df


def plot_comparison(df: pd.DataFrame, ticker_a, ticker_b):
    plt.clf()
    plt.style.use('ggplot')
    plt.title(f'{ticker_a} - {ticker_b}')
    plt.plot(df['tradeDate_'], df['ratio_'], color='green',label = 'Spread')
    plt.plot(df['tradeDate_'], df['meanRatio_'], color='red', label = 'Rolling Mean Spread')
    plt.plot(df['tradeDate_'], df['upBand_'], color='blue', label = 'Rolling 3 std dev')
    plt.plot(df['tradeDate_'], df['downBand_'], color='blue')
    plt.plot(df['tradeDate_'], df['upHurdle_'], color='orange', label = 'market width')
    plt.plot(df['tradeDate_'], df['downHurdle_'], color='orange')

    plt.xlabel("date")
    plt.ylabel("stuff")
    plt.legend(loc='best')
    return plt


def get_comparison_output_path(ticker_a, ticker_b):
    return os.path.join('output', 'app_data', 'comparisons', f'{ticker_a}_{ticker_b}.json')


corr_cutoff_default = 0.95


def run_comparisons(corr_cutoff=corr_cutoff_default):
    os.makedirs(os.path.join('output', 'app_data'), exist_ok=True)
    os.makedirs(os.path.join('output', 'app_data', 'comparisons'), exist_ok=True)
    df_full = pd.read_csv(os.path.join('output', 'full.csv'))
    df_corr = pd.read_csv(os.path.join('output', 'correlation.csv'))
    df_corr = df_corr[df_corr['correlation'] >= corr_cutoff]

    # create dataframe tickers and zscores, save comparisons to a file
    df_zscores = pd.DataFrame()
    for i, r in tqdm(df_corr.iterrows()):
        ticker_a = r.ticker_a
        ticker_b = r.ticker_b
        df_comp = get_comparison(df_full, ticker_a, ticker_b)

        # get last (most recent zscore in comparison dataframe)
        zscore = df_comp['zScore_'].iloc[-1]
        new_row = pd.DataFrame([{'ticker_a': ticker_a, 'ticker_b': ticker_b, 'zscore': zscore}])
        df_zscores = pd.concat([df_zscores, new_row])
        df_comp['tradeDate_'] = df_comp['tradeDate_'].dt.strftime('%Y-%m-%d')

        df_comp.to_json(get_comparison_output_path(ticker_a, ticker_b), orient='records', date_format='iso')

    # take top 10 zscores and create a json list containing them
    df_zscores.sort_values('zscore', ascending=False, inplace=True)
    df_zscores = df_zscores[:10]
    comparison_pairs = df_zscores[['ticker_a', 'ticker_b']]
    comparison_list_path = os.path.join('output', 'app_data', 'comparison_list.json')
    comparison_pairs.to_json(comparison_list_path, orient='records')


if __name__ == '__main__':
    run_comparisons()
