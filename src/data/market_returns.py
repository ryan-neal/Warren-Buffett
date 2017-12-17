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

def clean_sp(x):
    # manually adding S&P 500 Total Returns as data source does not inlude
    # backfill source is https://www.slickcharts.com/sp500/returns
    df = x["SP500TR"]
    sp5_backfill = {
        1977: -0.0718,
        1978: 0.0656,
        1979: 0.1844,
        1980: 0.3242,
        1981: -0.0491,
        1982: 0.2155,
        1983: 0.2256,
        1984: 0.0627,
        1985: 0.3173,
        1986: 0.1867,
        1987: 0.0525,
        1988: 0.1661
    }

    for k, v in sp5_backfill.items():
        df[str(k)] = v

    df = df.sort_index()
    return df

def get_difference(x):
    x['BRK-A'] = clean_buffett(x)
    x["SP500TR"] = clean_sp(x)
    x["difference"] = x["BRK-A"] - x["SP500TR"]
    df = x["difference"]
    df.loc["1978"] = np.nan
    df.loc["1977"] =np.nan
    df = df.sort_index()
    return(df)

if __name__ == '__main__':
    print(clean_buffett(x))
    print(clean_sp(x).loc["1981"])
    print(get_difference(x))
