import pandas as pd
from db import get_db_con


def get_comparison(ta, tb):
    """Compare two tickers (ta, tb)."""


if __name__ == '__main__':
    with get_db_con() as con:
        print(pd.read_sql('select * from corr', con))