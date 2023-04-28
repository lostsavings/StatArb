# Setup
1. Setup a virtualenvironment in the root directory and install requirements.
2. Create a file `configs/psql.yaml` containing the postgresql db configuration. Here's a template (you will need to replace some of these values - probably host and password):
```yaml
host: 127.0.0.1
username: finance
password: password_here
database: stat_arb
```

# Scripts
## [`fetch_data.py`](./fetch_data.py)
Used to pull data from ORATS for all tickers stored in `tickers.txt`. We're making one api call per ticker.
```bash
python fetch_data.py
# Or, if you want to save to the db as well as local files...
python fetch_data.py --save-db
```
Writes full ticker history to `output/full.csv`.

## [`correlation.py`](./correlation.py)
Computes correlation for all tickers and writes to `output/correlation.csv`
```bash
python correlation.py --n-days 60
```

## [`comparison.py`](./comparison.py)
Contains functionality for comparing two tickers.
Ideally we will run this for only relevant ticker combinations, based on the correlations.
```bash
python comparison.py
```
Writes 2 files:
1. `output/comparisons/csv/{ticker_a}_{ticker_b}.csv`: Contains dataframe result of comparison.
2. `output/comparisons/svg/{ticker_a}_{ticker_b}.svg`: Contains plot showing comparison.