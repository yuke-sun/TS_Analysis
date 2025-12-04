from pandas.tseries.offsets import BMonthEnd
from dateutil.relativedelta import relativedelta
import requests
from datetime import datetime
from urllib3 import exceptions, disable_warnings
from requests.auth import HTTPBasicAuth
import os
import pandas as pd
import numpy as np
import requests
from requests.auth import HTTPBasicAuth
from io import StringIO

user= 'yukesun'
pswd= 'RUNqbpPe4c68q5M!'

def get_live_index_history(jobId, base_date, base_value):
    pathTS = "https://www.stoxx.com/document/Indices/Current/HistoricalData/h_"+ str(jobId).lower()+".txt"
    r = requests.get(pathTS, auth=HTTPBasicAuth(user, pswd), verify  =False)
    dataTS= r.text
    b = StringIO(dataTS)
    dftemp = pd.read_csv(b, sep=";",  skiprows=1, parse_dates = True, dayfirst = True, index_col = 0)
    dftemp.index = pd.to_datetime(dftemp.index)

    if dftemp.shape[1]==0:
        pass
    elif dftemp.shape[1] == 2:
        dftemp.columns = ['Symbol', str(jobId).upper()]
        dftemp = dftemp[str(jobId).upper()]
    else:
        dftemp.columns = ['Symbol', str(jobId).upper(), 'Unnamed']
        dftemp = dftemp[str(jobId).upper()] 
    
    dftemp = pd.DataFrame(dftemp)
    dftemp = dftemp.rename_axis('Date')
    dftemp = dftemp[dftemp.index >= base_date]
    dftemp = dftemp/dftemp.iloc[0]*base_value
    # dftemp = dftemp.reset_index()

    return dftemp

# if __name__ == "__main__":

#     index = []
#     history = get_live_index_history(index, base_value= 1000, base_date= '2021-09-17')
#     print(history)
#     save_path =  os.path.join( os.getcwd(), f"get_data\\TS\\{index}_history.csv")
#     history.to_csv(save_path, index=False)
#     print(f'save {index} history to {save_path}')

def calculate_corr(df):
    daily_returns = df.dropna().pct_change()
    correlation_matrix = daily_returns.corr()
    return correlation_matrix


if __name__ == "__main__":

    pivoted_all = pd.DataFrame()
    index = ["SWL", "SWEL", "SWESCL", "SWAPJL", "SWDEGP", "SWDEUP", "SWUKACPB", "STXWAL"]

    for idx in index:
        history = get_live_index_history(idx, base_value= 1000, base_date= '2015-10-30')
        history.set_index('Date', inplace= True)
        pivoted_all = pd.concat([pivoted_all, history], axis = 1)

    pivoted_all = pivoted_all.ffill()
    if len(index) == 1:
        filename = os.path.join(os.getcwd(), f"get_data\\TS\\history_{index}.csv")
    else:
        today = datetime.today().strftime('%Y%m%d')
        filename = os.path.join(os.getcwd(), f"get_data\\TS\\{today}_history.csv")

    pivoted_all.to_csv(filename, sep= ',')
    print(f"Saved: {filename}")
    pivoted_all = pivoted_all[pivoted_all.index <= '2025-10-31']
    ## calculate Correlation
    # correlation_matrix = calculate_corr(pivoted_all)
    # print(correlation_matrix)
    # correlation_matrix.to_clipboard()