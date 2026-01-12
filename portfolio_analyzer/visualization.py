"""
Visualization Module

Creates charts and visualizations for portfolio analysis including:
- Portfolio value over time
- Individual asset performance
- Rolling volatility
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def create_visualizations(prices, returns, portfolio_returns, output_dir="outputs", 
                         show_rolling_volatility=True):
    """
    Create comprehensive visualization charts for portfolio analysis.
    
    Generates multiple charts showing portfolio performance, individual asset
    performance, and risk metrics over time.
    
    Args:
        prices: DataFrame with stock prices (dates as index, tickers as columns)
        returns: DataFrame with daily returns
        portfolio_returns: Series with portfolio daily returns
        output_dir: Directory to save charts (default: "outputs")
        show_rolling_volatility: Whether to include rolling volatility chart (default: True)
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Determine number of subplots based on whether we show rolling volatility
    num_plots = 3 if show_rolling_volatility else 2
    fig, axes = plt.subplots(num_plots, 1, figsize=(14, 5 * num_plots))
    
    # If only one subplot, make axes a list for consistent indexing
    if num_plots == 1:
        axes = [axes]
    
    # Chart 1: Portfolio Value Over Time (Normalized)
    ax1 = axes[0]
    portfolio_value = (1 + portfolio_returns).cumprod()
    ax1.plot(portfolio_value.index, portfolio_value.values, 
             linewidth=2.5, label='Portfolio', color='#2E86AB', alpha=0.9)
    ax1.set_title('Portfolio Value Over Time (Normalized to $1)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax1.set_xlabel('Date', fontsize=12)
    ax1.set_ylabel('Portfolio Value', fontsize=12)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.legend(loc='best', fontsize=11)
    ax1.tick_params(axis='x', rotation=45)
    
    # Format x-axis dates nicely
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    
    # Chart 2: Individual Asset Performance (Normalized)
    ax2 = axes[1]
    normalized_prices = prices / prices.iloc[0]  # Normalize to starting value of $1
    
    # Use distinct colors for each asset
    colors = ['#A23B72', '#F18F01', '#C73E1D', '#6A994E', '#BC4749', '#219EBC']
    
    for idx, col in enumerate(normalized_prices.columns):
        color = colors[idx % len(colors)]
        ax2.plot(normalized_prices.index, normalized_prices[col].values, 
                label=col, alpha=0.8, linewidth=2, color=color)
    
    ax2.set_title('Individual Asset Performance (Normalized to $1)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax2.set_xlabel('Date', fontsize=12)
    ax2.set_ylabel('Normalized Price', fontsize=12)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.legend(loc='best', fontsize=11, ncol=2)
    ax2.tick_params(axis='x', rotation=45)
    
    # Format x-axis dates
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    
    # Chart 3: Rolling Volatility (Optional)
    if show_rolling_volatility:
        ax3 = axes[2]
        
        # Calculate rolling volatility for portfolio
        from .metrics import calculate_rolling_volatility
        portfolio_rolling_vol = calculate_rolling_volatility(portfolio_returns, window=30)
        
        ax3.plot(portfolio_rolling_vol.index, portfolio_rolling_vol.values * 100,
                linewidth=2, label='Portfolio (30-day)', color='#2E86AB', alpha=0.9)
        
        # Also show individual assets' rolling volatility
        for idx, col in enumerate(returns.columns):
            asset_rolling_vol = calculate_rolling_volatility(returns[col], window=30)
            color = colors[idx % len(colors)]
            ax3.plot(asset_rolling_vol.index, asset_rolling_vol.values * 100,
                    label=f'{col} (30-day)', alpha=0.6, linewidth=1.5, color=color, linestyle='--')
        
        ax3.set_title('Rolling 30-Day Annualized Volatility', 
                      fontsize=14, fontweight='bold', pad=15)
        ax3.set_xlabel('Date', fontsize=12)
        ax3.set_ylabel('Volatility (%)', fontsize=12)
        ax3.grid(True, alpha=0.3, linestyle='--')
        ax3.legend(loc='best', fontsize=10, ncol=2)
        ax3.tick_params(axis='x', rotation=45)
        
        # Format x-axis dates
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax3.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    
    # Adjust layout to prevent overlap
    plt.tight_layout()
    
    # Save chart
    chart_path = os.path.join(output_dir, 'portfolio_analysis.png')
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    print(f"📊 Chart saved to: {chart_path}")
    
    # Close figure to free memory
    plt.close()

