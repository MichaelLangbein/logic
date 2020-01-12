from kanren import run, eq, var, conde, membero, Relation, facts


x = var('x')
human = Relation()
facts(human, ['Aristoteles'])

def mortal(x):
    return conde([human(x)])

results = run(1, x, mortal(x))
print(results)


marriedRel = Relation()
facts(marriedRel, ['Mickey', 'Minnie'])

def marriedDer(x, y):
    return conde([marriedRel(x, y)],
                 [marriedDer, y, x])


results = run(5, x, marriedDer(x, 'Mickey'))
print(results)