"""
Stock Portfolio Analyzer Package

A professional tool for analyzing stock portfolios with historical data,
calculating performance metrics, and generating visualizations.
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from .data_loader import download_stock_data
from .metrics import calculate_returns, calculate_asset_metrics
from .portfolio import calculate_portfolio_returns, calculate_portfolio_metrics
from .visualization import create_visualizations

__all__ = [
    'download_stock_data',
    'calculate_returns',
    'calculate_asset_metrics',
    'calculate_portfolio_returns',
    'calculate_portfolio_metrics',
    'create_visualizations',
]

