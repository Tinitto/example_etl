from dataclasses import dataclass


@dataclass
class StockRecord:
    """Data Transfer Object for all stock price records"""
    stock_symbol: str
    percentage_change: float
    current_price: float
    last_close_price: float
