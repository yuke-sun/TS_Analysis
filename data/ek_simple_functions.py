from datetime import datetime
import pandas as pd
import eikon as ek

class EikonFunctions:

    '''
    find field name in Workspace under DIB (Data Item Browser)
    
    '''

    def __init__(self):

        ek.set_app_key('5ecc2777ab114a7f8e8b0dccf47907cee7ec9b5c')


    def get_field(field_name, params=None, sort_dir=None, sort_priority=None):
        '''
        This is a helper function to build the field for the get_data function.
        '''
        field = ek.TR_Field(field_name, params, sort_dir, sort_priority)

        return field
        
    def get_timeseries_data(self, ric, start_date, end_date):
        '''
        ric = ['ric1','ric2']

        '''
        df = ek.get_timeseries(ric, 
                            start_date=start_date,  
                            end_date=end_date)
        if len(ric) == 1:
            name = df.columns.name + '_TS.csv'
        else:
            today = datetime.today().strftime('%Y%m%d')
            name = today + '_TS.csv'
        return df, name
    
    def get_timeseries_close(self, rics, start_date, end_date):
        '''
        ric = ['ric1','ric2'] OR single ric

        '''
        df = pd.DataFrame()

        for ric in rics:

            df_temp = ek.get_timeseries(ric, 
                                start_date=start_date,  
                                end_date=end_date, fields= ['CLOSE'])
            df_temp.rename(columns={"CLOSE": ric}, inplace=True)
            df = pd.merge(df, df_temp, left_index= True, right_index= True, how = 'outer')
    
        return df

    def get_ts_data(self, ric, start_date, end_date):

        '''
        get time series data from function get_data
        '''

        # Get data from Eikon
        data, _ = ek.get_data(
            ric,["TR.CLOSEPRICE.date", "TR.CLOSEPRICE(Adjusted=1)"],
            parameters={'SDate': start_date, 'EDate': end_date}
        )

        # Convert to DataFrame
        ts = pd.DataFrame(data)

        # Clean and convert the Date column
        ts["Date"] = pd.to_datetime(ts["Date"].str.replace("Z", ""), format="%Y-%m-%dT%H:%M:%S", errors='coerce')

        # Rename the Close Price column to the RIC
        ts.rename(columns={"Close Price": ric}, inplace=True)

        ts.drop(columns= 'Instrument', inplace=True)
        ts.set_index('Date', inplace=True)

        return ts

    def get_fundamental_data(rics, fields, scale=6, sdate=0, edate=-2, frq='FY', curn='EUR'):

        '''
        scale = 6 scaled to millions
        edate = -2 get past two years
  
        '''
        
        params = {'Scale': scale, 'SDate': sdate, 'EDate': edate, 'FRQ': frq, 'Curn': curn}
        df, err = ek.get_data(rics, fields, params)
        
        return df, err


    def save_csv(self, df, filename):
        df.to_csv(filename)
        return True



if __name__ == "__main__":

    ins = EikonFunctions()
    today = datetime.today().strftime('%Y%m%d')
    df, file_name = ins.get_timeseries_data([".dMIWD00000PUS"],"2016-01-01","2016-01-10")
    print(df)

    # # get fundamental info
    # rics = ['.dMIWD00000PUS']
    # fields = ["TR.F.GEOAGGTotRevenue;TR.F.GEOAGGTotRevenue.ChildGeoName"]
    # df, err = ek.get_data(rics, fields)
    # fundamental_df, fundamental_err = EikonFunctions.get_fundamental_data(rics, fields)
    # print(fundamental_df)


