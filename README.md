# Personal_Finance
Tool for calculating and forcasting personal investments and liabilities.

# Overview

## Holdings Classes

**Bank Account:**
- Fixed interest rate, compounded monthly
- Allows for monthly deposits and withdrawals 

**Common Stock:**
- Allows for both capital appreciation and dividend earnings
- Volatility can be set to low, medium, or high
- Allows for DRIP (Dividend Reinvestment Plan).  Dividends payed out quarterly.  If DRIP is in place, remaining funds will be transferred to a cash account.  If no DRIP is in place, all dividend fund transfer to cash account.
- Allows for annual deposits and withdrawals (with commission)
- Allows for monthly deposits and withdrawals (with commission)

**GIC (guaranteed investment certificate):**
- Balance is compounded annually
- Funds can be reinvested at the end of the maturity period
- Funds only available at the end of the maturity period.  If the funds are reinvested, they are not availabe until the next maturity.


## Other Features

**Plotting (utils):**
- Plot value of a single asset

**Collective Compound:**
- Allows for multiple assets (currently bank accounts, stocks, and GICs) to be compounded at the same time and combined to a collective portfolio value.

**Future:** Bonds, Real Estate, House Mortgages, Car Loans, Student Loans, Tax Rate (based on alberta tax laws), Taxed and Untaxed Income
