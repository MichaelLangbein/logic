
gamma = 0.95

S = [  # time / stock price / my debt
    '1/low/none', '1/mid/none', '1/high/none',
    '2/low/none', '2/mid/none', '2/high/none',
    '3/low/none', '3/mid/none', '3/high/none',
    '4/low/none', '4/mid/none', '4/high/none',
    '5/low/none', '5/mid/none', '5/high/none',
    '6/low/none', '6/mid/none', '6/high/none',
    '7/low/none', '7/mid/none', '7/high/none',

    '2/low/low', '2/mid/low', '2/high/low',
    '3/low/low', '3/mid/low', '3/high/low',
    '4/low/low', '4/mid/low', '4/high/low',
    '5/low/low', '5/mid/low', '5/high/low',
    '6/low/low', '6/mid/low', '6/high/low',
    '7/low/low', '7/mid/low', '7/high/low',
    '8/low/low', '8/mid/low', '8/high/low',
    '9/low/low', '9/mid/low', '9/high/low',

    '2/low/mid', '2/mid/mid', '2/high/mid',
    '3/low/mid', '3/mid/mid', '3/high/mid',
    '4/low/mid', '4/mid/mid', '4/high/mid',
    '5/low/mid', '5/mid/mid', '5/high/mid',
    '6/low/mid', '6/mid/mid', '6/high/mid',
    '7/low/mid', '7/mid/mid', '7/high/mid',
    '8/low/mid', '8/mid/mid', '8/high/mid',
    '9/low/mid', '9/mid/mid', '9/high/mid',

    '2/low/high', '2/mid/high', '2/high/high',
    '3/low/high', '3/mid/high', '3/high/high',
    '4/low/high', '4/mid/high', '4/high/high',
    '5/low/high', '5/mid/high', '5/high/high',
    '6/low/high', '6/mid/high', '6/high/high',
    '7/low/high', '7/mid/high', '7/high/high',
    '8/low/high', '8/mid/high', '8/high/high',
    '9/low/high', '9/mid/high', '9/high/high',

    '2/low/sold', '2/mid/sold', '2/high/sold',
    '3/low/sold', '3/mid/sold', '3/high/sold',
    '4/low/sold', '4/mid/sold', '4/high/sold',
    '5/low/sold', '5/mid/sold', '5/high/sold',
    '6/low/sold', '6/mid/sold', '6/high/sold',
    '7/low/sold', '7/mid/sold', '7/high/sold',
    '8/low/sold', '8/mid/sold', '8/high/sold',
    '9/low/sold', '9/mid/sold', '9/high/sold',
]


def possibleActions(state):
    t, v, s = state.split('/')
    if s == 'none':
        return ['keep', 'buy']
    if s in ['low', 'mid', 'high']:
        return ['keep', 'sell']
    if s == 'sold':
        return ['keep']


def isEndState(state):
    t, v, s = state.split('/')
    return s == 'sold'


def reward(sNext, state, a):
    t, v, s = state.split('/')
    if a == 'sell':
        if v == 'high':
            return 10
        if v == 'mid':
            return 5
        if v == 'low':
            return 1
    if a == 'buy':
        if v == 'high':
            return -10
        if v == 'mid':
            return -5
        if v == 'low':
            return -1
    return 0


def prob(sNext, state, a):
    ts, vs, ss = state.split('/')
    tn, vn, sn = sNext.split('/')

    # excluding impossible combinations
    if ss == 'sold' and sn != 'sold':
        return 0
    if ss in ['low', 'mid', 'high'] and sn == 'none':
        return 0
    if a == 'buy':
        if sn != vs:
            return 0
    if a == 'sell' and sn != 'sold':
        return 0
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
    while error > 0.001:
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

sOpt = optimalStrategy()
print(sOpt)