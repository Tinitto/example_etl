"""Module containing the core interfaces to be used in the script"""

from abc import abstractmethod
from dataclasses import dataclass
from functools import reduce
from typing import List, Dict, Any, Union, Iterator, Callable


class Extract:
    """Abstract class representing all possible extractors"""
    @abstractmethod
    def query(self, *args, **kwargs) -> Union[Iterator[List[Dict[str, Any]]], Iterator[Dict[str, Any]]]:
        raise NotImplementedError("to do")

    def __call__(self, *args, **kwargs):
        return self.query(*args, **kwargs)


class Transform:
    """Abstract class representing all possible transformers"""
    @abstractmethod
    def convert(self, *args, **kwargs) -> Any:
        raise NotImplementedError("to do")

    def __call__(self, *args, **kwargs):
        return self.convert(*args, **kwargs)


class Load:
    """Abstract class representing all possible loaders"""
    @abstractmethod
    def save(self, *args, **kwargs):
        raise NotImplementedError("to do")

    def __call__(self, *args, **kwargs):
        return self.save(*args, **kwargs)


def run_pipeline(*funcs: Callable):
    """
    Runs the funcs in a row, each passing on its output to the next
    """
    output = None

    for func in funcs:
        if output is None:
            output = func()
        else:
            output = func(output)

    return output

