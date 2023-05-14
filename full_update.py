from fetch_data import fetch_data
from correlation import get_correlation
from comparison import run_comparisons
from firestore_upload import run_firestore_upload


if __name__ == '__main__':
    print('Fetching data...')
    fetch_data()
    print('Running correlation...')
    get_correlation()
    print('Creating comparison data...')
    run_comparisons()
    print('Run firestore upload...')
    run_firestore_upload()
