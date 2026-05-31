# ============================
#   SIGNAL LOGIC
#   Strategy: EMA+RSI+BB + H1 Trend Filter
# ============================

from config import (
    RSI_BUY_MIN, RSI_BUY_MAX,
    RSI_SELL_MIN, RSI_SELL_MAX
)


def get_signal(last, prev, h1_trend):
    bb_expanding    = prev['bb_squeeze'] == True and last['bb_squeeze'] == False
    ema_bullish     = last['ema_fast'] > last['ema_slow']
    rsi_buy         = RSI_BUY_MIN  < last['rsi'] < RSI_BUY_MAX
    price_above_mid = last['close'] > last['bb_mid']

    # Spot trading — BUY only
    if h1_trend == 'bullish' and bb_expanding and ema_bullish and rsi_buy and price_above_mid:
        return 'buy'

    return None


def describe_market(last, h1_trend):
    trend   = "BULLISH 📈" if last['ema_fast'] > last['ema_slow'] else "BEARISH 📉"
    squeeze = "YES — Coiling 🔴" if last['bb_squeeze'] else "NO — Expanding 🟢"
    h1      = "BULLISH 📈" if h1_trend == 'bullish' else "BEARISH 📉" if h1_trend == 'bearish' else "NEUTRAL ➡️"

    print(f"   H1 Trend  : {h1}")
    print(f"   M5 Trend  : {trend}")
    print(f"   RSI       : {last['rsi']:.2f}")
    print(f"   BB Squeeze: {squeeze}")