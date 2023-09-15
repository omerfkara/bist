import yfinance as yf

msft = yf.Ticker("MSFT")

# get all stock info
msft.info

# get historical market data
hist = msft.history(period="1mo")

# show meta information about the history (requires history() to be called first)
msft.history_metadata

# show actions (dividends, splits, capital gains)
msft.actions
msft.dividends
msft.splits
msft.capital_gains  # only for mutual funds & etfs

# show share count
msft.get_shares_full(start="2023-09-10", end=None)

# show financials:
# - income statement
print(msft.income_stmt)
print(msft.quarterly_income_stmt)
# - balance sheet
print(msft.balance_sheet)
print(msft.quarterly_balance_sheet)
# - cash flow statement
print(msft.cashflow)
print(msft.quarterly_cashflow)
# see `Ticker.get_income_stmt()` for more options

# show holders
print(msft.major_holders)
print(msft.institutional_holders)
print(msft.mutualfund_holders)

# Show future and historic earnings dates, returns at most next 4 quarters and last 8 quarters by default. 
# Note: If more are needed use msft.get_earnings_dates(limit=XX) with increased limit argument.
msft.earnings_dates

# show ISIN code - *experimental*
# ISIN = International Securities Identification Number
msft.isin

# show options expirations
msft.options

# show news
msft.news

# get option chain for specific expiration
#opt = msft.option_chain('YYYY-MM-DD')
# data available via: opt.calls, opt.puts