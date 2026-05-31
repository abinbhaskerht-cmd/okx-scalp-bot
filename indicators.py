# ============================
#   INDICATORS
#   Added: H1 Trend Filter
# ============================

import pandas as pd
import ta
from config import (
    EMA_FAST, EMA_SLOW,
    RSI_PERIOD,
    BB_PERIOD, BB_STD_DEV, BB_SQUEEZE_LOOKBACK,
    HTF_EMA_FAST, HTF_EMA_SLOW
)


def build_dataframe(candles):
    df = pd.DataFrame(candles, columns=['time','open','high','low','close','volume'])
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df.set_index('time', inplace=True)
    return df


def calculate_indicators(df):
    df['ema_fast'] = ta.trend.ema_indicator(df['close'], window=EMA_FAST)
    df['ema_slow'] = ta.trend.ema_indicator(df['close'], window=EMA_SLOW)
    df['rsi']      = ta.momentum.rsi(df['close'], window=RSI_PERIOD)

    bb               = ta.volatility.BollingerBands(df['close'], window=BB_PERIOD, window_dev=BB_STD_DEV)
    df['bb_upper']   = bb.bollinger_hband()
    df['bb_lower']   = bb.bollinger_lband()
    df['bb_mid']     = bb.bollinger_mavg()
    df['bb_width']   = bb.bollinger_wband()
    df['bb_squeeze'] = df['bb_width'] < df['bb_width'].rolling(BB_SQUEEZE_LOOKBACK).mean()

    return df.dropna()


def calculate_h1_trend(candles_h1):
    """Calculate H1 trend direction"""
    df = pd.DataFrame(candles_h1, columns=['time','open','high','low','close','volume'])
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df.set_index('time', inplace=True)

    df['h1_ema_fast'] = ta.trend.ema_indicator(df['close'], window=HTF_EMA_FAST)
    df['h1_ema_slow'] = ta.trend.ema_indicator(df['close'], window=HTF_EMA_SLOW)
    df = df.dropna()

    if len(df) == 0:
        return 'neutral'

    last = df.iloc[-1]
    if last['h1_ema_fast'] > last['h1_ema_slow']:
        return 'bullish'
    elif last['h1_ema_fast'] < last['h1_ema_slow']:
        return 'bearish'
    return 'neutral'


def get_latest(df):
    return df.iloc[-1], df.iloc[-2]