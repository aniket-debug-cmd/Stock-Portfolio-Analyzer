"""
Unit tests for portfolio calculation module.

Tests portfolio return calculation and weight validation.
"""

import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from portfolio_analyzer.portfolio import (
    calculate_portfolio_returns,
    validate_weights,
    calculate_portfolio_metrics
)


class TestPortfolio(unittest.TestCase):
    """Test cases for portfolio calculations."""
    
    def setUp(self):
        """Set up test data."""
        # Create sample returns DataFrame with 3 assets
        dates = pd.date_range('2023-01-01', periods=5, freq='D')
        self.returns = pd.DataFrame({
            'AAPL': [0.01, 0.02, -0.01, 0.015, 0.01],
            'MSFT': [0.015, 0.01, 0.02, -0.005, 0.02],
            'GOOGL': [0.02, -0.01, 0.01, 0.02, 0.015]
        }, index=dates)
    
    def test_portfolio_returns_equal_weights(self):
        """Test portfolio returns calculation with equal weights."""
        portfolio_returns = calculate_portfolio_returns(self.returns, weights=None)
        
        # Should return a Series with same length as input
        self.assertEqual(len(portfolio_returns), len(self.returns))
        
        # With equal weights, portfolio return should be average of asset returns
        expected_first = (self.returns.iloc[0].sum() / 3)
        self.assertAlmostEqual(portfolio_returns.iloc[0], expected_first, places=5)
    
    def test_portfolio_returns_custom_weights(self):
        """Test portfolio returns calculation with custom weights."""
        weights = [0.5, 0.3, 0.2]  # 50% AAPL, 30% MSFT, 20% GOOGL
        portfolio_returns = calculate_portfolio_returns(self.returns, weights=weights)
        
        # Should return a Series
        self.assertEqual(len(portfolio_returns), len(self.returns))
        
        # First day: 0.5*0.01 + 0.3*0.015 + 0.2*0.02 = 0.0135
        expected_first = 0.5 * 0.01 + 0.3 * 0.015 + 0.2 * 0.02
        self.assertAlmostEqual(portfolio_returns.iloc[0], expected_first, places=5)
    
    def test_validate_weights_equal_weight(self):
        """Test weight validation with None (equal weights)."""
        weights = validate_weights(None, num_tickers=3)
        
        # Should return equal weights that sum to 1
        self.assertEqual(len(weights), 3)
        self.assertAlmostEqual(weights.sum(), 1.0, places=5)
        np.testing.assert_array_almost_equal(weights, [1/3, 1/3, 1/3])
    
    def test_validate_weights_normalization(self):
        """Test that weights are normalized to sum to 1."""
        weights = [0.4, 0.3, 0.3]  # Already sum to 1
        normalized = validate_weights(weights, num_tickers=3)
        
        self.assertAlmostEqual(normalized.sum(), 1.0, places=5)
    
    def test_validate_weights_not_normalized(self):
        """Test that weights not summing to 1 are normalized."""
        weights = [0.4, 0.3, 0.2]  # Sum to 0.9, should be normalized
        normalized = validate_weights(weights, num_tickers=3)
        
        # Should sum to 1 after normalization
        self.assertAlmostEqual(normalized.sum(), 1.0, places=5)
        # Ratios should be preserved: 4:3:2
        self.assertAlmostEqual(normalized[0] / normalized[1], 4/3, places=3)
    
    def test_validate_weights_wrong_count(self):
        """Test that wrong number of weights raises error."""
        with self.assertRaises(ValueError):
            validate_weights([0.5, 0.5], num_tickers=3)
    
    def test_validate_weights_negative(self):
        """Test that negative weights raise error."""
        with self.assertRaises(ValueError):
            validate_weights([0.5, -0.5, 1.0], num_tickers=3)
    
    def test_validate_weights_zero_sum(self):
        """Test that zero-sum weights raise error."""
        with self.assertRaises(ValueError):
            validate_weights([0.0, 0.0, 0.0], num_tickers=3)
    
    def test_portfolio_metrics_calculation(self):
        """Test portfolio metrics calculation."""
        weights = [0.4, 0.3, 0.3]
        metrics = calculate_portfolio_metrics(self.returns, weights=weights, risk_free_rate=0.03)
        
        # Should return dictionary with expected keys
        self.assertIn('Portfolio Cumulative Return (%)', metrics)
        self.assertIn('Portfolio Annualized Return (%)', metrics)
        self.assertIn('Portfolio Annualized Volatility (%)', metrics)
        self.assertIn('Portfolio Sharpe Ratio', metrics)
        self.assertIn('Weights', metrics)
        
        # Weights should match input (normalized)
        self.assertEqual(len(metrics['Weights']), 3)


if __name__ == '__main__':
    unittest.main()

