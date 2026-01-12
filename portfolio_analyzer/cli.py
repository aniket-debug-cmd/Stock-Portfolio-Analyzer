"""
Command-Line Interface Module

Handles argument parsing, validation, and user-friendly error messages.
"""

import argparse
import sys
import os
from datetime import datetime

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass


def parse_arguments():
    """
    Parse and validate command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments with validated values
    """
    parser = argparse.ArgumentParser(
        description='Stock Portfolio Analyzer - Professional portfolio analysis tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Equal-weight portfolio
  python main.py --tickers AAPL MSFT TSLA
  
  # Custom weights
  python main.py --tickers AAPL MSFT TSLA --weights 0.4 0.3 0.3
  
  # Custom date range
  python main.py --tickers GOOGL AMZN --start-date 2023-01-01 --end-date 2023-12-31
  
  # Custom risk-free rate and output directory
  python main.py --tickers AAPL MSFT --risk-free-rate 0.04 --output-dir results
        """
    )
    
    # Required arguments
    parser.add_argument(
        '--tickers',
        nargs='+',
        required=True,
        help='List of stock ticker symbols (e.g., AAPL MSFT TSLA)'
    )
    
    # Optional arguments
    parser.add_argument(
        '--weights',
        nargs='+',
        type=float,
        default=None,
        help='Portfolio weights (must match number of tickers, will be normalized)'
    )
    
    parser.add_argument(
        '--start-date',
        type=str,
        default=None,
        help='Start date for data download (format: YYYY-MM-DD). If not specified, uses --period.'
    )
    
    parser.add_argument(
        '--end-date',
        type=str,
        default=None,
        help='End date for data download (format: YYYY-MM-DD). If not specified, uses today.'
    )
    
    parser.add_argument(
        '--period',
        type=str,
        default='1y',
        help='Time period if dates not specified (default: 1y). Options: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max'
    )
    
    parser.add_argument(
        '--risk-free-rate',
        type=float,
        default=0.03,
        help='Risk-free rate for Sharpe ratio calculation (default: 0.03 = 3%%)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='outputs',
        help='Directory to save output files (default: outputs/)'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Validate and process arguments
    validate_arguments(args)
    
    return args


def validate_arguments(args):
    """
    Validate command-line arguments and provide helpful error messages.
    
    Args:
        args: argparse.Namespace with parsed arguments
    
    Raises:
        SystemExit: If validation fails with helpful error message
    """
    # Convert tickers to uppercase
    args.tickers = [t.upper().strip() for t in args.tickers]
    
    # Remove empty tickers
    args.tickers = [t for t in args.tickers if t]
    
    if not args.tickers:
        print("❌ ERROR: At least one ticker symbol is required")
        sys.exit(1)
    
    # Validate weights if provided
    if args.weights:
        if len(args.weights) != len(args.tickers):
            print(f"❌ ERROR: Number of weights ({len(args.weights)}) must match number of tickers ({len(args.tickers)})")
            print(f"   Tickers: {args.tickers}")
            print(f"   Weights: {args.weights}")
            sys.exit(1)
        
        if any(w < 0 for w in args.weights):
            print("❌ ERROR: Weights cannot be negative")
            print(f"   Weights: {args.weights}")
            sys.exit(1)
        
        if sum(args.weights) == 0:
            print("❌ ERROR: Sum of weights cannot be zero")
            sys.exit(1)
    
    # Validate date format if provided
    if args.start_date:
        try:
            datetime.strptime(args.start_date, '%Y-%m-%d')
        except ValueError:
            print(f"❌ ERROR: Invalid start date format: {args.start_date}")
            print("   Expected format: YYYY-MM-DD (e.g., 2023-01-01)")
            sys.exit(1)
    
    if args.end_date:
        try:
            datetime.strptime(args.end_date, '%Y-%m-%d')
        except ValueError:
            print(f"❌ ERROR: Invalid end date format: {args.end_date}")
            print("   Expected format: YYYY-MM-DD (e.g., 2023-12-31)")
            sys.exit(1)
    
    # Validate that both start and end dates are provided together
    if (args.start_date and not args.end_date) or (args.end_date and not args.start_date):
        print("❌ ERROR: Both --start-date and --end-date must be provided together")
        sys.exit(1)
    
    # Validate date range
    if args.start_date and args.end_date:
        start = datetime.strptime(args.start_date, '%Y-%m-%d')
        end = datetime.strptime(args.end_date, '%Y-%m-%d')
        
        if start >= end:
            print("❌ ERROR: Start date must be before end date")
            print(f"   Start: {args.start_date}")
            print(f"   End: {args.end_date}")
            sys.exit(1)
    
    # Validate risk-free rate
    if args.risk_free_rate < 0 or args.risk_free_rate > 1:
        print(f"❌ ERROR: Risk-free rate should be between 0 and 1 (e.g., 0.03 for 3%%)")
        print(f"   Provided: {args.risk_free_rate}")
        sys.exit(1)
    
    # Validate output directory name (basic check)
    if not args.output_dir or args.output_dir.strip() == '':
        print("❌ ERROR: Output directory cannot be empty")
        sys.exit(1)


def print_configuration(args):
    """
    Print the configuration that will be used for analysis.
    
    Args:
        args: argparse.Namespace with parsed arguments
    """
    print("\n" + "="*80)
    print("🚀 STOCK PORTFOLIO ANALYZER")
    print("="*80)
    print(f"Tickers: {', '.join(args.tickers)}")
    
    if args.weights:
        print(f"Weights: {args.weights} (will be normalized)")
    else:
        print("Weights: Equal-weight (not specified)")
    
    if args.start_date and args.end_date:
        print(f"Date Range: {args.start_date} to {args.end_date}")
    else:
        print(f"Period: {args.period}")
    
    print(f"Risk-Free Rate: {args.risk_free_rate * 100:.1f}%")
    print(f"Output Directory: {args.output_dir}/")
    print("="*80)

