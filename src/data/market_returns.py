from datetime import date
from pandas_datareader import DataReader as dr
import pandas as pd
import numpy as np

def get_market_returns():
    '''Getting Berkshire & SP 500 returns'''
    start_date = date(1979, 12, 31)
    end_date = date(2016, 12, 31)
    y_bk = dr('BRK-A', 'yahoo', start=start_date)
    y_bk = y_bk['Adj Close']
    y_sp = dr('^SP500TR', 'yahoo', start=start_date) #TODO: Get longer backfill
    y_sp = y_sp['Adj Close']
    ts = pd.concat([y_bk, y_sp], axis=1)
    ts.columns.values[0] = 'BRK-A'
    ts.columns.values[1] = 'SP500TR'
    dates_ann = pd.date_range(start_date, end_date, freq='A')
    ts_annualret = ts.reindex(dates_ann, method='ffill').pct_change()
    ts_annualret.pct_change()
    ts_annualret.index = ts_annualret.index.strftime('%Y')
    return ts_annualret

x = get_market_returns()

def clean_buffett(x):
    df = x["BRK-A"]
    df.loc['1977'] = np.nan
    df.loc['1978'] = np.nan
    df = df.sort_index()
    return df

if __name__ == '__main__':
    print(clean_buffett(x).loc["1981"])