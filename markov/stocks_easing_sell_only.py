#%% 
gamma = 0.95

S = [  # time / stock price / ownership
    '1/low/holding', '1/mid/holding', '1/high/holding',
    '2/low/holding', '2/mid/holding', '2/high/holding',
    '3/low/holding', '3/mid/holding', '3/high/holding',
    '4/low/holding', '4/mid/holding', '4/high/holding',
    '5/low/holding', '5/mid/holding', '5/high/holding',
    '6/low/holding', '6/mid/holding', '6/high/holding',
    '7/low/holding', '7/mid/holding', '7/high/holding',
    '8/low/holding', '8/mid/holding', '8/high/holding',
    '9/low/holding', '9/mid/holding', '9/high/holding',
    '1/low/sold', '1/mid/sold', '1/high/sold',
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
    if s == 'holding':
        return ['keep', 'sell']
    if s == 'sold':
        return ['-']


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

    # # strictly declining market. 
    # # MDP will suggest always selling
    # if vs == 'low':
    #     if vn == 'low':
    #         return 1
    #     if vn == 'mid':
    #         return 0
    #     if vn == 'high':
    #         return 0
    # if vs == 'mid':
    #     if vn == 'low':
    #         return 1
    #     if vn == 'mid':
    #         return 0
    #     if vn == 'high':
    #         return 0
    # if vs == 'high':
    #     if vn == 'low':
    #         return 0
    #     if vn == 'mid':
    #         return 1
    #     if vn == 'high':
    #         return 0

    # strictly increasing market.
    # MDP will suggest selling only when high    
    if vs == 'low':
        if vn == 'low':
            return 0
        if vn == 'mid':
            return 1
        if vn == 'high':
            return 0
    if vs == 'mid':
        if vn == 'low':
            return 0
        if vn == 'mid':
            return 0
        if vn == 'high':
            return 1
    if vs == 'high':
        if vn == 'low':
            return 0
        if vn == 'mid':
            return 0
        if vn == 'high':
            return 1
    
    # pretty random market.
    # if vs == 'low':
    #     if vn == 'low':
    #         return 0.4
    #     if vn == 'mid':
    #         return 0.4
    #     if vn == 'high':
    #         return 0.2
    # if vs == 'mid':
    #     if vn == 'low':
    #         return 0.3
    #     if vn == 'mid':
    #         return 0.4
    #     if vn == 'high':
    #         return 0.3
    # if vs == 'high':
    #     if vn == 'low':
    #         return 0.2
    #     if vn == 'mid':
    #         return 0.4
    #     if vn == 'high':
    #         return 0.4
                    
    

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

# %%
sVal = evalStrategy(sOpt)
for s in sOpt:
    print(f"{s} -- {sOpt[s]} -- {sVal[s]}")
# %%
