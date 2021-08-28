from util.object.Sphere import Sphere
from util.math.Vector import Vector


class ElectricCharge(Sphere):
    """
    ElectricCharge represents a physical electric charge. It has a signed magnitude and a vector.py position. The class
    also accepts a dictionary of object properties in order to draw a spherical object to represent it if desired.
    """
    electron_mass = 9.109e-31
    electron_charge = -1.602e-19

    def __init__(self, mass: float = electron_mass, position: Vector = None, value: float = electron_charge):
        super().__init__(mass, position)
        self.value = value

    def name_charge(self, name: str, value_alias: None):
        if value_alias is None:
            value_alias = self.value

        self.set_label_text("{0}={1}".format(name, value_alias))