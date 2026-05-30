# ============================
#   INDICATORS
# ============================

import pandas as pd
import ta
from config import (
    EMA_FAST, EMA_SLOW,
    RSI_PERIOD,
    BB_PERIOD, BB_STD_DEV, BB_SQUEEZE_LOOKBACK
)


def build_dataframe(candles):
    """Convert raw candle data into a DataFrame"""
    df = pd.DataFrame(candles, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df.set_index('time', inplace=True)
    return df


def calculate_indicators(df):
    """Add EMA, RSI and Bollinger Bands to DataFrame"""

    # EMA
    df['ema_fast'] = ta.trend.ema_indicator(df['close'], window=EMA_FAST)
    df['ema_slow'] = ta.trend.ema_indicator(df['close'], window=EMA_SLOW)

    # RSI
    df['rsi'] = ta.momentum.rsi(df['close'], window=RSI_PERIOD)

    # Bollinger Bands
    bb = ta.volatility.BollingerBands(df['close'], window=BB_PERIOD, window_dev=BB_STD_DEV)
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()
    df['bb_mid']   = bb.bollinger_mavg()
    df['bb_width'] = bb.bollinger_wband()

    # BB Squeeze — True when width is below recent average (market coiling)
    df['bb_squeeze'] = df['bb_width'] < df['bb_width'].rolling(BB_SQUEEZE_LOOKBACK).mean()

    return df


def get_latest(df):
    """Return last 2 rows for signal comparison"""
    return df.iloc[-1], df.iloc[-2]