# ============================
#   BOT CONFIGURATION
#   Strategy: EMA+RSI+BB + H1 Trend Filter
# ============================

# Trading pairs
SYMBOLS = ['BTC/USDT', 'ETH/USDT']

# Timeframe
TIMEFRAME    = '5m'
CANDLE_LIMIT = 100

# Higher timeframe
HTF_TIMEFRAME = '1h'
HTF_CANDLES   = 50

# EMA settings
EMA_FAST = 13
EMA_SLOW = 34

# HTF EMA
HTF_EMA_FAST = 9
HTF_EMA_SLOW = 21

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

# Volume filter
VOLUME_MA_PERIOD  = 20
VOLUME_MULTIPLIER = 1.0

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