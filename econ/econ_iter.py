#%%
import numpy as np


class Household:
    money = 100

    def workSupply(self, possibleWages):
        return np.array([w/100 for w in  possibleWages])
    
    def consumptionDemand(self, possiblePrices):
        return np.array([p/100 for p in possiblePrices])
    
    def moneyDemand():
        pass

class Firm:
    money = 100

    def workDemand(self, possibleWages):
        # L = (w / paK^(1-a))^(1/(a-1))
        return np.array([1 - w/100 for w in possibleWages])

    def goodsSupply(self, possiblePrices):
        return np.array([p/100 for p in  possiblePrices])

class Government:
    money = 100
    taxRate = 0.1

    def moneyDemand():
        pass

class Bank:
    money = 100
    reserveFraction = 0.1

    def moneySupply():
        pass




def intersect(xs, y1s, y2s):
    diff = np.abs(y1s - y2s)
    i = np.argmin(diff)
    x = xs[i]
    y = y1s[i]
    return x, y

def taxMarket(households: Household, government: Government):
    return government.taxRate * households.money

def factorMarket(households: Household, firms: Firm):
    possibleWages = np.arange(0, 100, 0.1)
    workDemand = firms.workDemand(possibleWages)
    workSupply = households.workSupply(possibleWages)
    wage, work = intersect(possibleWages, workDemand, workSupply)
    return work, wage

def goodsMarket(households: Household, firms: Firm):
    possiblePrices = np.arange(0, 100, 0.1)
    goodsDemand = households.consumptionDemand(possiblePrices)
    goodsSupply = firms.goodsSupply(possiblePrices)
    price, goods = intersect(possiblePrices, goodsDemand, goodsSupply)
    return price, goods

def moneyMarket():
    pass


households = Household()
firms = Firm()
government = Government()

for y in range(100):
    for m in range(12):

        taxes = taxMarket(households, government)
        employment, wages = factorMarket(households, firms)
        prices, consumption = goodsMarket(households, firms)

        government.money += taxes

        firms.employment = employment
        firms.money -= wages * employment
        firms.money += prices * consumption

        households.consumption = consumption
        households.money += wages * employment
        households.money -= prices * consumption
        households.money -= taxes

        print({"h": households.money, "f": firms.money, "g": government.money, "t": households.money + firms.money + government.money})


# %%
