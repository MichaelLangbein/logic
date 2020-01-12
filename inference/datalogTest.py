from pyDatalog import pyDatalog as pd
pd.create_terms('X, Y, human, mortal, married')


+ human('Aristoteles')
mortal(X) <= human(X)

print(mortal(X))


+ married('Mickey', 'Minnie')
married(X, Y) <= married(Y, X)

print(married(X, Y))
