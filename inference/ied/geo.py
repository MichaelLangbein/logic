from ied.base import Object, TestableRelation
from ied.simpleRelation import SimpleTestableRelation
from ied.engine import InferenceEngine
from shapely.geometry.base import BaseGeometry
from shapely.geometry import Polygon, LineString


class GeoObject(Object):
    def __init__(self, description, geometry: BaseGeometry):
        super().__init__(description)
        self.geometry = geometry




def __intersectionTest(*args):
    if len(args) != 2:
        return False
    obj1 = args[0]
    obj2 = args[1]
    if not isinstance(obj1, GeoObject) or not isinstance(obj2, GeoObject):
        return False
    return obj1.geometry.intersects(obj2.geometry)


intersects = SimpleTestableRelation('intersects', __intersectionTest)
