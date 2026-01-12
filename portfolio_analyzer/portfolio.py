"""
Portfolio Calculation Module

Handles portfolio-level calculations including:
- Weighted portfolio returns
- Portfolio performance metrics
- Weight validation and normalization
"""

import numpy as np
import pandas as pd
from .metrics import (
    calculate_cumulative_return,
    calculate_annualized_return,
    calculate_annualized_volatility,
    calculate_sharpe_ratio,
    calculate_maximum_drawdown,
    TRADING_DAYS_PER_YEAR
)


def validate_weights(weights, num_tickers):
    """
    Validate that weights are correct.
    
    Checks:
    - Number of weights matches number of tickers
    - All weights are non-negative
    - Sum of weights is not zero
    
    Args:
        weights: List of weights (can be None)
        num_tickers: Number of tickers in portfolio
    
    Returns:
        numpy.ndarray: Normalized weights that sum to 1
    
    Raises:
        ValueError: If validation fails
    """
    if weights is None:
        # Equal weights if not specified
        return np.array([1.0 / num_tickers] * num_tickers)
    
    weights = np.array(weights)
    
    # Check number of weights matches number of tickers
    if len(weights) != num_tickers:
        raise ValueError(
            f"Number of weights ({len(weights)}) must match number of tickers ({num_tickers})"
        )
    
    # Check for negative weights
    if any(w < 0 for w in weights):
        raise ValueError("Weights cannot be negative")
    
    # Check sum is not zero
    if np.sum(weights) == 0:
        raise ValueError("Sum of weights cannot be zero")
    
    # Normalize weights to sum to 1
    normalized_weights = weights / np.sum(weights)
    
    return normalized_weights


def calculate_portfolio_returns(returns, weights=None):
    """
    Calculate portfolio daily returns from individual asset returns.
    
    Portfolio return = sum(weight_i * return_i) for all assets i
    
    This gives us the daily return of the portfolio as a whole.
    
    Args:
        returns: DataFrame with daily returns (columns = tickers, index = dates)
        weights: Optional list of weights (will be normalized to sum to 1)
                 If None, uses equal weights
    
    Returns:
        pandas.Series: Daily returns of the portfolio
    """
    num_tickers = len(returns.columns)
    
    # Validate and normalize weights
    normalized_weights = validate_weights(weights, num_tickers)
    
    # Calculate weighted average of returns
    # Multiply each asset's returns by its weight, then sum across assets
    portfolio_returns = (returns * normalized_weights).sum(axis=1)
    
    return portfolio_returns


def calculate_portfolio_metrics(returns, weights=None, risk_free_rate=0.03):
    """
    Calculate all performance metrics for the portfolio.
    
    This computes portfolio-level metrics using the weighted portfolio returns.
    Similar to individual asset metrics but for the combined portfolio.
    
    Args:
        returns: DataFrame with daily returns for all assets
        weights: Optional list of portfolio weights
        risk_free_rate: Risk-free rate for Sharpe ratio (default: 0.03)
    
    Returns:
        dict: Dictionary containing portfolio metrics and weights
    """
    # Calculate portfolio daily returns
    portfolio_returns = calculate_portfolio_returns(returns, weights)
    
    # Get normalized weights for output
    num_tickers = len(returns.columns)
    normalized_weights = validate_weights(weights, num_tickers)
    
    # Calculate portfolio metrics (same as individual asset metrics)
    cumulative_return = calculate_cumulative_return(portfolio_returns)
    annualized_return = calculate_annualized_return(portfolio_returns)
    annualized_vol = calculate_annualized_volatility(portfolio_returns)
    sharpe_ratio = calculate_sharpe_ratio(portfolio_returns, risk_free_rate)
    max_drawdown = calculate_maximum_drawdown(portfolio_returns)
    
    # Create weights dictionary for easy access
    weights_dict = dict(zip(returns.columns, normalized_weights))
    
    # Return all metrics
    metrics = {
        'Portfolio Cumulative Return (%)': cumulative_return * 100,
        'Portfolio Annualized Return (%)': annualized_return * 100,
        'Portfolio Annualized Volatility (%)': annualized_vol * 100,
        'Portfolio Sharpe Ratio': sharpe_ratio,
        'Portfolio Maximum Drawdown (%)': max_drawdown * 100,
        'Weights': weights_dict
    }
    
    return metrics

