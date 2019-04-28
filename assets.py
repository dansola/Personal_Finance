import numpy as np
import random


class BankAccount:
    def __init__(self, balance, interest_rate, name='this account'):
        self.balance = balance
        self.interest_rate = interest_rate
        self.name = name
        self.broke = False
        self.broke_time = 0

    def compound(self, years=0, months=0, monthly_deposit=0, monthly_withdrawal=0):
        values = []
        total_months = int((years * 12) + months)
        monthly_interest = self.interest_rate / 1200

        for m in range(total_months + 1):
            values.append(self.balance)
            self.balance *= (1 + monthly_interest)
            self.balance += monthly_deposit
            self.balance -= monthly_withdrawal

            if self.balance <= 0 and self.broke_time == 0:
                self.broke = True
                self.broke_time = m

        return values

    def summary(self):

        print(f'The total value of {self.name} is ${self.balance:.2f}')
        if self.broke:
            print(f'You will go broke in {(self.broke_time / 12):.2f} years.')


class Stock:
    def __init__(self, shares, price, dividend, annual_growth, commission=10, cash=0, volatility='med', drip='True',
                 name='this stock'):
        self.shares = shares
        self.dividend = dividend
        self.volatility = volatility
        self.price = price
        self.annual_growth = annual_growth
        self.commission = commission
        self.drip = drip
        self.cash = cash
        self.name = name
        self.broke = False
        self.broke_time = 0

    def compound(self, years=0, months=0, monthly_deposit=0, monthly_withdrawal=0, annual_deposit=0,
                 annual_withdrawal=0):
        values = []
        prices = []
        total_months = int((years * 12) + months)
        monthly_growth = self.annual_growth / 1200
        quarterly_dividend = self.dividend / 400
        pay_div = 0
        month = 0
        if self.volatility == 'low':
            vol = 0.01
        elif self.volatility == 'med':
            vol = 0.03
        elif self.volatility == 'high':
            vol = 0.05

        for m in range(total_months + 1):
            balance = self.shares * self.price

            values.append(balance + self.cash)
            prices.append(self.price)

            self.price *= (1 + random.uniform(-vol, vol))
            if pay_div == 2:
                div_earnings = self.price * quarterly_dividend * self.shares
                if self.drip:
                    if div_earnings < self.price:
                        self.cash += div_earnings
                    else:
                        ChangeShares.add(self, div_earnings, is_drip=True)

                else:
                    self.cash += div_earnings

                pay_div = -1

            self.price *= (1 + monthly_growth)

            if monthly_deposit != 0:
                ChangeShares.add(self, monthly_deposit)
            if monthly_withdrawal != 0:
                ChangeShares.subtract(self, monthly_withdrawal)

            if (annual_deposit != 0 or annual_withdrawal != 0) and month == 12:
                ChangeShares.add(self, annual_deposit)
                ChangeShares.subtract(self, annual_withdrawal)
                month = 0

            if self.shares <= 0 and self.broke_time == 0:
                self.broke = True
                self.broke_time = m

            pay_div += 1
            month += 1

        return np.array(values), np.array(prices)

    def summary(self):
        value = (self.shares * self.price) + self.cash

        print(f'The total value of {self.name} is ${value:.2f}')
        print(f'You have {self.shares} shares at a price of ${self.price:.2f}.')
        print(f'You have ${self.cash:.2f} in cash.')
        if self.broke:
            print(f'You will go broke in {(self.broke_time / 12):.2f} years.')


class ChangeShares(Stock):

    def add(self, amount, is_drip=False):
        if not is_drip:
            if amount >= 10:
                amount -= self.commission
                new_shares = np.floor(amount / self.price)
                self.shares += new_shares
                self.cash += amount - new_shares * self.price
        else:
            new_shares = np.floor(amount / self.price)
            self.shares += new_shares
            self.cash += amount - new_shares * self.price

    def subtract(self, amount):
        amount -= self.commission
        if self.cash > 0:
            if amount <= self.cash:
                self.cash -= amount
            else:
                amount_left = amount - self.cash
                self.cash = 0
                sell_shares = np.floor(amount_left / self.price)
                self.shares -= sell_shares
        else:
            sell_shares = np.floor(amount / self.price)
            self.shares -= sell_shares


