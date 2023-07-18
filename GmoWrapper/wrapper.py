from datetime import datetime
import json
from time import mktime
import hmac
import hashlib

import requests
from rich import print

from GmoWrapper.constants import PUBLIC_ENDPOINT, PRIVATE_ENDPOINT
from GmoWrapper.load_api import load_config


class GmoWrapper:
    def __init__(self, api_file_name="gmo_api.json"):
        self._public_endpoint = PUBLIC_ENDPOINT
        self._private_endpoint = PRIVATE_ENDPOINT

        self._api_key, self._secret_key = load_config(api_file_name)

    def _requests(self, path, method, params=None) -> dict:
        if "private" in path:
            if method == "POST":
                headers = self._get_authentication(path, method, params)
                response = requests.post(path, headers=headers, data=json.dumps(params))
            elif method == "GET":
                headers = self._get_authentication(method, path)
                response = requests.get(path, headers=headers, params=params)
            else:
                raise ValueError(
                    "method must be POST or GET"
                )  # todo: need to make delete method
                return {}
            return response.json()
        else:
            if method == "POST":
                response = requests.post(path, params)
            elif method == "GET":
                response = requests.get(path, params)
            else:
                return {}
            return response.json()

    def _get_authentication(self, path, method, params=None):
        timestamp = "{0}000".format(int(mktime(datetime.now().timetuple())))
        if method == "POST":
            text = (
                timestamp
                + method
                + path.replace(self._private_endpoint, "")
                + json.dumps(params)
            )
        elif method == "GET":
            text = timestamp + method + path.replace(self._private_endpoint, "")
        else:
            raise ValueError(
                "method must be POST or GET"
            )  # todo: need to make delete method
        sign = hmac.new(
            bytes(self._secret_key.encode("ascii")),
            bytes(text.encode("ascii")),
            hashlib.sha256,
        ).hexdigest()

        headers = {
            "API-KEY": self._api_key,
            "API-TIMESTAMP": timestamp,
            "API-SIGN": sign,
        }
        return headers

    def is_exchange_status(self) -> bool:
        path = "/v1/status"
        result = self._requests(self._public_endpoint + path, "GET")
        status = result.get("data", {}).get("status")
        if status == 'OPEN':
            return True
        else:
            return False

    def get_ticker(self, symbol) -> dict:
        path = "/v1/ticker"
        params = {"symbol": symbol}
        result = self._requests(self._public_endpoint + path, "GET", params)
        if not result:
            result = result.get("data", [{}])[0]
        else:
            result = {}
        return result

    def get_available_account(self):
        path = "/v1/account/margin"
        result = self._requests(self._private_endpoint + path, "GET")
        result = result.get("data", {}).get("availableAmount")
        return result

    def get_deal_result(self, order_id):
        path = "/v1/executions"
        params = {"orderId": order_id}
        result = self._requests(self._private_endpoint + path, "GET", params)
        result = result.get("data", {}).get("list")
        return result

    def get_latest_deal(self, symbol):
        path = "/v1/latestExecutions"
        params = {"symbol": symbol, "page": 1, "count": 100}
        result = self._requests(self._private_endpoint + path, "GET", params)
        result = result.get("data", {}).get("list", [{}])[0].get("timestamp")
        if result is not None:
            result = result.split("-")
            result[2] = result[2][:2]
            latest_trade_day = ""
            for _ in result:
                latest_trade_day += _
            return latest_trade_day

    def order(self, symbol, side, size, price=None, time_in_force="FAK"):
        path = "/v1/order"
        params = {
            "symbol": symbol,
            "timeInForce": time_in_force,
            "size": str(size),
        }
        if side == "BUY":
            params["side"] = "BUY"
        elif side == "SELL":
            params["side"] = "SELL"
        else:
            raise ValueError("side must be BUY or SELL")
        if price is None:
            params["executionType"] = "MARKET"
        else:
            params["executionType"] = "LIMIT"
            params["price"] = str(price)

        result = self._requests(self._private_endpoint + path, "POST", params)
        print(result)
        # result = int(result.get("data", 0))
        # print(result)
        # self.get_deal_result(result)
        return result
