# ============================
#   BOT CONFIGURATION
# ============================

# Trading pairs
SYMBOLS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']

# Timeframe
TIMEFRAME    = '5m'
CANDLE_LIMIT = 100

# EMA settings
EMA_FAST = 13
EMA_SLOW = 34

# RSI settings
RSI_PERIOD   = 9
RSI_BUY_MIN  = 50
RSI_BUY_MAX  = 65
RSI_SELL_MIN = 35
RSI_SELL_MAX = 50

# Bollinger Bands
BB_PERIOD           = 20
BB_STD_DEV          = 2
BB_SQUEEZE_LOOKBACK = 20

# Risk management
RISK_PER_TRADE_PCT = 1.0
RISK_REWARD_RATIO  = 2.0
STOP_LOSS_PCT      = 0.8

# Trade limits
MAX_OPEN_TRADES = 1

# Time filter
TRADE_HOURS_START = 8
TRADE_HOURS_END   = 23
USE_TIME_FILTER   = False

# Trade type
TRADE_MODE = 'spot'