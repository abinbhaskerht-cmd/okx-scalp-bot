# ============================
#   MAIN BOT LOOP
#   With Telegram + Dashboard
# ============================

import time
import schedule
from datetime import datetime, timezone

from exchange      import get_exchange, get_balance, get_candles, test_connection
from indicators    import build_dataframe, calculate_indicators, calculate_h1_trend, get_latest
from strategy      import get_signal, describe_market
from risk          import calculate_trade, is_trade_allowed
from trader        import place_order, get_open_trades, monitor_positions
from logger        import log_trade, create_log_file
from telegram_bot  import alert_trade_opened, alert_bot_started, send_message
from dashboard     import print_dashboard, get_telegram_summary
from config        import (
    SYMBOLS, TIMEFRAME, CANDLE_LIMIT,
    HTF_TIMEFRAME, HTF_CANDLES,
    MAX_OPEN_TRADES, USE_TIME_FILTER,
    TRADE_HOURS_START, TRADE_HOURS_END
)

# Cooldown tracker
last_trade_time = {}
COOLDOWN_MINUTES = 15
run_count        = 0


def is_trading_time():
    if not USE_TIME_FILTER:
        return True
    hour = datetime.now(timezone.utc).hour
    return TRADE_HOURS_START <= hour < TRADE_HOURS_END


def is_cooldown_active(symbol):
    now  = datetime.now()
    last = last_trade_time.get(symbol)
    if last:
        elapsed   = (now - last).seconds / 60
        remaining = COOLDOWN_MINUTES - elapsed
        if elapsed < COOLDOWN_MINUTES:
            print(f"   ⏳ Cooldown active — {remaining:.1f} mins remaining")
            return True
    return False


def run_bot():
    global run_count
    run_count += 1

    print("\n" + "=" * 45)
    print(f"   🤖 BOT RUN #{run_count} — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 45)

    if not is_trading_time():
        print("   ⏰ Outside trading hours — Sleeping")
        return

    exchange, mode = get_exchange()

    if not test_connection(exchange):
        print("   ❌ Connection failed — Skipping")
        return

    create_log_file()

    balance = get_balance(exchange)
    print(f"\n   💰 Balance: ${balance:,.2f} USDT")

    open_trades = get_open_trades(exchange, SYMBOLS)
    print(f"   📂 Open trades: {open_trades}/{MAX_OPEN_TRADES}")

    # Monitor existing positions
    monitor_positions(exchange)

    # Print dashboard every 12 runs (1 hour)
    if run_count % 12 == 0:
        print_dashboard()
        send_message(get_telegram_summary())

    for symbol in SYMBOLS:
        print(f"\n🪙  Checking {symbol}...")

        if is_cooldown_active(symbol):
            continue

        candles = get_candles(exchange, symbol, TIMEFRAME, CANDLE_LIMIT)
        if candles is None:
            print(f"   ⚠️  No candle data — skipping")
            continue

        candles_h1 = get_candles(exchange, symbol, HTF_TIMEFRAME, HTF_CANDLES)
        if candles_h1 is None:
            print(f"   ⚠️  No H1 data — skipping")
            continue

        df         = build_dataframe(candles)
        df         = calculate_indicators(df)
        last, prev = get_latest(df)
        h1_trend   = calculate_h1_trend(candles_h1)

        describe_market(last, h1_trend)

        if h1_trend == 'neutral':
            print(f"   Signal: ➡️  H1 NEUTRAL — Skipping")
            continue

        signal = get_signal(last, prev, h1_trend)

        if signal is None:
            print(f"   Signal: ⏳ NO SIGNAL — Waiting")
            continue

        print(f"   Signal: {'✅ BUY' if signal == 'buy' else '🔴 SELL'}")

        if not is_trade_allowed(balance, last['close'], open_trades, MAX_OPEN_TRADES):
            continue

        qty, sl, tp = calculate_trade(balance, last['close'], signal)
        if qty is None:
            continue

        order = place_order(exchange, symbol, signal, qty, sl, tp)

        if order:
            open_trades += 1
            last_trade_time[symbol] = datetime.now()
            log_trade(symbol, signal, last['close'], qty, sl, tp, order['id'])
            alert_trade_opened(symbol, signal, last['close'], qty, sl, tp)
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
    print("   Strategy : EMA+RSI+BB + H1 Filter")
    print("   Alerts   : Telegram enabled")
    print("   Dashboard: Every 1 hour")
    print("=" * 45)

    alert_bot_started()
    run_bot()

    schedule.every(5).minutes.do(run_bot)

    print("\n   ⏰ Scheduled every 5 mins — Press Ctrl+C to stop\n")

    while True:
        schedule.run_pending()
        time.sleep(1)