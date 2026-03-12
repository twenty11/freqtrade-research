from enum import Enum


class TradingMode(str, Enum):
    SPOT = "spot"
    FUTURES = "futures"
