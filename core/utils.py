import csv
import logging
from typing import List, Optional, TextIO


class CSVFileWriter:
    """Class to write or append to a CSV file"""
    def __init__(self, path: str, headers: List[str]=()):
        self.__path = path
        self.__file_handle: Optional[TextIO] = None
        self.__headers = headers

    def __enter__(self):
        try:
            self.__file_handle = open(self.__path, "x")
            csv_writer = csv.writer(self.__file_handle)
            csv_writer.writerow(self.__headers)
        except FileExistsError:
            self.__file_handle = open(self.__path, "a")
            csv_writer = csv.writer(self.__file_handle)
        except Exception as exp:
            if self.__file_handle is not None:
                self.__file_handle.close()
            raise exp

        return csv_writer

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__file_handle is not None:
            self.__file_handle.close()


def setup_logger(file_path: Optional[str] = None):
    """Sets up the logger for the entire script"""
    logging.basicConfig(filename=file_path, level=logging.INFO)
