from vpython import sphere


class ElectricCharge:
    """
    ElectricCharge represents a physical electric charge. It has a signed magnitude and a vector position. The class
    also accepts a dictionary of object properties in order to draw a spherical object to represent it if desired.
    """
    def __init__(self, value, pos, name, value_alias=None, draw=True, object_props=None):
        if object_props is None:
            object_props = {}

        self.value = value
        self.pos = pos
        self.name = name
        self.value_alias = value_alias
        self.draw = draw
        self.object_props = object_props
        self.object = None

        if bool(self.draw):
            self.draw_obj()

    # Draw the object to represent the charge in the scene
    def draw_obj(self):
        if self.object is None:
            self.object = sphere(pos=self.pos, **self.object_props)

    # Tick the object position
    def tick_obj_pos(self, pos):
        if self.object is not None:
            self.object.pos = pos

    # Gets a text label for this charge
    def get_label_text(self):
        return "{0}={1}".format(self.name, self.value if self.value_alias is None else self.value_alias)