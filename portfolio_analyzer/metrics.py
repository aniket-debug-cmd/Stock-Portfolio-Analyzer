"""
Metrics Calculation Module

Calculates performance metrics for individual assets including:
- Returns (daily, cumulative, annualized)
- Volatility (annualized)
- Sharpe ratio
- Maximum drawdown
- Rolling volatility
"""

import numpy as np
import pandas as pd

# Number of trading days per year (used for annualization)
TRADING_DAYS_PER_YEAR = 252


def calculate_returns(prices):
    """
    Calculate daily returns from price data.
    
    Daily return = (Price today - Price yesterday) / Price yesterday
    
    Args:
        prices: DataFrame with stock prices (dates as index, tickers as columns)
    
    Returns:
        pandas.DataFrame: DataFrame with daily returns (first row will be NaN, then dropped)
    """
    # Calculate percentage change day-over-day
    returns = prices.pct_change()
    
    # Remove the first row (which is NaN since there's no previous day)
    returns = returns.dropna()
    
    return returns


def calculate_cumulative_return(returns):
    """
    Calculate cumulative return over the entire period.
    
    Cumulative return = (1 + r1) * (1 + r2) * ... * (1 + rn) - 1
    
    Args:
        returns: Series or DataFrame of daily returns
    
    Returns:
        float or Series: Cumulative return as a decimal (e.g., 0.15 = 15%)
    """
    # Multiply (1 + return) for each day, then subtract 1
    cumulative = (1 + returns).prod() - 1
    return cumulative


def calculate_annualized_return(returns):
    """
    Calculate annualized return from daily returns.
    
    This projects the return to what it would be over a full year.
    
    Args:
        returns: Series of daily returns
    
    Returns:
        float: Annualized return as a decimal
    """
    if len(returns) == 0:
        return 0.0
    
    # Calculate cumulative return first
    cumulative_return = calculate_cumulative_return(returns)
    
    # Number of trading days in the data
    trading_days = len(returns)
    
    # Annualize: (1 + cumulative_return) ^ (252 / trading_days) - 1
    annualized = (1 + cumulative_return) ** (TRADING_DAYS_PER_YEAR / trading_days) - 1
    
    return annualized


def calculate_annualized_volatility(returns):
    """
    Calculate annualized volatility (standard deviation of returns).
    
    Volatility measures how much the price fluctuates. Higher volatility = more risk.
    We annualize by multiplying daily volatility by sqrt(252).
    
    Args:
        returns: Series of daily returns
    
    Returns:
        float: Annualized volatility as a decimal
    """
    if len(returns) == 0:
        return 0.0
    
    # Calculate standard deviation of daily returns
    daily_volatility = returns.std()
    
    # Annualize by multiplying by square root of trading days per year
    annualized_vol = daily_volatility * np.sqrt(TRADING_DAYS_PER_YEAR)
    
    return annualized_vol


def calculate_sharpe_ratio(returns, risk_free_rate=0.03):
    """
    Calculate Sharpe ratio (risk-adjusted return metric).
    
    Sharpe Ratio = (Annualized Return - Risk-Free Rate) / Annualized Volatility
    
    Higher Sharpe ratio = better risk-adjusted returns.
    A Sharpe ratio above 1 is considered good, above 2 is very good.
    
    Args:
        returns: Series of daily returns
        risk_free_rate: Risk-free rate as decimal (default: 0.03 = 3%)
    
    Returns:
        float: Sharpe ratio
    """
    annualized_return = calculate_annualized_return(returns)
    annualized_vol = calculate_annualized_volatility(returns)
    
    # Avoid division by zero
    if annualized_vol == 0:
        return 0.0
    
    sharpe = (annualized_return - risk_free_rate) / annualized_vol
    
    return sharpe


def calculate_maximum_drawdown(returns):
    """
    Calculate maximum drawdown (largest peak-to-trough decline).
    
    Drawdown measures the worst loss from a peak. Maximum drawdown is the
    largest such loss over the entire period.
    
    Args:
        returns: Series of daily returns
    
    Returns:
        float: Maximum drawdown as a decimal (negative value, e.g., -0.25 = -25%)
    """
    if len(returns) == 0:
        return 0.0
    
    # Calculate cumulative returns over time
    cumulative_returns = (1 + returns).cumprod()
    
    # Calculate running maximum (peak) at each point
    running_max = cumulative_returns.expanding().max()
    
    # Drawdown = (current value - peak) / peak
    drawdown = (cumulative_returns - running_max) / running_max
    
    # Maximum drawdown is the most negative value
    max_drawdown = drawdown.min()
    
    return max_drawdown


def calculate_rolling_volatility(returns, window=30):
    """
    Calculate rolling volatility over a specified window.
    
    This shows how volatility changes over time, which is useful for
    understanding periods of high and low risk.
    
    Args:
        returns: Series of daily returns
        window: Number of days for rolling window (default: 30)
    
    Returns:
        pandas.Series: Rolling annualized volatility
    """
    if len(returns) == 0:
        return pd.Series(dtype=float)
    
    # Calculate rolling standard deviation
    rolling_std = returns.rolling(window=window).std()
    
    # Annualize by multiplying by sqrt(252)
    rolling_vol = rolling_std * np.sqrt(TRADING_DAYS_PER_YEAR)
    
    return rolling_vol


def calculate_asset_metrics(returns, ticker, risk_free_rate=0.03):
    """
    Calculate all performance metrics for a single asset.
    
    This is the main function to call for individual asset analysis.
    It computes all key metrics and returns them in a dictionary.
    
    Args:
        returns: Series of daily returns for the asset
        ticker: Ticker symbol (for labeling)
        risk_free_rate: Risk-free rate for Sharpe ratio (default: 0.03)
    
    Returns:
        dict: Dictionary containing all calculated metrics
    """
    if len(returns) == 0:
        return None
    
    # Calculate all metrics
    cumulative_return = calculate_cumulative_return(returns)
    annualized_return = calculate_annualized_return(returns)
    annualized_vol = calculate_annualized_volatility(returns)
    sharpe_ratio = calculate_sharpe_ratio(returns, risk_free_rate)
    max_drawdown = calculate_maximum_drawdown(returns)
    trading_days = len(returns)
    
    # Return as dictionary with clear labels
    metrics = {
        'Ticker': ticker,
        'Cumulative Return (%)': cumulative_return * 100,
        'Annualized Return (%)': annualized_return * 100,
        'Annualized Volatility (%)': annualized_vol * 100,
        'Sharpe Ratio': sharpe_ratio,
        'Maximum Drawdown (%)': max_drawdown * 100,
        'Trading Days': trading_days
    }
    
    return metrics

