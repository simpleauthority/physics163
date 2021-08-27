from vpython import sphere, label, vec


class ElectricCharge:
    """
    ElectricCharge represents a physical electric charge. It has a signed magnitude and a vector position. The class
    also accepts a dictionary of object properties in order to draw a spherical object to represent it if desired.
    """

    def __init__(self, value, pos, name, value_alias=None, draw=True, extra=None, object_props=None):
        if extra is None:
            extra = {}

        if object_props is None:
            object_props = {}

        self.value = value
        self.pos = pos
        self.name = name
        self.value_alias = value_alias
        self.draw = draw
        self.extra = extra
        self.object_props = object_props
        self.object = None
        self.label = None

        if bool(self.draw):
            self.draw_obj()
            self.draw_label()

    # Draw the object to represent the charge in the scene
    def draw_obj(self):
        if self.object is None:
            self.object = sphere(pos=self.pos, **self.object_props)

    # Tick the object position
    def tick_obj_pos(self, pos):
        if self.object is not None:
            self.object.pos = pos
            self.tick_label_pos()

    # Gets a text label for this charge
    def get_label_text(self):
        return "{0}={1}".format(self.name, self.value if self.value_alias is None else self.value_alias)

    # Draws a label containing the label text on top of the object
    def draw_label(self):
        if self.label is None:
            self.label = label(pos=self.pos + vec(0, -2 * self.object.radius, 0), height=11, text=self.get_label_text())

    # Updates the label pos to the object position
    def tick_label_pos(self):
        if self.label is not None:
            self.label.pos = self.object.pos + vec(0, -2 * self.object.radius, 0)
