from datetime import datetime
import pandas as pd
import eikon as ek
import os
from data.ek_simple_functions import EikonFunctions
loc = os.getcwd()
ins = EikonFunctions()

list = pd.read_csv(loc + r"\inputs\msci_ric.csv")



today = datetime.today().strftime('%Y%m%d')
df, file_name = ins.get_timeseries_data([".dMIWO000A0PUS"],"2015-12-01","2025-12-01")
print(df)
print(file_name)