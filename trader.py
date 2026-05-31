# ============================
#   ORDER EXECUTION
#   Manual TP/SL monitoring
# ============================

from config import TRADE_MODE

# Track open trades manually
open_positions = {}


def place_order(exchange, symbol, signal, qty, sl, tp):
    side = 'buy' if signal == 'buy' else 'sell'

    print(f"\n🚀 Placing {side.upper()} order...")
    print(f"   Symbol : {symbol}")
    print(f"   Qty    : {qty}")
    print(f"   SL     : {sl}")
    print(f"   TP     : {tp}")

    try:
        order = exchange.create_order(
            symbol = symbol,
            type   = 'market',
            side   = side,
            amount = qty,
        )

        print(f"   ✅ Order placed!")
        print(f"   Order ID: {order['id']}")

        open_positions[symbol] = {
            'side'    : signal,
            'entry'   : order.get('average') or order.get('price') or 0,
            'qty'     : qty,
            'sl'      : sl,
            'tp'      : tp,
            'order_id': order['id']
        }

        return order

    except Exception as e:
        print(f"   ❌ Order failed: {e}")
        return None


def monitor_positions(exchange):
    """Check open positions and close if TP or SL hit"""
    if not open_positions:
        return

    for symbol in list(open_positions.keys()):
        pos   = open_positions[symbol]
        side  = pos['side']
        sl    = pos['sl']
        tp    = pos['tp']

        try:
            ticker        = exchange.fetch_ticker(symbol)
            current_price = ticker['last']

            print(f"\n   📊 Monitoring {symbol}")
            print(f"   Entry : {pos['entry']}")
            print(f"   Now   : {current_price}")
            print(f"   TP    : {tp} | SL: {sl}")

            close_trade = False
            reason      = ''

            if side == 'buy':
                if current_price >= tp:
                    close_trade = True
                    reason      = 'TP HIT'
                elif current_price <= sl:
                    close_trade = True
                    reason      = 'SL HIT'

            elif side == 'sell':
                if current_price <= tp:
                    close_trade = True
                    reason      = 'TP HIT'
                elif current_price >= sl:
                    close_trade = True
                    reason      = 'SL HIT'

            if close_trade:
                close_side = 'sell' if side == 'buy' else 'buy'
                exchange.create_order(
                    symbol = symbol,
                    type   = 'market',
                    side   = close_side,
                    amount = pos['qty'],
                )
                emoji = "✅" if reason == 'TP HIT' else "🛑"
                print(f"   {emoji} {reason} — Position closed!")
                del open_positions[symbol]

        except Exception as e:
            print(f"   ❌ Monitor error {symbol}: {e}")


def get_open_trades(exchange, symbols):
    try:
        count = 0
        for symbol in symbols:
            orders = exchange.fetch_open_orders(symbol)
            count += len(orders)
        count += len(open_positions)
        return count
    except Exception as e:
        print(f"❌ Position check error: {e}")
        return len(open_positions)


def close_all_orders(exchange, symbol):
    try:
        exchange.cancel_all_orders(symbol)
        print(f"   ✅ All orders cancelled for {symbol}")
    except Exception as e:
        print(f"   ❌ Cancel error: {e}")