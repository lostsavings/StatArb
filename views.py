import pandas as pd
from utils import get_db_con


if __name__ == '__main__':
    with get_db_con() as con:
        print(pd.read_sql('select * from corr', con))