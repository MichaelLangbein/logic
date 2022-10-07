S = ['in', 'out']
A = ['stay', 'quit']
gamma = 0.9

def reward(sNext, s, a):
    if s == 'out':
        return 0
    if s == 'in':
        if a == 'quit':
            return 10
        if a == 'stay':
            if sNext == 'in':
                return 4
            if sNext == 'out':
                return 0

def isEndState(s):
    return s == 'out'

def prob(sNext, s, a):
    if s == 'out':
        if sNext == 'out':
            return 1
        else:
            return 0
    if s == 'in':
        if a == 'stay':
            if sNext == 'in':
                return 0.66667
            if sNext == 'out':
                return 0.33333
        if a == 'quit':
            return 1

def maxDif(pOld, pNew):
    md = 0
    for pOi, pNi in zip(pOld, pNew):
        if pOi != pNi:
            md += 1
    return md


def memo(f):
    cache = {}
    def memedFunc(p, b):
        pStr = f"{p}".replace("'", "").replace(" ", "").replace(", ", "")
        if pStr in cache and b in cache[pStr]:
            return cache[pStr][b]
        val = f(p, b)
        if pStr not in cache:
            cache[pStr] = {}
        cache[pStr][b] = val
        return val
    return memedFunc

@memo
def calcValue(policy, s):
    if isEndState(s):
        return 0
    a = policy[s]
    v = 0
    for sNext in S:
        vNow = reward(sNext, s, a)
        vFut = calcValue(policy, sNext)
        v += prob(sNext, s, a) * (vNow + gamma * vFut)
    return v


def calcPolicy(value, s):
    vMax = 0
    for a in A:
        v = 0
        for sNext in S:
            vNow = reward(sNext, s, a)
            vFut = value[sNext]
            v += prob(sNext, s, a) * (vNow + gamma * vFut)
        if v > vMax:
            vMax = v
            aOpt = a
    return aOpt

p = {
    'in': 'quit',
    'out': 'stay'
}
v = {
    'in': 10,
    'out': 10,
}
delta = 1
while delta > 0.01:
    pLast = p
    for s in S:
        v[s] = calcValue(p, s)
    for s in S:
        p[s] = calcPolicy(v, s)
    delta = maxDif(p, pLast)


print(p)