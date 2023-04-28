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
Used to pull data from ORATS and create correlations between all tickers stored in `tickers.txt`.
Takes forever because:
1. We're making one api call per ticker.
2. Computing the correlation just takes forever.
```bash
python fetch_data.py
# Or, if you want to save to the db as well as local files...
python fetch_data.py --save-db
```
Writes two files:
1. `output/full.csv`: entire ticker history
2. `output/corr.csv`:

## [`comparison.py`](./comparison.py)
Contains functionality for comparing two tickers.
Ideally we will run this for only relevant ticker combinations, based on the correlations.
```bash
python comparison.py
```
Writes 2 files:
1. `output/comparisons/csv/{ticker_a}_{ticker_b}.csv`: Contains dataframe result of comparison.
2. `output/comparisons/svg/{ticker_a}_{ticker_b}.svg`: Contains plot showing comparison.