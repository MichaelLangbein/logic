#%%
import numpy as np
import matplotlib.pyplot as plt


"""
firms i = 1 ,..., I
workers/consumers j = 1, ..., J
banks b = 1, ..., B
time t = 1, ..., T

homogenous non-storable consumption good market
labor market
credit services market
"""


def randomExponential(mean):
    pass

def randomUniform(min, max):
    pass



class Household:
    pass

class Firm:
    def __init__(self):
        self.laborProductivity = randomUniform(0, 10)
        self.fractionRnD = randomUniform(0, 1)

    def netWorth(self):
        # a stock variable equal to the sum of past retained net profits
        pass

    def researchAndDevelopment(self):
        # productivity can be increased by an uncertain amount 
        # thanks to investments in R&D, determined as a fixed fraction 
        # of the last periods gross profits
        fractionRnD = self.fractionRnD
        rndBudget = self.profits * fractionRnD
        sales = self.price * self.production
        z = randomExponential(mean = rndBudget / sales)
        self.laborProductivity = self.laborProductivity + z

    def decideProductionLaborPrice(self):
        # By looking at their past experience, each operating firm 
        # determines the amount of output to be produced 
        # (hence, the amount of labor to be hired) and the price. 
        # Expectations on future demand are updated adaptively
        production = 
        laborDemand = production / self.laborProductivity
        pass

    def produce(self):
        production = self.laborProductivity * self.labor
        return production

    def bookkeeping(self):
        # calculate profits, update net worth and,
        # if internal resources are enough, pay back debt obligations.



        pass


class Bank:
    def netWorth(self):
        # a stock variable equal to the sum of past retained net profits
        pass


class LaborMarket:
    def __init__(self, households, firms):
        self.households = households
        self.firms = firms

    def payWages(self):
        pass


class FinancialMarket:
    def __init__(self, firms, banks):
        self.firms = firms
        self.banks = banks

    def createCreditApplicationsIfRequired(self):
        # If internal financial resources are in short supply for paying wages, and fill in a fixed number of applications to obtain credit
        pass

    def allocateCredit(self):
        # banks allocate credit collecting individual demands, 
        # sorting them in descending order according to the financial viability of firms, 
        # and satisfy them until all credit supply has been exhausted
        # The contractual interest rate is calculated applying a markup 
        # (function of financial viability) on an exogenously determined baseline.
        pass


class GoodsMarket:
    def __init__(self, households, firms):
        self.households = households
        self.firms = firms

    def trade(self):
        # Firms post their offer price, 
        # while consumers are allowed to muddle through searching for a satisfying deal. 
        # If a firm ends up with excess supply, it gets rid of the unsold goods at zero costs.
        pass



households = [Household() for h in range(1000)]
firms = [Firm() for f in range(100)]
banks = [Bank() for b in range(30)]


for t in range(100):

    # 1. check financial viability

    for f, firm in enumerate(firms):
        if firm.netWorth() < 0:
            firms[f] = Firm()
    for b, bank in enumerate(banks):
        if bank.netWorth() < 0:
            banks[b] = Bank()

    # 2. R&D

    for firm in firms:
        firm.researchAndDevelopment()

    # 3. decide on production

    for firm in firms:
        firm.decideProductionLaborPrice()

    # 4. labor market
    
    lm = LaborMarket(households, firms)
    lm.payWages()

    # 5. if no funds for wages, take on credits

    fm = FinancialMarket(firms, banks)
    fm.createCreditApplicationsIfRequired()
    fm.allocateCredit()

    # 6. production
    for firm in firms:
        firm.produce()

    # 7. goods market

    gm = GoodsMarket(households, firms)
    gm.trade()
    
    # 8. bookkeeping 
    for firm in firms:
        firm.bookkeeping()


