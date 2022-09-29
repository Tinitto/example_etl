"""Module containing tests for the loading part of the script"""
import csv
import os.path
from unittest import main, TestCase

from core.dtos import StockRecord
from core.load import CSVLoad

assets_path = os.path.join(os.path.dirname(__file__), "assets")


class TestCSVLoad(TestCase):
    """Tests for loading appending Stock records to CSVs"""

    def setUp(self) -> None:
        """Initialize some default variables"""
        self.csv_file_path = os.path.join(assets_path, "dummy_csv.csv")
        self._delete_file(self.csv_file_path)

    def test_save(self):
        """CSVLoad.save() should append the Stock record to the CSV file, creating it with headers if not exist"""
        records = [
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
        expected_content = ["stock_symbol,percentage_change,current_price,last_close_price",
                            "AAPL,0.5345,2398.875,2386.12",
                            "AAPX,0.7229,2403.37,2386.12",
                            "MPM,-0.6791,115.54,116.33", ]
        csv_load = CSVLoad(csv_file_path=self.csv_file_path)

        for record in records:
            csv_load(record)

        actual_content = self._read_rows_in_csv(self.csv_file_path)

        self.assertEqual(expected_content, actual_content)

    @staticmethod
    def _delete_file(path):
        """Deletes the file at the given path"""
        try:
            os.remove(path)
        except:
            pass

    @staticmethod
    def _read_rows_in_csv(path):
        """
        Reads the contents in the csv at the given path
        and returns a list of the comma-separated rows
        """
        with open(path) as file:
            csv_reader = csv.reader(file)
            return [",".join(row) for row in csv_reader]


if __name__ == '__main__':
    main()
