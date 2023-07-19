from rich import print

from GmoWrapper.wrapper import GmoWrapper
from GmoWrapper.constants import (
    PUBLIC_ENDPOINT,
    PRIVATE_ENDPOINT,
    SYMBOL,
    MIN_ORDER_QUANTITIES,
    SIDE,
    ORDER_TYPE,
    TIME_IN_FORCE,
)

gmo = GmoWrapper()

# res = gmo.is_exchange_status()
# print(res)

# res = gmo.get_ticker(symbol=SYMBOL["BTC"])
# print(res)

# res = gmo.get_kline(symbol=SYMBOL["BTC"], interval="1day", date='2023')
# print(res)

# res =gmo.get_available_account()
# print(res)

# res = gmo.get_deal_result(order_id=3680690655)
# print(res)

# res = gmo.get_latest_deal(symbol=SYMBOL["BTC"])
# print(res)

# res = gmo.order(
#         symbol=SYMBOL["BTC"],
#         side=SIDE["BUY"],
#         size=MIN_ORDER_QUANTITIES["BTC"],
#         price=None,
#         time_in_force="FAK"
#         )
# print(res)
