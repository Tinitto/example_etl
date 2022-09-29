"""Module for transforming data from the Finnhub API into records"""
import logging
from typing import Iterator, Dict, Any, Tuple, Optional

from core.dtos import StockRecord
from core.lib import Transform


class ParseDictTransform(Transform):
    """Transform for converting the dict got from Finnhub latest stock price query"""

    def convert(self, stream: Iterator[Tuple[str, Dict[str, Any]]]) -> Iterator[StockRecord]:
        """
        Convert an iterator of something like this:
        ("AAPL", {
            "c": 2398.875,
            "d": 12.755,
            "dp": 0.5345,
            "h": 2408.7,
            "l": 2350.28,
            "o": 2351,
            "pc": 2386.12,
            "t": 1657302188
        })

        to an iterator of

        StockRecord {
            current_price: 2398.875,
            stock_symbol: "AAPL",
            percentage_change: 0.5345,
            last_close_price: 2386.12
        }
        """
        return (StockRecord(
            current_price=data.get("c", 0),
            stock_symbol=stock_symbol,
            percentage_change=data.get("dp", 0),
            last_close_price=data.get("pc", 0)
        ) for (stock_symbol, data) in stream)


class MostVolatileStockTransform(Transform):
    """Returns the most volatile StockRecord from an iterator of StockRecord's"""

    def convert(self, stream: Iterator[StockRecord]) -> StockRecord:
        most_volatile_record: Optional[StockRecord] = None

        for record in stream:
            logging.info(f"record: {record}")
            if record.percentage_change is None:
                continue

            if most_volatile_record is None:
                most_volatile_record = record
            elif record.percentage_change > most_volatile_record.percentage_change:
                most_volatile_record = record

        if most_volatile_record is None:
            raise ValueError("Unable to find any record with a proper percentage change")

        return most_volatile_record
