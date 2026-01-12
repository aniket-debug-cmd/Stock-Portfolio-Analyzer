Stock Portfolio Analyzer

A Python-based tool for analyzing equity portfolios using historical market data.
The project focuses on modular design, reproducible analysis, and basic risk/return metrics commonly used in portfolio evaluation.

Overview

This project downloads historical stock price data and computes portfolio-level and asset-level performance metrics such as returns, volatility, Sharpe ratio, and maximum drawdown. It also generates visualizations to compare portfolio performance against individual assets.

The codebase is structured as a Python package with separate modules for data loading, metric computation, portfolio logic, visualization, and CLI handling.

Features

Fetches historical stock data using Yahoo Finance

Computes key performance and risk metrics

Supports custom portfolio weights

Generates CSV summaries and performance plots

Command-line interface with argument validation

Unit tests for core calculations

Tech Stack

Python 3.7+

pandas – data manipulation

numpy – numerical computations

yfinance – market data retrieval

matplotlib – visualization

tabulate – formatted console output

unittest – testing framework

Project Structure
Stock-Portfolio-Analyzer/
├── portfolio_analyzer/
│   ├── data_loader.py        # Market data retrieval
│   ├── metrics.py            # Asset-level metrics
│   ├── portfolio.py          # Portfolio calculations
│   ├── visualization.py      # Plots and charts
│   ├── cli.py                # CLI argument parsing
│   └── __init__.py
├── tests/
│   ├── test_metrics.py
│   ├── test_portfolio.py
│   ├── test_cli.py
│   └── __init__.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore

Setup
1. Create virtual environment
python -m venv venv


Activate it:

Windows:

venv\Scripts\activate


macOS/Linux:

source venv/bin/activate

2. Install dependencies
pip install -r requirements.txt

Usage
Basic example
python main.py --tickers AAPL MSFT TSLA

Custom weights
python main.py --tickers AAPL MSFT TSLA --weights 0.4 0.3 0.3

Date range
python main.py --tickers GOOGL AMZN --start-date 2023-01-01 --end-date 2023-12-31

Full example
python main.py \
  --tickers AAPL MSFT GOOGL \
  --weights 0.5 0.3 0.2 \
  --start-date 2023-01-01 \
  --end-date 2023-12-31 \
  --risk-free-rate 0.035 \
  --output-dir outputs

Output

After execution, the following files are generated:

portfolio_summary.csv

Contains:

Cumulative return

Annualized return

Annualized volatility

Sharpe ratio

Maximum drawdown

Number of trading days

Includes both individual assets and portfolio-level results.

portfolio_analysis.png

Includes:

Normalized portfolio value over time

Normalized individual asset performance

Rolling 30-day volatility

Testing

Run all unit tests:

python -m unittest discover tests


Tests cover:

Return and volatility calculations

Sharpe ratio and drawdown logic

Portfolio weight validation

CLI argument validation

Design Notes

Daily adjusted close prices are used for calculations

Portfolio weights are normalized internally

Calculations assume 252 trading days per year

Data retrieval failures are handled with validation checks

Limitations

Does not account for transaction costs, taxes, or dividends

Assumes long-only portfolios

Relies on Yahoo Finance data availability and accuracy

Uses daily frequency only

Possible Improvements

Support for additional asset classes

Inclusion of transaction costs and rebalancing

Interactive dashboard (e.g., Streamlit)

More advanced risk metrics (VaR, CVaR)

Disclaimer

This project is intended for educational and analytical purposes only and should not be used as financial advice.
