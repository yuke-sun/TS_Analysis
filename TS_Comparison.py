import os
import pandas as pd
import numpy as np
from data.get_bt_history import get_bt_history
from data.get_index_history import get_live_index_history
loc = os.getcwd()
############# Toolkit packages are needed #########################

mapping = pd.read_csv(loc + r"\inputs\mapping.csv")
msci_ts_all = pd.read_csv(loc + r"\TS\msci_ts.csv", index_col= 'Date', parse_dates= ['Date'])
batch_ids = mapping['batch-id'].dropna().tolist()
outputs = dict()
excel_path = loc + r"\TS\Pivot_example.xlsx"

# Optional filters — set to None or [] to disable filtering
currency_filters = None        # e.g., ['EUR','USD'], or None
return_type_filters = ['pr']  # e.g., ['pr'], or None
base_date = '2024-10-01'
base_value = 1000



for batch_id in batch_ids:
    symbol = mapping.loc[mapping['batch-id'] == batch_id, 'Symbol'].iloc[0]
    msci_ric = mapping.loc[mapping['batch-id'] == batch_id, 'RIC'].iloc[0]
    key = mapping.loc[mapping['batch-id'] == batch_id, 'Key'].iloc[0]

    ############ Get TS ##################
    name, sw2_ts = get_bt_history(batch_id, currency_filters, return_type_filters, base_date)
    sw1_ts = get_live_index_history(symbol, base_value= 1000, base_date= base_date)
    msci_ts = msci_ts_all[msci_ric]
    ts_idx = pd.concat([sw2_ts, sw1_ts, msci_ts], axis=1, join='inner')
    ts_idx = ts_idx/ts_idx.iloc[0]*1000
    outputs[key] = ts_idx

    print(ts_idx)

    ########## Calculate TE ##############



# Save to Excel
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    for sheet_name, df in outputs.items():
        if isinstance(df.index, pd.DatetimeIndex):
            df = df.sort_index()
        df.to_excel(writer, sheet_name=sheet_name)


