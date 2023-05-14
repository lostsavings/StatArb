# Setup
1. Setup a virtualenvironment in the root directory and install requirements.
2. Create a file `configs/firebase_admin_key.json` containing an admin key for the firebase project (you can get this from Dawson).

# Running the whole process in one command
```bash
python full_update.py
```

# Scripts
## [`fetch_data.py`](./fetch_data.py)
Used to pull data from ORATS for all tickers stored in `tickers.txt`. We're making one api call per date, right now it's set to pull data for the last 60 day window.
https://docs.orats.io/datav2-api-guide/data.html#core-data-history
```bash
python fetch_data.py
```
Writes full ticker history to `output/full.csv`.

## [`correlation.py`](./correlation.py)
Computes correlation for all tickers and writes to `output/correlation.csv`
```bash
python correlation.py --n-days 60
```

## [`comparison.py`](./comparison.py)
Compares ticker combinations over a certain correlation threshold. Generates formatted data and puts it in the `output/app_data` folder
```bash
python comparison.py --corr-cutoff 0.95
```

## [`firestore_upload.py`](./firestore_upload.py)
Uploads the data in `output/app_data` to firebase's firestore (production).

# Running the dashboard
```bash
# in the webapp/frontend directory
npm i
npm run dev
```
Go to http://localhost:3000
