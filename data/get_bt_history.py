"""Retrieve index history for a specific Toolkit backtest.
Parameters
- batch_id : str — Toolkit batch ID.
- environment : str — The environment to query (e.g., common.PROD).
Returns
- pd.DataFrame — A DataFrame containing the historical index value for the specified batch.
"""
from docs.backtest import common
from docs.backtest.common import get_index_history, get_backtests
import pandas as pd
from datetime import datetime
import os

ENVIRONMENT = common.PROD
# Optional filters — set to None or [] to disable filtering
currency_filters = None        # e.g., ['EUR','USD'], or None
return_type_filters = ['pr']  # e.g., ['pr'], or None
base_date = '2015-10-30'
base_value = 1000
batch_ids = []
batch_ids = ["d84bfc9031d6","9ee3656a1d6a","dc2d0f01b768","7a74e7e95fe3","c556790f6e54","5eef8c4550ff","f59d87c69daa"]

def get_bt_history(batch_id, currency_filters, return_type_filters, base_date):
    
    try:
        history = get_index_history(environment=ENVIRONMENT, batch_id=batch_id)
        history['day'] = pd.to_datetime(history['day'], dayfirst=True)

        detail = get_backtests(environment=ENVIRONMENT, batch_id=batch_id)
        index_name = detail.get('index_name')

        # Apply currency filter if set
        if currency_filters:
            history = history[history['index_currency'].isin(currency_filters)]

        # Apply return type filter if set
        if return_type_filters:
            history = history[history['return_type'].isin(return_type_filters)]

        if history.empty:
            print(f"[INFO] No matching data for batch ID {batch_id} after filtering.")

        history['label'] = f"{index_name} " + history['index_currency'] + " " + history['return_type']
        pivoted = history.pivot(index='day', columns='label', values='index_value')
        pivoted = pivoted.sort_index().reset_index()
        if pivoted.shape[1] == 4:
            new_order = [0, 3, 2, 1]
            pivoted = pivoted.iloc[:, new_order]
        pivoted.rename(columns={'day': 'Date'}, inplace=True)
        pivoted = pivoted.set_index('Date')
        pivoted = pivoted[pivoted.index >= base_date]
        
        print(f"\n=== History for Batch ID: {batch_id} ===")
        print(pivoted)

    except Exception as e:
        print(f"[ERROR] Batch {batch_id} - History not available: {e}")
    
    return index_name, pivoted


# Save to CSV

if __name__ == "__main__":
    pivoted_all = pd.DataFrame()
    for batch_id in batch_ids:
        name, pivoted = get_bt_history(batch_id, currency_filters, return_type_filters)
        pivoted_all = pd.concat([pivoted_all, pivoted], axis = 1)

    if len(batch_ids) == 1:
        filename = os.path.join(os.getcwd(), f"BT\\bt_history\\history_{name}.csv")
    else:
        today = datetime.today().strftime('%Y%m%d')
        filename = os.path.join(os.getcwd(), f"BT\\bt_history\\{today}_history.csv")

    if base_date:
        pivoted_all = pivoted_all[pivoted_all.index >= base_date]
        pivoted_all = pivoted_all/pivoted_all.iloc[0]*base_value
        pivoted_all = pivoted_all.reset_index()
    
    pivoted_all.to_csv(filename, sep= ',')
    print(f"Saved: {filename}")