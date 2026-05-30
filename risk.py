# ============================
#   RISK MANAGEMENT
# ============================

from config import (
    RISK_PER_TRADE_PCT,
    RISK_REWARD_RATIO,
    STOP_LOSS_PCT
)


def calculate_trade(balance, price, signal):
    """
    Calculate position size, stop loss and take profit

    Returns:
        qty  — how much to buy/sell
        sl   — stop loss price
        tp   — take profit price
    """

    # How much USDT to risk on this trade (1% of balance)
    risk_amount = balance * (RISK_PER_TRADE_PCT / 100)

    # Stop loss distance in USDT
    sl_distance = price * (STOP_LOSS_PCT / 100)

    # Position size based on risk
    qty = round(risk_amount / sl_distance, 6)

    if signal == 'buy':
        sl = round(price - sl_distance, 6)
        tp = round(price + (sl_distance * RISK_REWARD_RATIO), 6)

    elif signal == 'sell':
        sl = round(price + sl_distance, 6)
        tp = round(price - (sl_distance * RISK_REWARD_RATIO), 6)

    else:
        return None, None, None

    return qty, sl, tp


def is_trade_allowed(balance, price, open_trades, max_trades):
    """Check if we are allowed to open a new trade"""

    # Too many open trades
    if open_trades >= max_trades:
        print(f"   ⚠️  Max trades reached ({open_trades}/{max_trades})")
        return False

    # Not enough balance
    min_required = price * 0.001   # Minimum ~0.1% of price
    if balance < min_required:
        print(f"   ⚠️  Balance too low: ${balance:.2f}")
        return False

    return True