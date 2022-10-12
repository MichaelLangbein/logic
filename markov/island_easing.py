#%%

gamma = 0.95
S = [
    '1/1', '1/2', '1/3', '1/4',
    '2/1', '2/2', '2/3', '2/4',
    '3/1', '3/2', '3/3', '3/4',
]

def possibleActions(state):
    A = ['up', 'right', 'down', 'left']
    r, c = [int(v) for v in state.split('/')]
    if r == 1:
        A.remove('up')
    if c == 1:
        A.remove('left')
    if r == 3:
        A.remove('down')
    if c == 4:
        A.remove('right')
    return A

def isEndState(s):
    return s == '1/3' or s == '2/3' or s == '1/4' or s == '3/1'

def reward(sNext, s, a):
    if sNext == '1/3' or sNext == '2/3':
        return -50
    if sNext == '1/4':
        return 20
    if sNext == '3/1':
        return 2
    return 0

def neighbor(pa, pb):
    [ra, ca] = pa
    [rb, cb] = pb
    if abs(ra - rb) <= 1 and abs(ca - cb) <= 1:
        return True
    return False

def prob(sNext, s, a):
    pSlip = 0.1
    r, c = [int(v) for v in s.split('/')]
    rN, cN = [int(v) for v in sNext.split('/')]
    if a == 'up' and rN == r-1 and c == cN:
        return 1 - pSlip
    if a == 'right' and rN == r and c+1 == cN:
        return 1 - pSlip
    if a == 'down' and rN == r+1 and c == cN:
        return 1 - pSlip
    if a == 'left' and rN == r and c-1 == cN:
        return 1 - pSlip
    elif neighbor([r, c], [rN, cN]):
        return pSlip / 8
    else:
        return 0

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



def optimalStrategy():
    strategy = {}
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
        error = errorFunc(Vnew, Vold)
    return strategy

#%%
strat = optimalStrategy()
vStrat = evalStrategy(strat)
for s in strat:
    r, c = s.split('/')
    print(f"{s} -- {strat[s]} -- {vStrat[s]}")

# %%
