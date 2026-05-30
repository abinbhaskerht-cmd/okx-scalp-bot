# ============================
#   SIGNAL LOGIC
# ============================

from config import (
    RSI_BUY_MIN, RSI_BUY_MAX,
    RSI_SELL_MIN, RSI_SELL_MAX
)


def get_signal(last, prev):
    """
    Returns 'buy', 'sell' or None
    
    BUY conditions:
    - BB was squeezing and now expanding
    - Fast EMA above Slow EMA (uptrend)
    - RSI between 50-65 (momentum building, not overbought)
    - Price closed above BB midline

    SELL conditions:
    - BB was squeezing and now expanding
    - Fast EMA below Slow EMA (downtrend)
    - RSI between 35-50 (momentum building down, not oversold)
    - Price closed below BB midline
    """

    # BB expansion after squeeze
    bb_expanding = prev['bb_squeeze'] == True and last['bb_squeeze'] == False

    # EMA direction
    ema_bullish = last['ema_fast'] > last['ema_slow']
    ema_bearish = last['ema_fast'] < last['ema_slow']

    # RSI conditions
    rsi_buy  = RSI_BUY_MIN  < last['rsi'] < RSI_BUY_MAX
    rsi_sell = RSI_SELL_MIN < last['rsi'] < RSI_SELL_MAX

    # Price vs BB midline
    price_above_mid = last['close'] > last['bb_mid']
    price_below_mid = last['close'] < last['bb_mid']

    # BUY signal — all 3 must agree
    if bb_expanding and ema_bullish and rsi_buy and price_above_mid:
        return 'buy'

    # SELL signal — all 3 must agree
    if bb_expanding and ema_bearish and rsi_sell and price_below_mid:
        return 'sell'

    return None


def describe_market(last):
    """Print a simple market summary"""
    trend = "BULLISH 📈" if last['ema_fast'] > last['ema_slow'] else "BEARISH 📉"
    squeeze = "YES — Coiling 🔴" if last['bb_squeeze'] else "NO — Expanding 🟢"

    print(f"   Trend     : {trend}")
    print(f"   RSI       : {last['rsi']:.2f}")
    print(f"   BB Squeeze: {squeeze}")