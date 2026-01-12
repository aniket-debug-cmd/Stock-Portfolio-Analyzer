# Stock Portfolio Analyzer

Hey! This is a Python project I built for analyzing stock portfolios. I'm currently a 3rd year Computer Science student at San Francisco State University (SFSU), and I'm originally from India. I created this tool to help me understand portfolio analysis better and to practice my Python skills.

## About This Project

I built this portfolio analyzer because I wanted to learn more about financial data analysis and portfolio management. It downloads real stock data, calculates important metrics like returns and risk, and creates nice visualizations. It's been really helpful for my learning!

The project uses Python with libraries like pandas and yfinance to download stock data from Yahoo Finance. I've structured it in a modular way so it's easy to understand and extend.

## Technologies I Used

- **Python 3.7+** - Main language
- **pandas** - For working with data
- **numpy** - For calculations
- **yfinance** - To get stock data from Yahoo Finance (it's free!)
- **matplotlib** - For making charts
- **tabulate** - To print nice tables in the console
- **unittest** - For testing (I learned this is really important!)

## Project Structure

Here's how I organized the code:

```
Stock-Portfolio-Analyzer/
├── portfolio_analyzer/          # Main package folder
│   ├── __init__.py              
│   ├── data_loader.py           # Downloads stock data
│   ├── metrics.py               # Calculates metrics for individual stocks
│   ├── portfolio.py             # Portfolio-level calculations
│   ├── visualization.py         # Creates charts
│   └── cli.py                   # Handles command line arguments
├── tests/                       # My test files
│   ├── __init__.py
│   ├── test_metrics.py          
│   ├── test_portfolio.py        
│   └── test_cli.py              
├── main.py                      # Main script to run
├── requirements.txt             # Python packages needed
├── README.md                    # This file
└── .gitignore                   # Files to ignore in git
```

## How to Set Up

I'll walk you through the setup step by step:

### Step 1: Check Python Version

Make sure you have Python 3.7 or higher:
```bash
python --version
```

### Step 2: Go to Project Folder

```bash
cd C:\Users\aniik\Stock-Portfolio-Analyzer
```
(Or wherever you saved the project)

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

You should see `(venv)` at the start of your command prompt.

### Step 5: Install Required Packages

```bash
pip install -r requirements.txt
```

This will install:
- `pandas` - For data manipulation
- `numpy` - For math calculations
- `yfinance` - To download stock data
- `matplotlib` - For charts
- `tabulate` - For nice table output

### Step 6: Test It Works

Try running it with one stock:
```bash
python main.py --tickers AAPL --period 1mo
```

If it works, you should see output and files created in the `outputs/` folder!

## How to Use

### Basic Examples

**Analyze 3 stocks with equal weights:**
```bash
python main.py --tickers AAPL MSFT TSLA
```

**Use custom weights (must add up to 1):**
```bash
python main.py --tickers AAPL MSFT TSLA --weights 0.4 0.3 0.3
```

**Use a specific date range:**
```bash
python main.py --tickers GOOGL AMZN --start-date 2023-01-01 --end-date 2023-12-31
```

**Change the risk-free rate (default is 3%):**
```bash
python main.py --tickers AAPL MSFT --risk-free-rate 0.04
```

**Save outputs to a different folder:**
```bash
python main.py --tickers AAPL MSFT --output-dir my_results
```

### All Options Together

```bash
python main.py --tickers AAPL MSFT GOOGL --weights 0.5 0.3 0.2 --start-date 2023-01-01 --end-date 2023-12-31 --risk-free-rate 0.035 --output-dir my_results
```

### Command-Line Arguments Explained

| Argument | Required? | Default | What It Does |
|----------|-----------|---------|--------------|
| `--tickers` | Yes | - | List of stock symbols (like AAPL MSFT TSLA) |
| `--weights` | No | Equal weights | How much of each stock (will normalize to sum to 1) |
| `--start-date` | No | - | Start date (YYYY-MM-DD). Must use with --end-date |
| `--end-date` | No | Today | End date (YYYY-MM-DD). Must use with --start-date |
| `--period` | No | 1y | Time period if dates not specified (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max) |
| `--risk-free-rate` | No | 0.03 | Risk-free rate for Sharpe ratio (0.03 = 3%) |
| `--output-dir` | No | outputs | Where to save CSV and chart files |

## What Gets Created

After you run the analysis, you'll find these files in the output folder:

### 1. `portfolio_summary.csv`

A CSV file with:
- One row for each stock showing:
  - Cumulative Return (%)
  - Annualized Return (%)
  - Annualized Volatility (%)
  - Sharpe Ratio
  - Maximum Drawdown (%)
  - Trading Days
- One row for the portfolio summary

### 2. `portfolio_analysis.png`

A chart showing:
- **Portfolio Value Over Time**: How your portfolio performed (normalized to $1)
- **Individual Stock Performance**: How each stock did (also normalized)
- **Rolling 30-Day Volatility**: How risky things were over time

## Understanding the Metrics

I learned about these metrics in my finance classes, so let me explain:

### Cumulative Return
Total return over the whole period. If it says 15%, that means $100 became $115.

### Annualized Return
What the return would be if projected to a full year. Useful for comparing different time periods.

### Annualized Volatility
How much prices go up and down (risk measure). Higher = more risk. Calculated as standard deviation × √252 (trading days per year).

### Sharpe Ratio
Risk-adjusted return. Formula: (Annualized Return - Risk-Free Rate) / Annualized Volatility
- **> 1**: Pretty good
- **> 2**: Very good
- **> 3**: Excellent

### Maximum Drawdown
The worst loss from a peak. If it says -25%, that means at some point you lost 25% from the highest point.

## Running Tests

I wrote some tests to make sure everything works correctly. Run them with:

```bash
python -m unittest discover tests
```

Or using pytest if you have it:
```bash
python -m pytest tests/
```

### What the Tests Cover

- **test_metrics.py**: Tests calculations like Sharpe ratio, returns, volatility, drawdown
- **test_portfolio.py**: Tests portfolio calculations and weight validation
- **test_cli.py**: Tests that command-line arguments are validated correctly

All 21 tests should pass! If they don't, let me know and I can help fix it.

## Common Problems and Solutions

### "No module named 'yfinance'"

**Fix**: Make sure you activated the virtual environment and installed packages:
```bash
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### "No data found" for a ticker

**Possible reasons:**
- Wrong ticker symbol (use "GOOGL" not "GOOGLE")
- Stock doesn't exist or was delisted
- Date range has no trading days

**Fix**: 
- Check ticker on Yahoo Finance
- Try different dates
- Make sure dates include trading days (not weekends)

### "Number of weights must match number of tickers"

**Fix**: Give same number of weights as tickers:
```bash
# Right:
python main.py --tickers AAPL MSFT --weights 0.6 0.4

# Wrong:
python main.py --tickers AAPL MSFT --weights 0.6
```

### "Start date must be before end date"

**Fix**: Start date should be earlier:
```bash
# Right:
python main.py --tickers AAPL --start-date 2023-01-01 --end-date 2023-12-31

# Wrong:
python main.py --tickers AAPL --start-date 2023-12-31 --end-date 2023-01-01
```

### "Weights cannot be negative"

**Fix**: All weights must be 0 or positive:
```bash
# Right:
python main.py --tickers AAPL MSFT --weights 0.6 0.4

# Wrong:
python main.py --tickers AAPL MSFT --weights 0.6 -0.4
```

### Chart or CSV Not Created

**Fix**: 
- Check you have write permission in the folder
- Look for error messages in the console
- Make sure matplotlib is working: `python -c "import matplotlib; print('OK')"`

## How I Built This

I organized the code into modules to keep things clean:

- **data_loader.py**: Gets stock data from Yahoo Finance
- **metrics.py**: Calculates metrics for individual stocks
- **portfolio.py**: Does portfolio-level calculations and handles weights
- **visualization.py**: Makes the charts
- **cli.py**: Handles command-line arguments and validation
- **main.py**: Ties everything together

If you want to add features:
- New metrics? Add functions to `metrics.py`
- New charts? Extend `visualization.py`
- New CLI options? Update `cli.py` and `main.py`

## GitHub Setup

I've already set this up on GitHub. Here's what I did:

### Initial Commit

```bash
git init
git add .
git commit -m "Initial commit: Professional Stock Portfolio Analyzer with modular architecture"
```

### Good Commit Messages

When I make changes, I use messages like:
```bash
git commit -m "Add maximum drawdown calculation"
git commit -m "Fix Windows encoding issue for emojis"
git commit -m "Add more unit tests for portfolio calculations"
```

### What's in the Repo

**Included:**
- All source code
- Test files
- requirements.txt, README.md, .gitignore

**Excluded (in .gitignore):**
- Virtual environment folder (`venv/`)
- Output files (`outputs/`, `*.csv`, `*.png`)
- Python cache (`__pycache__/`)
- IDE files

## About Me

I'm a Computer Science student at San Francisco State University, currently in my 3rd year. I'm originally from India and I'm passionate about programming and data analysis. This project helped me learn a lot about:
- Working with financial APIs
- Data analysis with pandas
- Creating visualizations
- Writing clean, modular code
- Unit testing

I'm always learning and improving, so if you have suggestions or find bugs, feel free to let me know!

## Acknowledgments

- Yahoo Finance for providing free stock data through yfinance
- The Python community for amazing libraries
- My professors at SFSU for teaching me about software engineering best practices

## Note

This tool is for educational purposes only. I built it to learn about portfolio analysis. Always do your own research and consult with financial advisors before making investment decisions!

---

**Thanks for checking out my project!** 🙏

If you find it useful or have questions, feel free to reach out!
