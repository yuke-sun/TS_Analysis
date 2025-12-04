import pandas as pd
import numpy as np

def ts_clease(df, start_date,base_value,freq):

    # df = df.ffill()
    
    base_row = pd.Series({
        col: df[col].loc[df[col].first_valid_index()] if df[col].first_valid_index() is not None else np.nan
        for col in df.columns
    })

    df = df.div(base_row, axis=1) * base_value

    if freq == 'd':
        df = df
    elif freq == 'm':
        df = df.resample('M').last()
    
    return df