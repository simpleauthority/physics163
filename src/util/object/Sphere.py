from vpython import sphere

from util.math.Vector import Vector
from util.object.PhysicalObject import PhysicalObject


class Sphere(PhysicalObject):
    def __init__(self, mass: float = 1, position: Vector = None):
        PhysicalObject.__init__(self, mass, position)

    def create(self, position: Vector = Vector(0, 0, 0), **kwargs) -> None:
        self.__object_backend__ = sphere(
            pos=self.position.as_vec(),
            **kwargs
        )
