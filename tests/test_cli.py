"""
Unit tests for CLI validation module.

Tests argument validation and weight checking.
"""

import unittest
import sys
import os
from unittest.mock import patch

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from portfolio_analyzer.cli import validate_arguments
from portfolio_analyzer.portfolio import validate_weights


class TestCLI(unittest.TestCase):
    """Test cases for CLI validation."""
    
    def test_validate_weights_matching_count(self):
        """Test weight validation when counts match."""
        # Should not raise error
        try:
            weights = validate_weights([0.4, 0.3, 0.3], num_tickers=3)
            self.assertEqual(len(weights), 3)
        except ValueError:
            self.fail("validate_weights raised ValueError unexpectedly")
    
    def test_validate_weights_mismatch_count(self):
        """Test weight validation when counts don't match."""
        with self.assertRaises(ValueError):
            validate_weights([0.5, 0.5], num_tickers=3)
    
    def test_validate_weights_sum_to_one(self):
        """Test that normalized weights sum to 1."""
        weights = [0.4, 0.3, 0.3]
        normalized = validate_weights(weights, num_tickers=3)
        
        self.assertAlmostEqual(sum(normalized), 1.0, places=5)
    
    def test_validate_weights_negative(self):
        """Test that negative weights are rejected."""
        with self.assertRaises(ValueError):
            validate_weights([-0.5, 0.5, 1.0], num_tickers=3)


if __name__ == '__main__':
    unittest.main()

