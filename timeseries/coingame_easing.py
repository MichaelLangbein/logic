#%%

states = ['in', 'out']
gamma = 1.0

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

def endState(state):
    return state == 'out'


def qValue(state, action):
    v = 0
    for nextState in states:
        p = prob(nextState, state, action)
        vNow = reward(nextState, state, action)
        vFut = V_policy_last[nextState]
        v += p * (vNow + gamma * vFut)
    return v


def estimateValue(policy, state):
    if endState(state):
        return 0
    else:
        action = policy(state)
        return qValue(state, action)


def calcDiff(v1, v2):
    d = 0
    for key in v1:
        d += (v1[key] - v2[key])**2
    return d



def stayPolicy(state):
    return 'stay'

def leavePolicy(state):
    return 'leave'

for policy in [stayPolicy, leavePolicy]:
    V_policy = {state: 0 for state in states}
    diff = 99999
    while diff > 0.05:
        V_policy_last = V_policy
        V_policy = {}
        for state in states:
            V_policy[state] = estimateValue(policy, state)
        diff = calcDiff(V_policy, V_policy_last)
    print(f"{policy.__name__} -> {V_policy}")


# %%
