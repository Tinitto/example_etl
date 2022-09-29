"""Module for loading a StockRecord onto a CSV"""
import logging
from typing import Optional

from .lib import Load
from .dtos import StockRecord
from .utils import CSVFileWriter


class CSVLoad(Load):
    """Appends a given record to a CSV file of chosen path"""
    _headers = ["stock_symbol", "percentage_change", "current_price", "last_close_price"]

    def __init__(self, csv_file_path: str):
        self.__csv_file_path = csv_file_path

    def save(self, record: StockRecord):
        logging.info(f"Saving most volatile stock to CSV...\n")

        with CSVFileWriter(path=self.__csv_file_path, headers=self._headers) as csv_writer:
            csv_writer.writerow([getattr(record, header) for header in self._headers])

        logging.info(f"Done saving output to csv {self.__csv_file_path}\n")


