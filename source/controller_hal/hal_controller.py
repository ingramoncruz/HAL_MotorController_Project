"""
This is the main Abstraction Class for the controllers using Formal Abstraction to be able to
control different motors by using this class.
"""
from abc import abstractmethod
from abc import ABCMeta


class MotorController(metaclass=ABCMeta):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def move_relative_positive(self):
        pass

    @abstractmethod
    def move_relative_positive(self):
        pass

    @abstractmethod
    def move_relative_negative(self):
        pass

    @abstractmethod
    def move_absolute(self):
        pass

    @abstractmethod
    def stop_motion(self):
        pass

    @abstractmethod
    def set_position(self):
        pass

    @abstractmethod
    def set_distance(self):
        pass

    @abstractmethod
    def get_position(self):
        pass

    @abstractmethod
    def get_connected(self):
        pass

    @abstractmethod
    def get_moving(self):
        pass

    @abstractmethod
    def motor_select(self):
        pass
