# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 00:12:51 2018

@author: Kushagra
"""

from nsepy import get_history
from datetime import date
import itertools
from collections import deque
import pandas as pd

# Get Data
INFY = get_history(symbol="INFY", start=date(2015,1,1), end=date(2016,1,1))
INFY = INFY[['Open','High','Low','Close','Volume']]

TCS = get_history(symbol="TCS", start=date(2015,1,1), end=date(2016,1,1))
TCS = TCS[['Open','High','Low','Close','Volume']]

NIFTYIT = get_history(symbol="NIFTY IT", start=date(2015,1,1), end=date(2016,1,1), index=True)
NIFTYIT = NIFTYIT[['Open','High','Low','Close','Volume']]

#*************************** PART 1 ****************************

# calculate the moving average
def moving_average(iterable, window):
    it = iter(iterable)
    d = deque(itertools.islice(it, window-1))
    d.appendleft(0)
    s = sum(d)
    for elem in it:
        s += elem - d.popleft()
        d.append(elem)
        yield s / float(window)

# Append null to first (window - 1) steps because we dont have points to calculate
# average till that point 
def return_window_average(iterable, window):
    res = [None for i in range(window-1)]
    res.extend(list(moving_average(iterable, window)))
    return res

INFY['4_week'] = return_window_average(INFY['Close'], 20)
INFY['16_week'] = return_window_average(INFY['Close'], 80)
INFY['52_week'] = return_window_average(INFY['Close'], 260)

TCS['4_week'] = return_window_average(TCS['Close'], 20)
TCS['16_week'] = return_window_average(TCS['Close'], 80)
TCS['52_week'] = return_window_average(TCS['Close'], 260)

NIFTYIT['4_week'] = return_window_average(NIFTYIT['Close'], 20)
NIFTYIT['16_week'] = return_window_average(NIFTYIT['Close'], 80)
NIFTYIT['52_week'] = return_window_average(NIFTYIT['Close'], 260)


#**************************** PART 2 *****************************

def rolling_window(data, resample='1d', lookback='75d'):
    data.index = data.index.to_datetime()
    dts = data.resample(resample).mean()
    return dts
        
rolling_window(INFY)

rolling_window(TCS)

rolling_window(NIFTYIT)


#***************************** PART 3 *****************************

# 3.1 Volume shocks - If volume traded is 10% higher/lower than previous day -
# make a 0/1 boolean time series for shock, 0/1 dummy-coded time series for 
# direction of shock.

def volume_shocks(df):
    df_vol = df[['Volume']]
    df_vol['prev_vol'] = df_vol.shift(1)
    df_vol['Volume shocks'] = (df_vol['prev_vol'] * 0.1 + df_vol['prev_vol'] < df_vol['Volume']) * 1
    return df_vol

INFY_vol = volume_shocks(INFY)

TCS_vol = volume_shocks(TCS)

NIFTYIT_vol = volume_shocks(NIFTYIT)

# 3.2 Price shocks - If closing price at T vs T+1 has a difference > 2%, then 0/1
# boolean time series for shock, 0/1 dummy-coded time series for direction of shock.

def price_shocks(df):
    df_price = df[['Prev Close', 'Close']]
    df_price['Price shocks'] = (df_price['Prev Close'] * 0.02 + df_price['Prev Close'] < df_price['Close']) * 1
    return df_price

INFY_price = price_shocks(INFY)

TCS_price = price_shocks(TCS)

NIFTYIT_price = price_shocks(NIFTYIT)


#3.3 Pricing black swan - If closing price at T vs T+1 has a difference > 2%, then
# 0/1 boolean time series for shock, 0/1 dummy-coded time series for direction of shock.

def pricing_black_swan(df):
    df_price = df[['Prev Close', 'Close']]
    df_price['Price shocks'] = (df_price['Prev Close'] * 0.02 + df_price['Prev Close'] < df_price['Close']) * 1
    return df_price

INFY_bs_price = pricing_black_swan(INFY)

TCS_bs_price = pricing_black_swan(TCS)

NIFTYIT_bs_price = pricing_black_swan(NIFTYIT)

# 3.4 Pricing shock without volume shock - based on points a & b - Make a 0/1 dummy
# time series.

#Could'nt understand the question properly 


