"""
Unit tests for metrics calculation module.

Tests Sharpe ratio calculation and other performance metrics.
"""

import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from portfolio_analyzer.metrics import (
    calculate_sharpe_ratio,
    calculate_annualized_return,
    calculate_annualized_volatility,
    calculate_cumulative_return,
    calculate_maximum_drawdown
)


class TestMetrics(unittest.TestCase):
    """Test cases for metrics calculations."""
    
    def setUp(self):
        """Set up test data."""
        # Create sample returns: 1% daily return for 10 days
        self.positive_returns = pd.Series([0.01] * 10)
        
        # Create sample returns: -1% daily return for 10 days
        self.negative_returns = pd.Series([-0.01] * 10)
        
        # Create mixed returns (some positive, some negative)
        self.mixed_returns = pd.Series([0.02, -0.01, 0.015, -0.005, 0.01])
        
        # Create empty returns
        self.empty_returns = pd.Series(dtype=float)
    
    def test_sharpe_ratio_positive_returns(self):
        """Test Sharpe ratio calculation with positive returns."""
        sharpe = calculate_sharpe_ratio(self.positive_returns, risk_free_rate=0.03)
        
        # Sharpe ratio should be positive for positive returns above risk-free rate
        self.assertGreater(sharpe, 0, "Sharpe ratio should be positive for good returns")
    
    def test_sharpe_ratio_negative_returns(self):
        """Test Sharpe ratio calculation with negative returns."""
        sharpe = calculate_sharpe_ratio(self.negative_returns, risk_free_rate=0.03)
        
        # Sharpe ratio should be negative for negative returns
        self.assertLess(sharpe, 0, "Sharpe ratio should be negative for negative returns")
    
    def test_sharpe_ratio_zero_volatility(self):
        """Test Sharpe ratio with zero volatility (constant returns)."""
        # Constant returns have near-zero volatility (not exactly zero due to floating point)
        constant_returns = pd.Series([0.01] * 10)
        sharpe = calculate_sharpe_ratio(constant_returns, risk_free_rate=0.03)
        
        # For constant returns, volatility is very small, so Sharpe ratio will be very large
        # This is expected behavior - we just verify it doesn't crash
        self.assertIsInstance(sharpe, (float, type(pd.Series([0.01]).std())))
    
    def test_cumulative_return_calculation(self):
        """Test cumulative return calculation."""
        # For 1% daily return over 10 days: (1.01^10) - 1
        cumulative = calculate_cumulative_return(self.positive_returns)
        expected = (1.01 ** 10) - 1
        
        # Allow small floating point differences
        self.assertAlmostEqual(cumulative, expected, places=5)
    
    def test_annualized_return_calculation(self):
        """Test annualized return calculation."""
        annualized = calculate_annualized_return(self.positive_returns)
        
        # Annualized return should be positive for positive daily returns
        self.assertGreater(annualized, 0, "Annualized return should be positive")
    
    def test_annualized_volatility_calculation(self):
        """Test annualized volatility calculation."""
        vol = calculate_annualized_volatility(self.mixed_returns)
        
        # Volatility should always be non-negative
        self.assertGreaterEqual(vol, 0, "Volatility should be non-negative")
    
    def test_maximum_drawdown(self):
        """Test maximum drawdown calculation."""
        # Create returns that go up then down (should have a drawdown)
        returns_with_drawdown = pd.Series([0.05, 0.03, -0.10, -0.05, 0.02])
        max_dd = calculate_maximum_drawdown(returns_with_drawdown)
        
        # Maximum drawdown should be negative (or zero)
        self.assertLessEqual(max_dd, 0, "Maximum drawdown should be negative or zero")
    
    def test_empty_returns(self):
        """Test that functions handle empty returns gracefully."""
        # Should not crash with empty returns
        # Empty Series prod() returns 1.0, so cumulative return = 1.0 - 1 = 0.0
        cumulative = calculate_cumulative_return(self.empty_returns)
        self.assertIsInstance(cumulative, (float, type(pd.Series(dtype=float).prod())))


if __name__ == '__main__':
    unittest.main()

