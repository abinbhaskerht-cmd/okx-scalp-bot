# ============================
#   ORDER EXECUTION
# ============================

from config import TRADE_MODE


def place_order(exchange, symbol, signal, qty, sl, tp):
    side = 'buy' if signal == 'buy' else 'sell'

    print(f"\n🚀 Placing {side.upper()} order...")
    print(f"   Symbol : {symbol}")
    print(f"   Qty    : {qty}")
    print(f"   SL     : {sl}")
    print(f"   TP     : {tp}")

    try:
        # Simple market order first
        order = exchange.create_order(
            symbol = symbol,
            type   = 'market',
            side   = side,
            amount = qty,
        )

        print(f"   ✅ Order placed!")
        print(f"   Order ID: {order['id']}")

        # Place TP limit order
        tp_side = 'sell' if signal == 'buy' else 'buy'
        try:
            tp_order = exchange.create_order(
                symbol = symbol,
                type   = 'limit',
                side   = tp_side,
                amount = qty,
                price  = tp,
            )
            print(f"   ✅ TP order placed at {tp}")
        except Exception as e:
            print(f"   ⚠️ TP order failed: {e}")

        return order

    except Exception as e:
        print(f"   ❌ Order failed: {e}")
        return None


def get_open_trades(exchange, symbols):
    try:
        count = 0
        for symbol in symbols:
            orders = exchange.fetch_open_orders(symbol)
            count += len(orders)
        return count
    except Exception as e:
        print(f"❌ Position check error: {e}")
        return 0


def close_all_orders(exchange, symbol):
    try:
        exchange.cancel_all_orders(symbol)
        print(f"   ✅ All orders cancelled for {symbol}")
    except Exception as e:
        print(f"   ❌ Cancel error: {e}")