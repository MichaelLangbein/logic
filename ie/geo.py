from ie.base import Object, TestableRelation
from ie.engine import InferenceEngine
from shapely.geometry.base import BaseGeometry
from shapely.geometry import Polygon, LineString


class GeoObject(Object):
    def __init__(self, description, geometry: BaseGeometry):
        super().__init__(description)
        self.geometry = geometry


def intersection(ie: InferenceEngine, *args):
    obj1Candidates = ie.evalExpression(args[0])
    obj2Candidates = ie.evalExpression(args[1])

    truthList = []

    for o1c in obj1Candidates:
        for o2c in obj2Candidates:
            if isinstance(o1c[0], GeoObject) and isinstance(o2c[0], GeoObject) and o1c[0] != o2c[0]:
                if o1c[0].geometry.intersects(o2c[0].geometry):
                    truthList.append((intersects, o1c[0], o2c[0]))

    return truthList

intersects = TestableRelation('intersects', intersection)
