from util.math.Vector import Vector


class Force:
    def __init__(self, value: Vector):
        self.value = value

    def get_acceleration(self, mass: float) -> float:
        return self.value.
