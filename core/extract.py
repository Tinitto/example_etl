"""Module for extracting latest stock price from Finnhub"""
import logging
import time
from typing import Dict, Any, Iterator, Tuple

import requests

from .config import finnhub_base_url, stock_symbols as default_stock_symbols
from .lib import Extract


class LatestSockPriceExtract(Extract):
    """Extracts the latest stock price for the given stock names; returning a stream of records"""
    _base_url = finnhub_base_url
    _wait_interval_map = {0: 1, 1: 60, 60: 180, 180: 420}

    def __init__(self, api_key: str, rate_limit: int, stock_symbols=default_stock_symbols):
        self._query_interval = 60 / rate_limit
        self._api_key = api_key
        self._stock_symbols = stock_symbols

    def query(self, *args, **kwargs) -> Iterator[Tuple[str, Dict[str, Any]]]:
        """Queries Finnhub and returns an iterator of the results"""
        index = 0
        num_of_stock_symbols = len(self._stock_symbols)
        logging.info(f"Starting extraction of latest stock prices at {self._query_interval} seconds intervals...\n")
        logging.info(f"This will take some time...\n")

        while index < num_of_stock_symbols:
            stock_symbol = self._stock_symbols[index]
            try:
                logging.info(f"Getting latest stock price for {stock_symbol}...")
                data = self._get_current_stock_price(stock_symbol=stock_symbol, wait_interval=0)
                yield stock_symbol, data
            except PermissionError as exp:
                logging.error(exp)

            time.sleep(self._query_interval)
            index += 1

    def _get_current_stock_price(self, stock_symbol: str, wait_interval: int) -> Dict[str, Any]:
        """
        Gets the current stock price for the given `stock_symbol`
        It will wait for the given `wait_interval` before making the request
        """
        # make the query
        time.sleep(wait_interval)
        url = f"{self._base_url}/api/v1/quote?symbol={stock_symbol}"
        resp = requests.get(url, headers={"X-Finnhub-Token": self._api_key})
        if resp.ok:
            return resp.json()

        if resp.status_code == 403:
            data = resp.json()
            error_msg = data.get("error", f"request for {stock_symbol} was unauthorized")
            raise PermissionError(error_msg)

        if resp.status_code == 429:
            if wait_interval > 300:
                raise TimeoutError(
                    "number of API calls to Finnhub exceeded."
                    "Check that you are not using the same key in"
                    "another script or something then try again in 2 minutes")
            new_wait_interval = self._wait_interval_map[wait_interval]
            return self._get_current_stock_price(stock_symbol=stock_symbol, wait_interval=new_wait_interval)
