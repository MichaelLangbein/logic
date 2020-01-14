from kanren import run, eq, var, conde, membero, Relation, facts
from plotly.geometry import BaseGeometry


x = var('x')
human = Relation()
facts(human, ['Aristoteles'])

def mortal(x):
    return conde([human(x)])

results = run(1, x, mortal(x))
print(results)


class GeoObject:
    def __init__(self, name, geometry):
        self.name = name
        self.geometry = geometry


def intersecto(go1, go2):
    return conde([go1.geometry.intersects(go2.geometry)])