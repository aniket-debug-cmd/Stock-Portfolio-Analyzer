# Stock Portfolio Analyzer

A professional Python tool for analyzing stock portfolios with historical data, calculating comprehensive performance metrics, and generating publication-ready visualizations.

## 🎯 Project Overview

This project provides a complete portfolio analysis solution that:
- Downloads historical stock data from Yahoo Finance
- Calculates key performance metrics (returns, volatility, Sharpe ratio, maximum drawdown)
- Supports custom portfolio weights or equal-weight allocation
- Generates professional visualizations and CSV reports
- Includes comprehensive unit tests and error handling

## 🛠️ Technologies Used

- **Python 3.7+** - Core programming language
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computations
- **yfinance** - Stock data API (Yahoo Finance)
- **matplotlib** - Data visualization
- **tabulate** - Formatted console output
- **unittest** - Unit testing framework

## 📁 Project Structure

```
Stock-Portfolio-Analyzer/
├── portfolio_analyzer/          # Main package
│   ├── __init__.py              # Package initialization
│   ├── data_loader.py           # Stock data downloading
│   ├── metrics.py               # Individual asset metrics
│   ├── portfolio.py             # Portfolio calculations
│   ├── visualization.py         # Chart generation
│   └── cli.py                   # CLI argument parsing
├── tests/                       # Unit tests
│   ├── __init__.py
│   ├── test_metrics.py          # Metrics calculation tests
│   ├── test_portfolio.py        # Portfolio calculation tests
│   └── test_cli.py              # CLI validation tests
├── main.py                      # Entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── .gitignore                   # Git ignore rules
```

## 🚀 Setup Instructions

### Step 1: Prerequisites

Ensure you have Python 3.7 or higher installed:
```bash
python --version
```

### Step 2: Navigate to Project Directory

```bash
cd C:\Users\aniik\Stock-Portfolio-Analyzer
```

### Step 3: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
```

**Mac/Linux:**
```bash
python3 -m venv venv
```

### Step 4: Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the beginning of your command prompt.

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `pandas>=2.0.0` - Data manipulation
- `numpy>=1.24.0` - Numerical calculations
- `yfinance>=0.2.28` - Stock data API
- `matplotlib>=3.7.0` - Visualization
- `tabulate>=0.9.0` - Formatted tables

### Step 6: Verify Installation

Run a quick test to ensure everything works:
```bash
python main.py --tickers AAPL --period 1mo
```

## 📖 Usage

### Basic Examples

**Equal-weight portfolio (3 stocks):**
```bash
python main.py --tickers AAPL MSFT TSLA
```

**Custom weights:**
```bash
python main.py --tickers AAPL MSFT TSLA --weights 0.4 0.3 0.3
```

**Custom date range:**
```bash
python main.py --tickers GOOGL AMZN --start-date 2023-01-01 --end-date 2023-12-31
```

**Custom risk-free rate:**
```bash
python main.py --tickers AAPL MSFT --risk-free-rate 0.04
```

**Custom output directory:**
```bash
python main.py --tickers AAPL MSFT --output-dir results
```

### Complete Example with All Options

```bash
python main.py --tickers AAPL MSFT GOOGL --weights 0.5 0.3 0.2 --start-date 2023-01-01 --end-date 2023-12-31 --risk-free-rate 0.035 --output-dir my_results
```

### Command-Line Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--tickers` | Yes | - | List of stock ticker symbols (e.g., AAPL MSFT TSLA) |
| `--weights` | No | Equal-weight | Portfolio weights (must match number of tickers) |
| `--start-date` | No | - | Start date (YYYY-MM-DD). Must use with --end-date |
| `--end-date` | No | Today | End date (YYYY-MM-DD). Must use with --start-date |
| `--period` | No | 1y | Time period if dates not specified (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max) |
| `--risk-free-rate` | No | 0.03 | Risk-free rate for Sharpe ratio (0.03 = 3%) |
| `--output-dir` | No | outputs | Directory to save output files |

## 📊 Output Files

After running the analysis, the following files are generated in the output directory:

### 1. `portfolio_summary.csv`

A CSV file containing:
- One row per individual asset with metrics:
  - Cumulative Return (%)
  - Annualized Return (%)
  - Annualized Volatility (%)
  - Sharpe Ratio
  - Maximum Drawdown (%)
  - Trading Days
- One portfolio summary row with aggregated metrics

### 2. `portfolio_analysis.png`

A high-resolution chart (300 DPI) showing:
- **Portfolio Value Over Time**: Normalized portfolio performance
- **Individual Asset Performance**: Normalized price movements for each asset
- **Rolling 30-Day Volatility**: Risk metrics over time for portfolio and individual assets

## 📈 Understanding the Metrics

### Cumulative Return
Total return over the analysis period. Example: 15% means your $100 investment became $115.

### Annualized Return
Return projected to a full year. Useful for comparing investments over different time periods.

### Annualized Volatility
Risk measure showing how much prices fluctuate. Higher volatility = more risk. Calculated as standard deviation of returns × √252.

### Sharpe Ratio
Risk-adjusted return metric. Formula: (Annualized Return - Risk-Free Rate) / Annualized Volatility
- **> 1**: Good
- **> 2**: Very good
- **> 3**: Excellent

### Maximum Drawdown
Largest peak-to-trough decline. Shows the worst loss from a peak. Negative value (e.g., -25% means a 25% decline from peak).

