"""
This is the HAL Class for the PI Controller. The methods defined by the hal_controller.py
are going to be implemented here for the correct control of the PI Controller.
"""

import logging
from ..hal_controller import MotorController
from .pi_controller_api import *


logging.basicConfig(
    level = logging.INFO,
    format = '%(threadName)s-%(levelname)s-%(message)s')


class PiHalClass(MotorController):
    def __init__(self):
        self.pi = PiControllerApi()

    def connect(self):
        if self.pi.get_connected():
            logging.info(f"{self.connect.__qualname__} not done because system is already Connected.")
        else:
            self.pi.connect()
            self.pi.enable()
            self.pi.commut()

    def disconnect(self):
        self.pi.disable()
        self.pi.disconnect()

    def move_relative_positive(self):
        self.pi.move_relative_positive()

    def move_relative_negative(self):
        self.pi.move_relative_negative()

    def move_absolute(self):
        self.pi.move_absolute()

    def stop_motion(self):
        self.pi.stop_motion()

    # In order to set the position at main, the instance function has to be returned
    def set_position(self):
        return self.pi.property_position.set_position

    # In order to set the distance at main, the instance function has to be returned
    def set_distance(self):
        return self.pi.property_distance.set_distance

    # Validation if the controller is connected is done here, without decorators.
    # It is done in tha way to avoid returning back confusing values to PyQt5 indicator.
    def get_position(self):
        if self.pi.get_connected():
            return self.pi.get_position()
        else:
            return None

    def get_connected(self):
        return self.pi.get_connected()

    def get_moving(self):
        if self.pi.get_connected():
            # Getting binary number to check the moving state of the motor.
            # [-6] is the position of the moving bit.
            motor_state = str(bin(self.pi.get_motor_state()))[-6]
            moving = motor_state == '1'
            return moving
        else:
            return False
