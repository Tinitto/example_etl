"""Module containing tests for transforming"""
import types
from unittest import TestCase, main

from core.dtos import StockRecord
from core.transform import ParseDictTransform, MostVolatileStockTransform


class TestParseDictTransform(TestCase):
    """Tests for the ParseDictTransform class"""

    def test_convert(self):
        """Converts a stream of tuples of (stock_symbol, dict of data) to a stream of StockRecord"""
        transform = ParseDictTransform()
        input_list = [
            ("AAPL", {
                "c": 2398.875,
                "d": 12.755,
                "dp": 0.5345,
                "h": 2408.7,
                "l": 2350.28,
                "o": 2351,
                "pc": 2386.12,
                "t": 1657302188
            }),
            ("AAPX", {
                "c": 2403.37,
                "d": 17.25,
                "dp": 0.7229,
                "h": 2408.7,
                "l": 2350.28,
                "o": 2351,
                "pc": 2386.12,
                "t": 1657310404
            }),
            ("MPM", {
                "c": 115.54,
                "d": -0.79,
                "dp": -0.6791,
                "h": 116.58,
                "l": 113.7,
                "o": 114.6,
                "pc": 116.33,
                "t": 1657310404
            })
        ]

        expected_output = [
            StockRecord(
                current_price=2398.875,
                stock_symbol="AAPL",
                percentage_change=0.5345,
                last_close_price=2386.12,
            ),
            StockRecord(
                current_price=2403.37,
                stock_symbol="AAPX",
                percentage_change=0.7229,
                last_close_price=2386.12,
            ),
            StockRecord(
                current_price=115.54,
                stock_symbol="MPM",
                percentage_change=-0.6791,
                last_close_price=116.33,
            ),
        ]
        actual_output = transform((item for item in input_list))
        self.assertIsInstance(actual_output, types.GeneratorType)
        self.assertListEqual(expected_output, list(actual_output))


class TestMostVolatileStockTransform(TestCase):
    """Tests for the MostVolatileStockTransform class"""

    def test_convert(self):
        """Converts a stream of StockRecord to a single StockRecord with the highest percentage_change"""
        transform = MostVolatileStockTransform()
        input_list = [
            StockRecord(
                current_price=2398.875,
                stock_symbol="AAPL",
                percentage_change=0.5345,
                last_close_price=2386.12,
            ),
            StockRecord(
                current_price=2403.37,
                stock_symbol="AAPX",
                percentage_change=0.7229,
                last_close_price=2386.12,
            ),
            StockRecord(
                current_price=115.54,
                stock_symbol="MPM",
                percentage_change=-0.6791,
                last_close_price=116.33,
            ),
        ]
        expected_output = input_list[1]
        actual_output = transform((item for item in input_list))
        self.assertIsInstance(actual_output, StockRecord)
        self.assertEqual(expected_output, actual_output)


if __name__ == '__main__':
    main()
