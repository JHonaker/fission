from abc import ABC, abstractmethod


class Component(ABC):

    def __init__(self):
        pass


class BasicComponent(Component):

    def __init__(self, x):
        self.id = "Test: " + x
