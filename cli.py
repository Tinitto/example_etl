"""Entry point for the script"""
import logging
from typing import Optional

import typer
from core.utils import setup_logger

from core.config import default_api_rate_limit, destination_file
from core.extract import LatestSockPriceExtract
from core.lib import run_pipeline
from core.transform import ParseDictTransform, MostVolatileStockTransform
from core.load import CSVLoad


def main(
        api_key: str = typer.Option(..., help="the Finnhub API key, whether for sandbox or for live"),
        api_rate_limit: int = typer.Option(default_api_rate_limit,
                                           help="the number of API requests per minute allowed for the given api key"),
        csv_file_path: str = typer.Option(destination_file,
                                          help="path to the CSV file where to save the most volatile stock record"),
        log_file_path: Optional[str] = typer.Option(None, help="path to a log file where any logs can be output")):
    """
    Retrieves the latest stock prices for Apple, Amazon, Netflix, Facebook, Google
    and gets the most volatile of those and saves them in a CSV at `csv_file_path`
    """
    setup_logger(log_file_path)
    extract = LatestSockPriceExtract(api_key=api_key, rate_limit=api_rate_limit)
    transform_dicts_to_records = ParseDictTransform()
    get_most_volatile_record = MostVolatileStockTransform()
    load_to_csv = CSVLoad(csv_file_path=csv_file_path)

    run_pipeline(
        extract,
        transform_dicts_to_records,
        get_most_volatile_record,
        load_to_csv
    )


if __name__ == '__main__':
    typer.run(main)
