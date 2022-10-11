
gamma = 0.95
S = [
    '1/low', '1/mid', '1/high',
    '2/low', '2/mid', '2/high',
    '3/low', '3/mid', '3/high',
    '4/low', '4/mid', '4/high',
    '5/low', '5/mid', '5/high',
    '6/low', '6/mid', '6/high',
    'sold'
]
A = ['buy', 'sell', 'keep']

def isEndState(s):
    return s == 'sold'

def reward(sNext, s, a):
    ts, vs = s.split('/')
    if a == 'sell':
        if vs == 'high':
            return 10
        if vs == 'mid':
            return 5
        if vs == 'low':
            return 1
    if a == 'buy':
        if vs == 'high':
            return -10
        if vs == 'mid':
            return -5
        if vs == 'low':
            return -1
    return 0


def prob(sNext, s, a):
    if s == 'sold':
        if sNext == 'sold':
            return 1
        return 0
    if sNext == 'sold':
        if a == 'sell':
            return 1
        return 0
    
    ts, vs = s.split('/')
    tn, vn = sNext.split('/')

    if int(ts) + 1 != int(tn):
        return 0

    if vs == 'low':
        if vn == 'low':
            return 0.4
        if vn == 'mid':
            return 0.4
        if vn == 'high':
            return 0.2
    if vs == 'mid':
        if vn == 'low':
            return 0.3
        if vn == 'mid':
            return 0.4
        if vn == 'high':
            return 0.3
    if vs == 'high':
        if vn == 'low':
            return 0.2
        if vn == 'mid':
            return 0.4
        if vn == 'high':
            return 0.4
                    

def errorFunc(v1, v2):
    e = 0
    for key in v1:
        e += (v1[key] - v2[key]) ** 2
    return e


def qValue(state, action, Vold):
    if isEndState(state):
        return 0
    v = 0
    for sNext in S:
        vNow = reward(sNext, state, action)
        vFut = Vold[sNext]
        p = prob(sNext, state, action)
        v += p * (vNow + gamma * vFut)
    return v


def evalStrategy(strategy):
    Vnew = {s: 0 for s in S}
    error = 99999
    while error > 0.05:
        Vold = Vnew
        Vnew = {}
        for s in S:
            action = strategy[s]
            Vnew[s] = qValue(s, action, Vold)
        error = errorFunc(Vnew, Vold)
    return Vnew



s0 = S[0]
vOpt = -99999
for tBuy in range(1, 4):
    for tSell in range(tBuy + 1, 6):
        def action(state):
            if state == 'sold':
                return 'keep'
            ts, vs = state.split('/')
            if int(ts) == tBuy:
                return 'buy'
            if int(ts) == tSell:
                return 'sell'
            return 'keep'
        strat = {
            state: action(state) for state in S
        }
        v = evalStrategy(strat)
        if v[s0] > vOpt:
            vOpt = v[s0]
            stratOpt = strat
print(stratOpt)