#%%
import scipy.stats as ss
import numpy.random as nr


#%% domain specific mix-in's


def possibleNextStates(state, action):
    pns = []
    if action == 'stay':
        pns.append('in')
        pns.append('out')
    else:
        pns.append('out')
    return pns

def endState(state):
    return state == 'out'


def prob(nextState, state, action):
    if state == 'out':
        if nextState == 'out':
            return 1.0
        else:
            return 0.0
    if action == 'stay':
        if nextState == 'in':
            return 0.6667
        else:
            return 0.3333
    if action == 'leave':
        if nextState == 'out':
            return 1.0
        else:
            return 0.0


def reward(nextState, state, action):
    if action == 'stay':
        if nextState == 'in':
            return 4
        if nextState == 'out':
            return 0
    if action == 'leave':
        return 10


#%% core

gamma = 1.0

cache = {}
def memo(qVal):
    def cachedQVal(policy, state, action):
        key = f"{state}/{action}"
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

def stayPolicy(state):
    if stayPolicy.counter > 0:
        stayPolicy.counter -= 1
        return 'stay'
    return 'leave'
stayPolicy.counter = 4

def leavePolicy(state):
    return 'leave'

vPolMax = -99999999

for policy in [stayPolicy, leavePolicy]:
        vPol = value(policy, 'in')
        print(f"Evaluated {policy.__name__} => {vPol}")
        if vPol > vPolMax:
            vPolMax = vPol
            polOpt = (policy, vPolMax)

print(polOpt)

# %%
