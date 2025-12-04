import pandas as pd
import numpy as np

def ts_clease(df, start_date,base_value,freq):

    df = df.ffill()
    df = df/df.loc[start_date]*base_value

    if freq == 'd':
        df = df
    elif freq == 'm':
        df = df.resample('M').last()
    
    return df