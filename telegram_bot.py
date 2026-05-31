# ============================
#   TELEGRAM ALERTS
# ============================

import requests
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN  = os.environ.get('TELEGRAM_TOKEN')  or os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID') or os.getenv('TELEGRAM_CHAT_ID')


def send_message(message):
    """Send message to Telegram"""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("   ⚠️  Telegram not configured")
        return False

    try:
        url  = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {
            'chat_id'    : TELEGRAM_CHAT_ID,
            'text'       : message,
            'parse_mode' : 'HTML'
        }
        response = requests.post(url, data=data, timeout=10)
        if response.status_code == 200:
            print("   📱 Telegram alert sent!")
            return True
        else:
            print(f"   ⚠️  Telegram error: {response.text}")
            return False
    except Exception as e:
        print(f"   ⚠️  Telegram failed: {e}")
        return False


def alert_trade_opened(symbol, signal, entry, qty, sl, tp):
    emoji  = "✅" if signal == 'buy' else "🔴"
    action = "BUY" if signal == 'buy' else "SELL"
    msg = f"""🤖 <b>OKX SCALP BOT</b>

{emoji} <b>{action} Signal — {symbol}</b>

📊 Entry  : <code>{entry}</code>
🎯 TP     : <code>{tp}</code>
🛑 SL     : <code>{sl}</code>
📦 Qty    : <code>{qty}</code>

⏰ Time: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
    send_message(msg)


def alert_trade_closed(symbol, reason, profit, balance):
    emoji  = "💰" if "TP" in reason else "🛑"
    msg = f"""🤖 <b>OKX SCALP BOT</b>

{emoji} <b>Trade Closed — {symbol}</b>

📌 Result  : <b>{reason}</b>
💵 PnL     : <code>{profit:+.2f} USDT</code>
💰 Balance : <code>{balance:,.2f} USDT</code>

⏰ Time: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
    send_message(msg)


def alert_bot_started():
    msg = """🤖 <b>OKX SCALP BOT STARTED</b>

✅ Connected to OKX Demo
📊 Strategy: EMA+RSI+BB + H1 Filter
🪙 Pairs: BTC/USDT, ETH/USDT
⏰ Running every 5 minutes
🚀 Bot is live and scanning!"""
    send_message(msg)


def alert_signal_missed(symbol, reason):
    msg = f"""🤖 <b>OKX SCALP BOT</b>

⚠️ Signal missed — {symbol}
Reason: {reason}"""
    send_message(msg)