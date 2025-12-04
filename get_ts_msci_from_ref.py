from datetime import datetime
import pandas as pd
import eikon as ek
import os
from data.ek_simple_functions import EikonFunctions
from data.data_cleasing import ts_clease
loc = os.getcwd()
ins = EikonFunctions()


######################## Inputs #####################
list = pd.read_csv(loc + r"\inputs\msci_ric_test.csv")
start_date = "2015-10-01"
end_date = "2025-12-01"
ts_freq = "EndOfDay"
final_freq = 'd'
base_value = 1000
########################################################

list = list[list['Frequency'] == ts_freq]
ric = list['RIC'].tolist()
ric_to_name_dic = list.set_index('RIC')['Name'].to_dict()
today = datetime.today().strftime('%Y%m%d')
df = ins.get_timeseries_close(ric,start_date,end_date)
df_renamed = df.rename(columns = ric_to_name_dic)
df_rebased = ts_clease(df = df_renamed, start_date= start_date, base_value= base_value, freq= final_freq)

print(df_rebased)