## 🧪 Running Tests

The project includes comprehensive unit tests. Run them with:

```bash
python -m pytest tests/
```

Or using unittest:

```bash
python -m unittest discover tests
```

### Test Coverage

- **test_metrics.py**: Tests Sharpe ratio, returns, volatility, and drawdown calculations
- **test_portfolio.py**: Tests portfolio return calculation and weight validation
- **test_cli.py**: Tests CLI argument validation

### Example Test Output

```
...
----------------------------------------------------------------------
Ran 15 tests in 0.123s

OK
```

## ⚠️ Common Errors and Fixes

### Error: "No module named 'yfinance'"

**Solution**: Activate virtual environment and install dependencies:
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Error: "No data found" for a ticker

**Possible causes:**
- Incorrect ticker symbol (use "GOOGL" not "GOOGLE")
- Ticker doesn't exist or is delisted
- Date range has no trading days

**Solution**: 
- Verify ticker symbols on Yahoo Finance
- Try a different date range
- Check that dates include trading days (not weekends/holidays)

### Error: "Number of weights must match number of tickers"

**Solution**: Provide the same number of weights as tickers:
```bash
# Correct:
python main.py --tickers AAPL MSFT --weights 0.6 0.4

# Wrong:
python main.py --tickers AAPL MSFT --weights 0.6
```

### Error: "Start date must be before end date"

**Solution**: Ensure start date is earlier than end date:
```bash
# Correct:
python main.py --tickers AAPL --start-date 2023-01-01 --end-date 2023-12-31

# Wrong:
python main.py --tickers AAPL --start-date 2023-12-31 --end-date 2023-01-01
```

### Error: "Weights cannot be negative"

**Solution**: All weights must be non-negative (≥ 0):
```bash
# Correct:
python main.py --tickers AAPL MSFT --weights 0.6 0.4

# Wrong:
python main.py --tickers AAPL MSFT --weights 0.6 -0.4
```

### Chart/CSV Not Generated

**Solution**: 
- Check that output directory is writable
- Ensure matplotlib backend is working: `python -c "import matplotlib; matplotlib.use('Agg')"`
- Look for error messages in console output

## 🔧 Development

### Code Structure

The project follows a modular architecture:

- **data_loader.py**: Handles all data fetching from Yahoo Finance
- **metrics.py**: Pure functions for calculating individual asset metrics
- **portfolio.py**: Portfolio-level calculations and weight management
- **visualization.py**: Chart generation and formatting
- **cli.py**: Argument parsing and validation
- **main.py**: Orchestrates the workflow

### Adding New Features

1. **New Metrics**: Add functions to `metrics.py`
2. **New Charts**: Extend `visualization.py`
3. **New CLI Options**: Update `cli.py` and `main.py`

### Code Style

- Follow PEP 8 style guide
- Use descriptive variable names
- Include docstrings for all functions
- Add inline comments for complex logic

## 📝 GitHub Setup

### Initial Commit

```bash
git init
git add .
git commit -m "Initial commit: Stock Portfolio Analyzer with modular architecture"
```

### Recommended Commit Messages

```bash
git commit -m "Add maximum drawdown calculation to metrics module"
git commit -m "Implement rolling volatility visualization"
git commit -m "Add comprehensive unit tests for portfolio calculations"
git commit -m "Enhance CLI with date range and risk-free rate options"
git commit -m "Update README with professional documentation"
```

### What to Include in Repository

**Include:**
- All source code (`portfolio_analyzer/`, `main.py`)
- Test files (`tests/`)
- Configuration files (`requirements.txt`, `.gitignore`, `README.md`)
- Sample output screenshots (optional but recommended)

**Exclude (handled by .gitignore):**
- Virtual environment (`venv/`)
- Output files (`outputs/`, `*.csv`, `*.png`)
- Python cache (`__pycache__/`)
- IDE files (`.vscode/`, `.idea/`)

### Screenshots to Include

Consider adding to your repository:
1. Console output showing analysis results
2. Sample chart (`portfolio_analysis.png`)
3. Sample CSV output (first few rows)

## 🎓 Resume Bullets

Here are three strong, accurate resume bullets that match the final features:

1. **"Developed a modular Python portfolio analysis tool with 6 specialized modules (data loading, metrics calculation, portfolio optimization, visualization) that downloads historical stock data via yfinance API, calculates risk-adjusted performance metrics including Sharpe ratio and maximum drawdown, and generates automated CSV reports and publication-ready visualizations with rolling volatility charts."**

2. **"Built a professional command-line financial analysis application with comprehensive input validation, custom date range support, configurable risk-free rates, and weighted portfolio allocation logic, implementing unit tests with 15+ test cases covering metrics calculations, portfolio returns, and weight validation using Python's unittest framework."**

3. **"Created an internship-ready portfolio analyzer following software engineering best practices including modular architecture, PEP 8 compliance, comprehensive error handling, and professional documentation, processing multiple stock tickers with equal-weight or custom allocation strategies to compute annualized returns, volatility, and risk metrics for portfolio optimization."**

## 📄 License

This project is for educational and portfolio purposes.

## 👤 Author

Your Name - [Your GitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Yahoo Finance for providing free stock data via yfinance
- Python open-source community for excellent libraries

---

**Note**: This tool is for educational purposes only. Always consult with a financial advisor before making investment decisions.

