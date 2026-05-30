# ============================
#   OKX CONNECTION
# ============================

import ccxt
import os
from dotenv import load_dotenv

load_dotenv()


def get_exchange():
    api_key    = os.environ.get('OKX_API_KEY') or os.getenv('OKX_API_KEY')
    secret_key = os.environ.get('OKX_SECRET_KEY') or os.getenv('OKX_SECRET_KEY')
    passphrase = os.environ.get('OKX_PASSPHRASE') or os.getenv('OKX_PASSPHRASE')
    mode       = os.environ.get('OKX_MODE') or os.getenv('OKX_MODE', 'demo')
    is_sandbox = (mode == 'demo')

    exchange = ccxt.okx({
        'apiKey'  : api_key,
        'secret'  : secret_key,
        'password': passphrase,
        'sandbox' : is_sandbox,
        'options' : {'defaultType': 'spot'},
    })

    return exchange, mode


def test_connection(exchange):
    print("\n🔌 Testing connection...")
    try:
        balance = exchange.fetch_balance()
        usdt    = float(balance.get('USDT', {}).get('free', 0))
        print(f"   ✅ Connected to OKX!")
        print(f"   💰 USDT Available: ${usdt:,.2f}")
        return True
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False


def get_balance(exchange):
    try:
        balance = exchange.fetch_balance()
        return float(balance.get('USDT', {}).get('free', 0))
    except Exception as e:
        print(f"❌ Balance error: {e}")
        return 0.0


def get_candles(exchange, symbol, timeframe, limit):
    try:
        return exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    except Exception as e:
        print(f"❌ Candle error [{symbol}]: {e}")
        return None