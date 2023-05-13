import os
import json
import glob
import firebase_admin
from firebase_admin import credentials, firestore


if __name__ == '__main__':
    cred_path = os.path.join('configs', 'firebase_admin_key.json')
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://stat-arb-9bc39.firebaseio.com/'
    })
    db = firestore.client()
    collection = db.collection('statdata')

    # upload ticker list
    with open(os.path.join('output', 'app_data', 'comparison_list.json')) as f:
        data = json.load(f)
    collection.document('comparison_list').set({
        'items': data
    })

    # upload ticker comparisons
    comparisons_path = os.path.join('output', 'app_data', 'comparisons', '*.json')
    for file_path in glob.glob(comparisons_path):
        with open(file_path) as f:
            # parse ticker names from file
            ticker_combo = os.path.basename(file_path).replace('.json', '')
            data = json.load(f)
            collection.document(ticker_combo).set({
                'items': data
            })
