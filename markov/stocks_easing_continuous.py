#%% 
import scipy.stats as scs
import numpy.random as npr


gamma = 0.95



def possibleActions(state):
    t, v, s = state.split('/')
    if s == 'holding':
        return ['keep', 'sell']
    if s == 'sold':
        return ['-']



def sampleState():
    # should be ergodic sample
    sample = []
    for t in range(10):
        for v in range(10, 30): # better: sample here according to prediction
            for s in ['holding', 'sold']:
                sample.append(f"{t}/{v}/{s}")
    return sample


def isEndState(state):
    t, v, s = state.split('/')
    return s == 'sold' or int(t) >= 9


def reward(sNext, state, a):
    t, v, s = state.split('/')
    if a == 'sell':
        if v == 'high':
            return 10
        if v == 'mid':
            return 5
        if v == 'low':
            return 1
    return 0


def prob(sNext, state, a):
    ts, vs, ss = state.split('/')
    tn, vn, sn = sNext.split('/')

    # excluding impossible combinations
    if ss == 'sold' and sn != 'sold':
        return 0
    if a == 'sell' and sn != 'sold':
        return 0
    if int(ts) + 1 != int(tn):
        return 0

    norm = scs.norm(float(vs), 1.5)
    return norm.pdf(float(vn))
   
    

def differenceFunction(v1, v2):
    e = 0
    for key in v1:
        e += (v1[key] - v2[key]) ** 2
    return e


def qValue(state, action, Vold):
    if isEndState(state):
        return 0
    v = 0
    for sNext in Vold.keys():
        vNow = reward(sNext, state, action)
        vFut = Vold[sNext]
        p = prob(sNext, state, action)
        v += p * (vNow + gamma * vFut)
    return v


def evalStrategy(strategy):
    S = sampleState()
    Vnew = {s: 0 for s in S}
    error = 99999
    while error > 0.001:
        Vold = Vnew
        Vnew = {}
        for s in S:
            action = strategy[s]
            Vnew[s] = qValue(s, action, Vold)
        error = differenceFunction(Vnew, Vold)
    return Vnew


def optimalStrategy():
    strategy = {}
    S = sampleState()
    Vnew = {s: 0 for s in S}
    error = 99999
    while error > 0.05:
        Vold = Vnew
        Vnew = {}
        for s in S:
            maxQs = -99999
            for a in possibleActions(s):
                qs = qValue(s, a, Vold)
                if qs > maxQs:
                    maxQs = qs
                    strategy[s] = a
            Vnew[s] = maxQs
        error = differenceFunction(Vnew, Vold)
    return strategy

# %%
sOpt = optimalStrategy()
print(sOpt)

sVal = evalStrategy(sOpt)
for s in sOpt:
    print(f"{s} -- {sOpt[s]} -- {sVal[s]}")
# %%
