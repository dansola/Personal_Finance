import numpy as np
import random


# bank account
class BankAccount:
    """
    balance: amount of money in the account
    interest_rate: annual interest rate compounded monthly
    name: name of the account
    """

    def __init__(self, balance, interest_rate, name='this account'):
        self.balance = balance
        self.interest_rate = interest_rate
        self.name = name
        self.broke = False
        self.broke_time = 0

    # project monthly balance of the bank account and return a list of values for a certain time into the future
    def compound(self, years=0, months=0, monthly_deposit=0, monthly_withdrawal=0):
        values = []
        total_months = int((years * 12) + months)
        monthly_interest = self.interest_rate / 1200

        # compound interest every month and deposit or withdrawal monthly
        for m in range(total_months + 1):
            values.append(self.balance)
            self.balance *= (1 + monthly_interest)
            self.balance += monthly_deposit
            self.balance -= monthly_withdrawal

            # recognize if account has run dry due to excessive withdrawal
            if self.balance <= 0 and self.broke_time == 0:
                self.broke = True
                self.broke_time = m

        return np.array(values)

    def summary(self):

        print(f'The total value of {self.name} is ${self.balance:.2f}.')
        if self.broke:
            print(f'You will go broke in {(self.broke_time / 12):.2f} years.')


# brokerage account can contain multiple Stocks, GICs, or Bonds
class Account:
    def __init__(self, cash=0, fee=0, tax_free=True):
        self.cash = cash
        self.fee = fee  # TODO: incorporate tax ?? in what situatios are shareholders automatially taxed? ex. withholdingn tax
        self.tax_free = tax_free
        self.stock = self.createStock()
        self.fee_applied = False

    def createStock(self):
        return Account.Stock(self)

    def createGic(self):
        return Account.Gic(self)

    # GIC
    class Gic:
        """
        balance: amount of money in the GIC
        interest_rate: annual interest rate compounded annually
        maturity: number of years for the GIC to mature (i.e. the funds are available)
        is_reinvest: weather or not the funds are reinvested once the GIC matures
        name: name of the GIC
        availability: weather or not the funds are available to the owner
        note: fees do not apply to GICs
        """

        def __init__(self, balance, interest_rate, maturity, is_reinvest=True, name='this GIC', availability='are not'):
            self.balance = balance
            self.interest_rate = interest_rate
            self.maturity = maturity
            self.is_reinvest = is_reinvest
            self.name = name
            self.availability = availability

        # project monthly balance of the GIC and return a list of values for a certain time into the future
        def compound(self, years=0, months=0):
            values = []
            total_months = int((years * 12) + months)
            month = 0
            compounding_years = np.floor(total_months / 12)

            # raise error if the compounding period is less than a year since funds cannot compound
            if total_months < 12:
                raise Exception(f'{self.name} will not compound since {months} months is less than a year.')

            else:
                if self.is_reinvest:
                    # check if funds are available by seeing if the compounding time is a factor of the maturity
                    if ((total_months / 12) / self.maturity).is_integer():
                        self.availability = 'are'

                    # compound interest annually but store balance monthly
                    for m in range(int(compounding_years * 12)):
                        values.append(self.balance)
                        if month == 11:
                            self.balance *= (1 + self.interest_rate / 100)
                            month = -1
                        month += 1
                    # balance is stored for the remaining months
                    for i in range(total_months - m):
                        values.append(self.balance)
                else:
                    # check if funds are available. since funds are not reinvested, they are available after maturity
                    if total_months >= self.maturity * 12:
                        self.availability = 'are'
                    # compound interest annually but store balance monthly
                    year = 0
                    for m in range(int(total_months) + 1):
                        # only compound before maturity
                        if year < self.maturity:
                            values.append(self.balance)
                            if month == 11:
                                self.balance *= (1 + self.interest_rate / 100)
                                month = -1
                                year += 1
                            month += 1
                        # constant balance is stored for remaining time
                        else:
                            values.append(self.balance)

            return np.array(values)

        def summary(self):
            print(f'The total value of {self.name} is ${self.balance:.2f}.')
            print(f'These funds {self.availability} available.')

    # stock
    class Stock:
        """
        account: specify the brokerage account
        shares: number of shares of stock (int)
        price: price of stock
        dividend: total money returned per share at the end of the year
        dividend_percent_growth: projected annual growth of the dividend
        annual_growth: projected annual growth of the stock price
        commission: price to buy or sell a stock
        drip: whether or not dividends are reinvested (note: dividends are reinvested according to the number of shares
              which can be purchased at the current share price. If quarterly dividend payments are less than the stock,
              no dividends can be reinvested.
        name: name of the stock
        """

        def __init__(self, account, shares=0, price=0, dividend=0, dividend_percent_growth=0, annual_growth=0,
                     commission=10, volatility='med', drip='True', name='this stock'):
            self.account = account
            self.shares = shares
            self.dividend = dividend
            self.dividend_percent_growth = dividend_percent_growth
            self.volatility = volatility
            self.price = price
            self.annual_growth = annual_growth
            self.commission = commission
            self.drip = drip
            self.name = name
            self.broke = False
            self.broke_time = 0

        # project monthly price of the stock as well as the value of the product of the number of shares and the stock
        # price

        def compound(self, years=0, months=0, monthly_deposit=0, monthly_withdrawal=0, annual_deposit=0,
                     annual_withdrawal=0):
            """
            years: years to compound into the future
            months: months to compound into the future
            monthly_deposit: amount added the the stock every month, remaining amount after maximum stocks are
                             purchased will go to cash account.
            monthly_withdrawal: amount taken every month. Withdrawal amount is first taken from the cash account, if
                                cash account is zero, remaining money will be taken from selling stock.  If all shares
                                are sold, an error will arise due to the user going broke in that stock.
            annual_deposit: amount added the the stock every year, remaining amount after maximum stocks are
                            purchased will go to cash account.
            annual_withdrawal: amount taken every year. Withdrawal amount is first taken from the cash account, if
                               cash account is zero, remaining money will be taken from selling stock.  If all shares
                               are sold, an error will arise due to the user going broke in that stock.
            """
            values = []
            prices = []
            cash_amount = []
            total_months = int((years * 12) + months)
            monthly_growth = self.annual_growth / 1200
            pay_div = 0
            month = 0
            original_cash = self.account.cash

            # determine amount of volatility
            if self.volatility == 'low':
                vol = 0.01
            elif self.volatility == 'med':
                vol = 0.02
            elif self.volatility == 'high':
                vol = 0.04

            # every month update the value stock price, holding price (aggregate stocks), and the amount of cash
            # produced by this stock.
            for m in range(total_months + 1):
                balance = self.shares * self.price
                new_cash = self.account.cash - original_cash
                cash_amount.append(new_cash)  # amount of cash produced by this stock.
                values.append(balance)  # holding price (aggregate stocks)
                prices.append(self.price)  # stock price

                # apply volatility
                self.price *= (1 + random.uniform(-vol, vol))

                # every 3 months produce dividend earnings
                if pay_div == 2:
                    div_earnings = (self.dividend / 4) * self.shares
                    if self.drip:
                        if div_earnings < self.price:
                            self.account.cash += div_earnings
                        else:
                            Account.ChangeShares.add(self, div_earnings, is_drip=True)

                    else:
                        self.account.cash += div_earnings

                    pay_div = -1

                # growth of the stock
                self.price *= (1 + monthly_growth)

                # apply monthly withdrawals or deposits
                if monthly_deposit != 0:
                    Account.ChangeShares.add(self, monthly_deposit)
                if monthly_withdrawal != 0:
                    Account.ChangeShares.subtract(self, monthly_withdrawal)

                # apply annual withdrawals or deposits as well as dividend growth
                if month == 12:
                    self.dividend *= (1 + (self.dividend_percent_growth / 100))
                    if self.account.fee >= 0 and not self.account.fee_applied:
                        self.account.cash -= self.account.fee
                    if annual_deposit != 0:
                        Account.ChangeShares.add(self, annual_deposit)
                    if annual_withdrawal != 0:
                        Account.ChangeShares.subtract(self, annual_withdrawal)
                        # print(self.account.cash)
                    month = 0

                # determine if shares are being sold to a point of negative number of shares, if so break the loop and
                # report error message.
                if self.shares <= 0 and self.broke_time == 0:
                    self.broke = True
                    self.broke_time = m
                    break

                pay_div += 1
                month += 1

            # return stock price, holding price (aggregate stocks), and the amount of cash produced by this stock if the
            # account never went broke.  Otherwise raise error.
            if not self.broke:
                return np.array(values), np.array(prices), np.array(cash_amount)
            else:
                raise Exception(f'You will go broke in {(self.broke_time / 12):.2f} years with {self.name}. \n '
                                f'Please reevaluate your strategy.')

        def summary(self):
            value = (self.shares * self.price) + self.account.cash

            print(f'The total value of {self.name} is ${value:.2f}.')
            print(f'You have {self.shares} shares at a price of ${self.price:.2f}.')
            print(f'You have ${self.account.cash:.2f} in cash.')
            if self.broke:
                print(f'You will go broke in {(self.broke_time / 12):.2f} years.')
            print('\n')

    class ChangeShares(Stock):
        """
        add: Buys shares commission free if buying is under a DRIP, contributes remaining amount to cash. Otherwise
             a commission is applied prior to new shares being purchased and remaining amount going to cash.

        subtract: If cash is present in the account, take money from the cash pool.  Remaining money will be
                  collected from selling shares.  If no cash is present, all money will be collected from selling shares
        """

        # add stocks or cash to the account depending on if a DRIP is in place.  If no DRIP is in place and the amount
        # added is less than commission, an error will be raised.
        def add(self, amount, is_drip=False):
            if not is_drip:
                if amount >= self.commission:
                    amount -= self.commission
                    new_shares = np.floor(amount / self.price)
                    self.shares += new_shares
                    self.account.cash += amount - (new_shares * self.price)
                else:
                    raise Exception(f'Amount depositing to {self.name} is less than the commission to buy a stock')
            else:
                new_shares = np.floor(amount / self.price)
                self.shares += new_shares
                self.account.cash += amount - (new_shares * self.price)

        # remove stocks or cash from the account. If the amount taken is less than commission, an error will be raised.
        def subtract(self, amount):
            if amount >= self.commission:
                amount -= self.commission
                if self.account.cash > 0:
                    if amount <= self.account.cash:
                        self.account.cash -= amount  # (this might be firing when it shouldn't)
                    else:
                        amount_left = amount - self.account.cash
                        self.account.cash = 0
                        sell_shares = np.floor(amount_left / self.price)
                        self.shares -= sell_shares
                else:
                    sell_shares = np.floor(amount / self.price)
                    self.shares -= sell_shares
            else:
                raise Exception(f'Amount withdrawing from {self.name} is less than the commission to buy a stock')


# general compound of all accounts, though monthy/annual withdrawals and deposits cannot apply
# arguments can be from the following classes: BankAccount, Gic, Stock
import matplotlib.pyplot as plt


def CollectiveCompound(years=0, months=0, plot=True, args=[]):
    vals = np.zeros((12 * years) + months +1)
    if plot:
        x = np.array([i for i in range(len(vals))])
        if len(vals) <= 24:
            x_lab = 'Months'
        else:
            x = x/12
            x_lab = 'Years'
    for a in args:
        if type(a) == Account.Stock:
            val = a.compound(years=years, months=months)[0]
        else:
            val = a.compound(years=years, months=months)
        vals += val
        if plot:
            plt.plot(x, val, label=a.name)
    if plot:
        plt.plot(x, vals, label='Collective')
        plt.legend()
        plt.xlabel(x_lab)
        plt.ylabel('Value ($)')
        plt.show()
    else:
        return vals



