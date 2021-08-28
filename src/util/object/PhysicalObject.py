from abc import ABC, abstractmethod

from vpython import label

from util.math.Vector import Vector


class PhysicalObject(ABC):
    """This class represents a drawable and labelable physical object with mass"""

    def __init__(self, mass: float = 1.0, position: Vector = None):
        self.mass = mass
        self.position = position
        self.label_text = None
        self.label_relative_position = None

        self.__label_backend__ = None
        self.__object_backend__ = None

    def set_position(self, position: Vector) -> None:
        self.position = position

    def tick(self, position: Vector, object_kwargs=None, label_kwargs=None):
        if object_kwargs is None:
            object_kwargs = {}

        if label_kwargs is None:
            label_kwargs = {}

        self.position = position
        self.__tick_object__(**object_kwargs)
        self.__tick_label__(**label_kwargs)

    def draw(self, position: Vector = Vector(0, 0, 0), **kwargs) -> None:
        if self.position is None:
            raise RuntimeError("Cannot draw an object at nonexistent position.")

        if self.__object_backend__ is not None:
            raise RuntimeError("Object has already been drawn. Tick it instead.")

        self.create(position, **kwargs)

    def __tick_object__(self, **kwargs) -> None:
        if self.position is None or self.__object_backend__ is None:
            raise RuntimeError("Either the object position is not set or the object has not been drawn. Cannot tick.")

        self.__object_backend__['pos'] = self.position.as_vec()

        for (key, value) in kwargs:
            self.__object_backend__[key] = value

    @abstractmethod
    def create(self, position: Vector = Vector(0, 0, 0), **kwargs) -> None:
        pass

    def set_label_text(self, label_text: str) -> None:
        self.label_text = label_text

    def set_label_relative_position(self, label_relative_position: Vector) -> None:
        self.label_relative_position = label_relative_position

    def draw_label(self, **kwargs):
        if self.__object_backend__ is None:
            raise RuntimeError("Cannot draw a label for object which has not been drawn. Draw the object first.")

        if self.label_text is None or self.label_text == "":
            raise RuntimeError("Cannot draw an empty label. Set the label text first.")

        if self.__label_backend__ is not None:
            raise RuntimeError("Label has already been drawn. Tick it instead.")

        position = self.position

        if self.label_relative_position is not None:
            position += self.label_relative_position

        self.__label_backend__ = label(pos=position.as_vec(), text=self.label_text, **kwargs)

    def __tick_label__(self, **kwargs):
        if self.position is None or self.__object_backend__ is None or self.__label_backend__ is None:
            raise RuntimeError(
                "Either the object position is not set, the object has not been drawn, or the label has not been drawn. Cannot tick.")

        position = self.position

        if self.label_relative_position is not None:
            position += self.label_relative_position

        self.__label_backend__['pos'] = position.as_vec()

        for (key, value) in kwargs:
            self.__label_backend__[key] = value
