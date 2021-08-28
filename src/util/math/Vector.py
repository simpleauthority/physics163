from math import sqrt

from vpython import vec


class Vector:
    """
    Exists to make vector operations slightly easier than having to deal with VPython's way.
    To each their own but VPython annoys me a little bit. No hate to the VPython team.
    """

    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: 'Vector') -> 'Vector':
        """Overloads the + operator for this vector"""
        return self.add(other)

    def add(self, other: 'Vector') -> 'Vector':
        """Adds the given vector to this vector"""
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __sub__(self, other: 'Vector') -> 'Vector':
        """Overloads the - operator for this vector"""
        return self.subtract(other)

    def subtract(self, other: 'Vector') -> 'Vector':
        """Subtracts the given vector from this vector"""
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __mul__(self, other: float) -> 'Vector':
        """Overloads the * operator for this vector"""
        return self.multiply(other)

    def multiply(self, factor: float) -> 'Vector':
        """Multiplies each vector component by the given factor"""
        self.x *= factor
        self.y *= factor
        self.z *= factor
        return self

    def __div__(self, other: float) -> 'Vector':
        """Overloads the / operator for this vector"""
        return self.divide(other)

    def divide(self, divisor: float) -> 'Vector':
        """Divides each vector component by the given scalar divisor"""
        self.x /= divisor
        self.y /= divisor
        self.z /= divisor
        return self

    def dot(self, other: 'Vector') -> float:
        """Dots this vector with the given other vector"""
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

    def cross(self, other: 'Vector') -> 'Vector':
        """Crosses this vector with the given other vector"""
        self.x = (self.y * other.z) - (other.y - self.z)
        self.y = (self.z * other.x) - (other.z - self.x)
        self.z = (self.x * other.y) - (other.x - self.y)
        return self

    def mag(self) -> float:
        """Gets the magnitude of this vector"""
        return sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

    def magSquared(self) -> float:
        """Gets the squared magnitude of this vector"""
        return self.mag() ** 2

    def scalarDist(self, other: 'Vector') -> float:
        """Gets the scalar distance of this vector from the other"""
        return sqrt(((self.x - other.x) ** 2) + ((self.y - other.y) ** 2) + ((self.z - other.z) ** 2))

    def scalarDistSquared(self, other: 'Vector') -> float:
        """Gets the squared scalar distance of this vector from the other"""
        return self.scalarDist(other) ** 2

    def dist(self, other: 'Vector') -> 'Vector':
        """Gets the vector distance of this vector from the other"""
        return self.clone().subtract(other)

    def hat(self) -> 'Vector':
        """Normalizes this vector and turns it into a unit/hat vector"""
        mag = self.mag()

        if mag is 0:
            raise ArithmeticError("This vector has a magnitude of 0. It cannot be normalized.")
        else:
            self.x /= mag
            self.y /= mag
            self.z /= mag

        return self

    def zero(self) -> 'Vector':
        """Set all vector components to 0"""
        self.x = 0
        self.y = 0
        self.z = 0
        return self

    def set_x(self, x) -> 'Vector':
        """Sets the x component of this vector"""
        self.x = x
        return self

    def set_y(self, y) -> 'Vector':
        """Sets the y component of this vector"""
        self.y = y
        return self

    def set_z(self, z) -> 'Vector':
        """Sets the z component of this vector"""
        self.z = z
        return self

    def clone(self) -> 'Vector':
        """Creates a copy of this vector and returns that copy"""
        return Vector(self.x, self.y, self.z)

    def as_vec(self) -> vec:
        """Converts this Vector to a VPython vec object"""
        return vec(self.x, self.y, self.z)

    def __str__(self) -> str:
        return "<{0}, {1}, {2}>".format(self.x, self.y, self.z)

    @staticmethod
    def from_vec(given: vec) -> 'Vector':
        """Converts a VPython vec object into a Vector"""
        return Vector(given.x, given.y, given.z)
