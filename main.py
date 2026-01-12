#!/usr/bin/env python3
"""
Stock Portfolio Analyzer - Main Entry Point

This is the main script that orchestrates the portfolio analysis workflow.
It handles data loading, metric calculation, visualization, and output generation.
"""

import os
import sys
from tabulate import tabulate
import pandas as pd

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# Import our custom modules
from portfolio_analyzer.data_loader import download_stock_data
from portfolio_analyzer.metrics import calculate_returns, calculate_asset_metrics
from portfolio_analyzer.portfolio import calculate_portfolio_returns, calculate_portfolio_metrics
from portfolio_analyzer.visualization import create_visualizations
from portfolio_analyzer.cli import parse_arguments, print_configuration


def save_results_to_csv(individual_metrics, portfolio_metrics, output_dir="outputs"):
    """
    Save analysis results to a CSV file.
    
    Creates a summary table with one row per asset plus one portfolio summary row.
    
    Args:
        individual_metrics: List of dictionaries with individual asset metrics
        portfolio_metrics: Dictionary with portfolio metrics
        output_dir: Directory to save CSV file
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Create summary data list
    summary_data = []
    
    # Add individual asset metrics
    for metrics in individual_metrics:
        summary_data.append(metrics)
    
    # Add portfolio summary row
    portfolio_row = {
        'Ticker': 'PORTFOLIO',
        'Cumulative Return (%)': portfolio_metrics['Portfolio Cumulative Return (%)'],
        'Annualized Return (%)': portfolio_metrics['Portfolio Annualized Return (%)'],
        'Annualized Volatility (%)': portfolio_metrics['Portfolio Annualized Volatility (%)'],
        'Sharpe Ratio': portfolio_metrics['Portfolio Sharpe Ratio'],
        'Maximum Drawdown (%)': portfolio_metrics['Portfolio Maximum Drawdown (%)'],
        'Trading Days': individual_metrics[0]['Trading Days'] if individual_metrics else 0
    }
    summary_data.append(portfolio_row)
    
    # Convert to DataFrame and save
    df_summary = pd.DataFrame(summary_data)
    csv_path = os.path.join(output_dir, 'portfolio_summary.csv')
    df_summary.to_csv(csv_path, index=False)
    print(f"💾 Summary saved to: {csv_path}")


def print_results_table(individual_metrics, portfolio_metrics):
    """
    Print formatted results table to console.
    
    Displays individual asset performance and portfolio summary in a clean,
    readable table format.
    
    Args:
        individual_metrics: List of dictionaries with individual asset metrics
        portfolio_metrics: Dictionary with portfolio metrics
    """
    print("\n" + "="*80)
    print("📈 PORTFOLIO ANALYSIS RESULTS")
    print("="*80)
    
    # Individual asset metrics table
    if individual_metrics:
        print("\n📊 Individual Asset Performance:")
        print("-" * 80)
        table_data = []
        for metrics in individual_metrics:
            table_data.append([
                metrics['Ticker'],
                f"{metrics['Cumulative Return (%)']:.2f}%",
                f"{metrics['Annualized Return (%)']:.2f}%",
                f"{metrics['Annualized Volatility (%)']:.2f}%",
                f"{metrics['Sharpe Ratio']:.3f}",
                f"{metrics['Maximum Drawdown (%)']:.2f}%"
            ])
        
        headers = [
            'Ticker', 
            'Cumulative Return', 
            'Annualized Return', 
            'Annualized Volatility', 
            'Sharpe Ratio',
            'Max Drawdown'
        ]
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
    
    # Portfolio metrics
    print("\n🎯 Portfolio Summary:")
    print("-" * 80)
    print(f"  Cumulative Return:     {portfolio_metrics['Portfolio Cumulative Return (%)']:.2f}%")
    print(f"  Annualized Return:     {portfolio_metrics['Portfolio Annualized Return (%)']:.2f}%")
    print(f"  Annualized Volatility: {portfolio_metrics['Portfolio Annualized Volatility (%)']:.2f}%")
    print(f"  Sharpe Ratio:          {portfolio_metrics['Portfolio Sharpe Ratio']:.3f}")
    print(f"  Maximum Drawdown:      {portfolio_metrics['Portfolio Maximum Drawdown (%)']:.2f}%")
    
    # Portfolio weights
    print("\n⚖️  Portfolio Weights:")
    print("-" * 80)
    for ticker, weight in portfolio_metrics['Weights'].items():
        print(f"  {ticker}: {weight*100:.1f}%")
    
    print("\n" + "="*80)


def main():
    """
    Main function that orchestrates the entire portfolio analysis workflow.
    
    Workflow:
    1. Parse and validate command-line arguments
    2. Download historical stock data
    3. Calculate returns
    4. Calculate individual asset metrics
    5. Calculate portfolio metrics
    6. Print results to console
    7. Save results to CSV
    8. Generate visualizations
    """
    try:
        # Parse command-line arguments
        args = parse_arguments()
        
        # Print configuration
        print_configuration(args)
        
        # Step 1: Download stock data
        prices = download_stock_data(
            tickers=args.tickers,
            start_date=args.start_date,
            end_date=args.end_date,
            period=args.period
        )
        
        # Step 2: Calculate daily returns
        returns = calculate_returns(prices)
        
        # Step 3: Calculate individual asset metrics
        individual_metrics = []
        for ticker in prices.columns:
            metrics = calculate_asset_metrics(
                returns[ticker], 
                ticker, 
                risk_free_rate=args.risk_free_rate
            )
            if metrics:
                individual_metrics.append(metrics)
        
        # Step 4: Calculate portfolio metrics
        portfolio_returns = calculate_portfolio_returns(returns, args.weights)
        portfolio_metrics = calculate_portfolio_metrics(
            returns, 
            weights=args.weights,
            risk_free_rate=args.risk_free_rate
        )
        
        # Step 5: Print results to console
        print_results_table(individual_metrics, portfolio_metrics)
        
        # Step 6: Save results to CSV
        save_results_to_csv(individual_metrics, portfolio_metrics, args.output_dir)
        
        # Step 7: Create visualizations
        create_visualizations(
            prices, 
            returns, 
            portfolio_returns, 
            output_dir=args.output_dir
        )
        
        print("\n✅ Analysis complete!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nTroubleshooting tips:")
        print("  - Check that ticker symbols are correct")
        print("  - Verify internet connection")
        print("  - Ensure date ranges are valid (if specified)")
        print("  - Check that all required packages are installed")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

