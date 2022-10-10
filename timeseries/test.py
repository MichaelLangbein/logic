#%%
import scipy.stats as ss
import numpy.random as nr


#%% domain specific mix-in's


fee = 1.2
possibleValues = [i * fee for i in range(10)]

def last(l, n=1):
    if n == 1:
        return l[-1]
    return l[-n:]

def possibleNextStates(state, action):
    pns = []
    if action == 'sell':
        pns.append([*state, 'sold'])
    else:
        for next in possibleValues:
            pns.append([*state, next])
    return pns

def endState(state):
    return last(state) == 'sold'

def prob(nextState, state, action):
    if action == 'sell':
        if last(nextState) == 'sold':
            return 1.0
        else:
            return 0.0
    mu = last(state) / fee
    x = last(nextState) / fee
    distr = ss.binom(len(possibleValues), mu/len(possibleValues))
    p = distr.cdf(x + 1) - distr.cdf(x)
    return p

# def prob(nextState, state, action):
#     if action == 'sell':
#         if last(nextState) == 'sold':
#             return 1.0
#         else:
#             return 0.0
#     if last(nextState) > last(state):
#         return 1.0
#     else:
#         return 0

def reward(nextState, state, action):
    if action == 'sell':
        return last(state) - fee
    if action == 'buy':
        return - last(state) - fee
    return 0


def cacheKeyFunction(policy, state, action):
    return f"{last(state, 2)}/{action}"


#%% core

gamma = 0.9

cache = {}
def memo(qVal):
    def cachedQVal(policy, state, action):
        key = cacheKeyFunction(policy, state, action)
        if key in cache:
            return cache[key]
        r = qVal(policy, state, action)
        cache[key] = r
        return r
    return cachedQVal

@memo
def cachedValue(policy, state, action):
    """ expected utility of state given action and policy """
    v = 0
    for nextState in possibleNextStates(state, action):
        p = prob(nextState, state, action)
        vNow = reward(nextState, state, action)
        vFut = value(policy, nextState)
        v += p * (vNow + gamma * vFut)
    return v


def value(policy, state):
    """ expected utility of state given policy """
    if endState(state):
        return 0
    else:
        action = policy(state)
        return cachedValue(policy, state, action)


#%% evaluation

def createPolicy(tBuy, tSell):
    def policy(state):
        if len(state) - 1 == tBuy:
            return 'buy'
        if len(state) - 1 == tSell:
            return 'sell'
        return 'keep'
    return policy

T = 30
state0 = [possibleValues[3]]
vPolMax = -99999999

for tBuy in range(0, T-1):
    for tSell in range(tBuy + 1, T):
        policy = createPolicy(tBuy, tSell)
        vPol = value(policy, state0)
        print(f"Evaluated {tBuy} - {tSell} => {vPol}")
        if vPol > vPolMax:
            vPolMax = vPol
            polOpt = (tBuy, tSell, vPolMax)

print(polOpt)

# %%
