PUBLIC_ENDPOINT = "https://api.coin.z.com/public"
PRIVATE_ENDPOINT = "https://api.coin.z.com/private"
SYMBOL = {
    "BTC": "BTC",
    "ETH": "ETH",
    "BCH": "BCH",
    "LTC": "LTC",
    "XRP": "XRP",
    "XEM": "XEM",
    "XLM": "XLM",
    "BAT": "BAT",
    "OMG": "OMG",
    "XTZ": "XTZ",
    "QTUM": "QTUM",
    "ENJ": "ENJ",
    "DOT": "DOT",
    "ATOM": "ATOM",
    "MKR": "MKR",
    "DAI": "DAI",
    "XYM": "XYM",
    "MONA": "MONA",
    "FCR": "FCR",
    "ADA": "ADA",
    "LINK": "LINK",
    "ASTR": "ASTR",
}
MIN_ORDER_QUANTITIES = {
    "BTC": 0.0001,
    "ETH": 0.01,
    "BCH": 0.01,
    "LTC": 0.1,
    "XRP": 1,
    "XEM": 1,
    "XLM": 1,
    "BAT": 1,
    "OMG": 0.1,
    "XTZ": 0.1,
    "QTUM": 0.1,
    "ENJ": 1,
    "DOT": 0.1,
    "ATOM": 0.01,
    "MKR": 0.001,
    "DAI": 1,
    "XYM": 1,
    "MONA": 1,
    "FCR": 10,
    "ADA": 1,
    "LINK": 0.1,
    "ASTR": 10,
}

SIDE = {
    "BUY": "BUY",
    "SELL": "SELL",
}
ORDER_TYPE = {
    "MARKET": "MARKET",
    "LIMIT": "LIMIT",
    "STOP": "STOP",
}
TIME_IN_FORCE = {
    "FAK": "FAK",
    "FAS": "FAS",
    "FOK": "FOK",
    "SOK": "SOK",
}

INTERVAL_8STR = ("1min", "5min", "10min", "15min", "30min", "1hour")
INTERVAL_4STR = ("4hour", "8hour", "12hour", "1day", "1week", "1month")
