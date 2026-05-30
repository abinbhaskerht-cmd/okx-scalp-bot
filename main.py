# ============================
#   MAIN BOT LOOP
# ============================

import time
import schedule
from datetime import datetime, timezone

from exchange   import get_exchange, get_balance, get_candles, test_connection
from indicators import build_dataframe, calculate_indicators, get_latest
from strategy   import get_signal, describe_market
from risk       import calculate_trade, is_trade_allowed
from trader     import place_order, get_open_trades
from config     import (
    SYMBOLS, TIMEFRAME, CANDLE_LIMIT,
    MAX_OPEN_TRADES, USE_TIME_FILTER,
    TRADE_HOURS_START, TRADE_HOURS_END
)

# ============================
#   COOLDOWN TRACKER
# ============================
last_trade_time = {}
COOLDOWN_MINUTES = 15


def is_trading_time():
    if not USE_TIME_FILTER:
        return True
    hour = datetime.now(timezone.utc).hour
    return TRADE_HOURS_START <= hour < TRADE_HOURS_END


def is_cooldown_active(symbol):
    """Check if symbol is in cooldown period"""
    now  = datetime.now()
    last = last_trade_time.get(symbol)
    if last:
        elapsed = (now - last).seconds / 60
        remaining = COOLDOWN_MINUTES - elapsed
        if elapsed < COOLDOWN_MINUTES:
            print(f"   ⏳ Cooldown active — {remaining:.1f} mins remaining")
            return True
    return False


def run_bot():
    print("\n" + "=" * 45)
    print(f"   🤖 BOT RUN — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 45)

    # Check trading hours
    if not is_trading_time():
        print("   ⏰ Outside trading hours — Sleeping")
        return

    # Connect
    exchange, mode = get_exchange()

    # Test connection
    if not test_connection(exchange):
        print("   ❌ Connection failed — Skipping")
        return

    # Get balance
    balance = get_balance(exchange)
    print(f"\n   💰 Balance: ${balance:,.2f} USDT")

    # Check open trades
    open_trades = get_open_trades(exchange, SYMBOLS)
    print(f"   📂 Open trades: {open_trades}/{MAX_OPEN_TRADES}")

    # Loop through each symbol
    for symbol in SYMBOLS:
        print(f"\n🪙  Checking {symbol}...")

        # Check cooldown
        if is_cooldown_active(symbol):
            continue

        # Fetch candles
        candles = get_candles(exchange, symbol, TIMEFRAME, CANDLE_LIMIT)
        if candles is None:
            print(f"   ⚠️  No candle data — skipping")
            continue

        # Calculate indicators
        df         = build_dataframe(candles)
        df         = calculate_indicators(df)
        last, prev = get_latest(df)

        # Show market summary
        describe_market(last)

        # Get signal
        signal = get_signal(last, prev)

        if signal is None:
            print(f"   Signal: ⏳ NO SIGNAL — Waiting")
            continue

        print(f"   Signal: {'✅ BUY' if signal == 'buy' else '🔴 SELL'}")

        # Check if trade allowed
        if not is_trade_allowed(balance, last['close'], open_trades, MAX_OPEN_TRADES):
            continue

        # Calculate position size, SL, TP
        qty, sl, tp = calculate_trade(balance, last['close'], signal)
        if qty is None:
            continue

        # Place order
        order = place_order(exchange, symbol, signal, qty, sl, tp)

        if order:
            open_trades += 1
            last_trade_time[symbol] = datetime.now()
            print(f"\n   ✅ Trade opened!")
            print(f"   Qty: {qty} | SL: {sl} | TP: {tp}")
            print(f"   ⏳ Cooldown started — next trade in {COOLDOWN_MINUTES} mins")

    print("\n   ✅ Run complete — waiting for next candle...")


# ============================
#   START BOT
# ============================

if __name__ == "__main__":
    print("\n" + "=" * 45)
    print("   🤖 OKX SCALP BOT STARTING...")
    print("   Cooldown: 15 mins per symbol")
    print("=" * 45)

    run_bot()

    schedule.every(5).minutes.do(run_bot)

    print("\n   ⏰ Scheduled every 5 mins — Press Ctrl+C to stop\n")

    while True:
        schedule.run_pending()
        time.sleep(1)