"""
This is the main Abstraction Class for the controllers using Formal Abstraction to be able to
control different motors by using this class.
"""

import os
import sys
from abc import abstractmethod
from abc import ABCMeta


class MotorController(metaclass=ABCMeta):
    @abstractmethod
    def next_channel(self):
        pass
