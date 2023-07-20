from datetime import datetime
import json
from time import mktime
import hmac
import hashlib

import pytz
import requests
from rich import print

from GmoWrapper.constants import (
    PUBLIC_ENDPOINT,
    PRIVATE_ENDPOINT,
    SIDE,
    ORDER_TYPE,
    TIME_IN_FORCE,
    INTERVAL_8STR,
    INTERVAL_4STR,
)
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
                headers = self._get_authentication(path, method)
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

    @staticmethod
    def convert_to_unixtime(datetime_str) -> int:
        """
        datetime_str: ISO format string
        """
        datetime_str = datetime_str.rstrip("Z")
        dt = datetime.fromisoformat(datetime_str)
        dt = dt.replace(tzinfo=pytz.UTC)
        unix_time = int(dt.timestamp())
        return unix_time

    @staticmethod
    def convert_to_jst(unixtime_int) -> str:
        """
        datetime: unixtime
        """
        dt = datetime.fromtimestamp(unixtime_int)
        jst = dt.strftime("%Y:%m:%d:%H:%M:%S")
        return jst

    def is_exchange_status(self) -> bool:
        path = "/v1/status"
        result = self._requests(self._public_endpoint + path, "GET")
        status = result.get("data", {}).get("status")
        if status == "OPEN":
            return True
        else:
            return False

    def get_ticker(self, symbol) -> dict:
        path = "/v1/ticker"
        params = {"symbol": symbol}
        result = self._requests(self._public_endpoint + path, "GET", params)
        if result:
            result = result.get("data", [{}])[0]
            data = {
                "ask": float(result["ask"]),
                "bid": float(result["bid"]),
                "high": float(result["high"]),
                "last": float(result["last"]),
                "low": float(result["low"]),
                "symbol": result["symbol"],
                "timestamp": self.convert_to_unixtime(result["timestamp"]),
                "volume": float(result["volume"]),
            }
            return data
        else:
            return {}

    def get_kline(self, symbol, interval, date) -> list:
        path = "/v1/klines"
        params = {"symbol": symbol, "interval": interval, "date": date}
        # Check if interval and date format match the allowed combinations
        if len(date) == 8 and interval not in INTERVAL_8STR:
            raise ValueError(
                f"Invalid interval '{interval}' for date format YYYYMMDD. Allowed values: 1min, 5min, 10min, 15min, 30min, 1hour."
            )
        elif len(date) == 4 and interval not in INTERVAL_4STR:
            raise ValueError(
                f"Invalid interval '{interval}' for date format YYYY. Allowed values: 4hour, 8hour, 12hour, 1day, 1week, 1month."
            )

        result = self._requests(self._public_endpoint + path, "GET", params)
        if result.get("status") == 0:
            data = []
            for kline in result.get("data"):
                timestamp = int(kline["openTime"]) // 1000
                data.append(
                    {
                        "timestamp": timestamp,
                        "jst": self.convert_to_jst(timestamp),
                        "open": float(kline["open"]),
                        "high": float(kline["high"]),
                        "low": float(kline["low"]),
                        "close": float(kline["close"]),
                        "volume": float(kline["volume"]),
                    }
                )
            return data
        else:
            print(result.get("messages"))
            return []

    def get_available_account(self) -> int:
        path = "/v1/account/margin"
        result = self._requests(self._private_endpoint + path, "GET")
        result = result.get("data", {}).get("availableAmount")
        return result

    def get_deal_result(self, order_id) -> dict:
        path = "/v1/executions"
        params = {"orderId": order_id}
        result = self._requests(self._private_endpoint + path, "GET", params)
        if result.get("data", {}).get("list") is None:
            data = {
                "filled_id": None,
                "fee": None,
                "loss_gain": None,
                "order_id": None,
                "price": None,
                "settle_type": None,
                "side": None,
                "size": None,
                "symbol": None,
                "timestamp": self.convert_to_unixtime(result["responsetime"]),
            }
        else:
            result = result.get("data", {}).get("list")[0]
            data = {
                "filled_id": result["executionId"],
                "fee": float(result["fee"]),
                "loss_gain": float(result["lossGain"]),
                "order_id": result["orderId"],
                "price": int(result["price"]),
                "settle_type": result["settleType"],
                "side": result["side"],
                "size": float(result["size"]),
                "symbol": result["symbol"],
                "timestamp": self.convert_to_unixtime(result["timestamp"]),
            }
        return data

    def get_latest_deal(self, symbol) -> int:
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

    def order(
        self, symbol, side, size, price=None, time_in_force=TIME_IN_FORCE["FAK"]
    ) -> dict:
        """
        Success return:
        {
            'status': 0,
            'data': '3681627737',
            'responsetime': '2023-07-19T11:37:01.903Z'
        }

        Failed return:
        {
            'status': 1,
            'messages': [
                {
                    'message_code': 'ERR-5106',
                    'message_string': 'Invalid request parameter. size'
                }
            ],
            'responsetime': '2023-07-19T11:36:35.494Z'
        }

        """
        path = "/v1/order"
        params = {
            "symbol": symbol,
            "timeInForce": time_in_force,
            "size": str(size),
        }
        if side == "BUY":
            params["side"] = SIDE["BUY"]
        elif side == "SELL":
            params["side"] = SIDE["SELL"]
        else:
            raise ValueError("side must be BUY or SELL")
        if price is None:
            params["executionType"] = ORDER_TYPE["MARKET"]
        else:
            params["executionType"] = ORDER_TYPE["LIMIT"]
            params["price"] = str(price)

        result = self._requests(self._private_endpoint + path, "POST", params)
        if result.get("status") == 0:
            print(result)
            data = {
                "order_id": result["data"],
                "timestamp": self.convert_to_unixtime(result["responsetime"]),
            }
        else:
            data = {
                "order_id": None,
                "timestamp": self.convert_to_unixtime(result["responsetime"]),
                "error_code": result["messages"][0]["message_code"],
                "error_message": result["messages"][0]["message_string"],
            }
        return data
