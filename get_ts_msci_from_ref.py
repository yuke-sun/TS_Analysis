from datetime import datetime
import pandas as pd
import eikon as ek
import os
from data.ek_simple_functions import EikonFunctions
loc = os.getcwd()
ins = EikonFunctions()

list = pd.read_csv(loc + r"\inputs\msci_ric.csv")
list = list[list['Frequency'] == 'EndOfDay']
ric = list['RIC'].tolist()
ric_to_name = list.set_index('RIC')['Name'].to_dict()

today = datetime.today().strftime('%Y%m%d')
df = ins.get_timeseries_close(ric,"2015-10-01","2025-12-01")
df_renamed = df.rename(columns=ric_to_name)

def ts_clease(df, start_date,base_value,freq):

    df = df.ffill()
    df = df/df.loc[start_date]*base_value
    
    return df_rebased

df_rebased = ts_clease(df=df_renamed, start_date= '2025-09-23', base_value= 1000, freq= 'd')

print(df_rebased)