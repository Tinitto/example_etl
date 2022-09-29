"""Module containing the tests for the extract functionality"""
from datetime import datetime, timedelta
from typing import Dict, Any, List
from unittest import TestCase, main, mock

from core.extract import LatestSockPriceExtract


class MockResponse:
    def __init__(self, ok: bool, response_data: List[Dict[str, Any]]):
        self.ok = ok
        self.status_code = 200
        self.__response_data = (record for record in response_data)

    def json(self):
        return next(self.__response_data)


class TestExtract(TestCase):
    """Tests for extraction of latest stock price for the given stock_symbols"""

    @mock.patch("core.extract.requests.get")
    def test_query(self, mock_get: mock.MagicMock):
        """
        The query() method should make repeated GET
        requests to the Finnhub latest_stock endpoint
        """
        dummy_stock_symbols = ["uganda", "rwanda", "kenya"]
        dummy_response_data = [{"you": "uganda"}, {"you": "rwanda"}, {"you": "kenya"}]
        mock_response = MockResponse(ok=True, response_data=dummy_response_data)
        mock_get.return_value = mock_response
        rate_limit = 720
        api_key = "dummy"
        extract = LatestSockPriceExtract(api_key=api_key, rate_limit=rate_limit, stock_symbols=dummy_stock_symbols)
        expected_interval = timedelta(seconds=60 / rate_limit)
        start = datetime.now()

        i = 0
        for response in extract():
            if i > 0:
                elapsed = datetime.now() - start
                self.assertGreaterEqual(elapsed, expected_interval)
                self.assertLess(elapsed, expected_interval + timedelta(seconds=1))

            self.assertTupleEqual(response, (dummy_stock_symbols[i], dummy_response_data[i]))
            mock_get.assert_called_with(f"https://finnhub.io/api/v1/quote?symbol={dummy_stock_symbols[i]}",
                                        headers={'X-Finnhub-Token': api_key})

            i += 1
            start = datetime.now()


if __name__ == '__main__':
    main()
