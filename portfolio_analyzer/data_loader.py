"""
Data Loading Module

Handles downloading historical stock data from Yahoo Finance.
Supports both period-based and date range-based downloads.
"""

import sys
from datetime import datetime
import pandas as pd
import yfinance as yf

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass


def download_stock_data(tickers, start_date=None, end_date=None, period="1y"):
    """
    Download historical stock data for given tickers.
    
    This function downloads closing prices for the specified tickers.
    It can use either a period string (like "1y") or specific start/end dates.
    
    Args:
        tickers: List of stock ticker symbols (e.g., ['AAPL', 'MSFT'])
        start_date: Optional start date string (format: 'YYYY-MM-DD')
        end_date: Optional end date string (format: 'YYYY-MM-DD')
        period: Time period string if dates not provided (default: "1y")
                Options: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    
    Returns:
        pandas.DataFrame: DataFrame with dates as index and tickers as columns
                          Contains closing prices for each ticker
    
    Raises:
        SystemExit: If no data could be downloaded for any ticker
    """
    print(f"\n📥 Downloading data for {len(tickers)} ticker(s)...")
    
    data = {}
    failed_tickers = []
    
    # Download data for each ticker
    for ticker in tickers:
        try:
            print(f"  Fetching {ticker}...", end=" ")
            stock = yf.Ticker(ticker)
            
            # Use date range if provided, otherwise use period
            if start_date and end_date:
                hist = stock.history(start=start_date, end=end_date)
            else:
                hist = stock.history(period=period)
            
            # Check if we got any data
            if hist.empty:
                print(f"❌ No data found")
                failed_tickers.append(ticker)
                continue
            
            # Extract closing prices
            data[ticker] = hist['Close']
            print(f"✅ {len(hist)} days of data")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            failed_tickers.append(ticker)
    
    # Validate that we got at least some data
    if not data:
        print("\n❌ ERROR: No data could be downloaded for any ticker.")
        print("   Please check:")
        print("   - Ticker symbols are correct (e.g., 'AAPL' not 'APPLE')")
        print("   - Internet connection is working")
        print("   - Date range is valid (if specified)")
        sys.exit(1)
    
    # Warn about failed tickers but continue with successful ones
    if failed_tickers:
        print(f"\n⚠️  Warning: Failed to download data for: {', '.join(failed_tickers)}")
        print(f"Continuing with {len(data)} ticker(s)...")
    
    # Combine all ticker data into a single DataFrame
    df = pd.DataFrame(data)
    df.index.name = 'Date'
    
    # Sort by date to ensure chronological order
    df = df.sort_index()
    
    return df

