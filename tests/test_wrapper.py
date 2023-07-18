from rich import print

from GmoWrapper.wrapper import GmoWrapper
from GmoWrapper.constants import PUBLIC_ENDPOINT, PRIVATE_ENDPOINT

gmo = GmoWrapper()

res = gmo.is_exchange_status()
print(res)

# res = gmo.get_ticker()
# print(res)

# res =gmt.get_available_account()
# print(res)

# res = gmo.get_deal_result(order_id=)
# print(res)

# res = gmo.get_latest_deal(symbol=)
# print(res)

# res = gmo.order(symbol=, side=, size=, price=None, time_in_force="FAK")
# print(res)
