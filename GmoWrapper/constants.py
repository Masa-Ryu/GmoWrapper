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
    "ETH": 0.001,
    "BCH": 0.002,
    "LTC": 0.01,
    "XRP": 2,
    "XEM": 1,
    "XLM": 5,
    "BAT": 2,
    "OMG": 0.3,
    "XTZ": 0.5,
    "QTUM": 0.1,
    "ENJ": 1,
    "DOT": 0.1,
    "ATOM": 1,  # Please confirm
    "MKR": 0.01,  # Please confirm
    "DAI": 1,  # Please confirm
    "XYM": 1,  # Please confirm
    "MONA": 1,  # Please confirm
    "FCR": 1,  # Please confirm
    "ADA": 1,  # Please confirm
    "LINK": 1,  # Please confirm
    "ASTR": 1,  # Please confirm
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
