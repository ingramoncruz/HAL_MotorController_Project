""" This is the HAL Class for the Newport Controller. The methods defined by the hal_controller.py
are going to be implemented here for the correct control of the Newport Controller.
"""
import configparser
import logging
import sys
# Relative import modules
from ..hal_controller import MotorController
from .newport_controller_api import *
from ..utils.functions import read_motor_names


logging.basicConfig(
    level = logging.INFO,
    format = '%(threadName)s-%(levelname)s-%(message)s')


class NewportHalClass(MotorController):
    def __init__(self, distance, position):
        self.np = NewportControllerApi(distance, position)
        project_path = sys.path[0]  # Getting the project path
        INI_PATH = '\config\_newport_motor_config.ini'
        self.motor_list = read_motor_names(project_path, INI_PATH)
        self.motor1, self.motor2 = self.motor_list
        self.motor = self.motor1  #Setting up a default motor value.
        self.group1 = self.motor1.split('.')[0]
        self.group2 = self.motor2.split('.')[0]
        self.group_list = [self.group1, self.group2]
        self.group = self.group1 #Setting up a default group value.

    def motor_select(self, motor_selected):
        if motor_selected == 'Motor 2':
            self.motor = self.motor2
            self.group = self.group2
        else:
            self.motor = self.motor1
            self.group = self.group1

    def connect(self):
        if self.np.connection:
            logging.info(f"{self.connect.__qualname__} not done. The controller is connected already.")
        else:
            self.np.connect()
            for group in self.group_list:
                # All motors need to be initialized and homed to be used.
                self.np.initialize(group)
                self.np.home(group)
            self.np.connection = True
            for motor in self.motor_list:
                # Setting a default low velocity and acceleration in each motor.
                self.np.set_velocity_acceleration(motor, 50, 500)

    def disconnect(self):
        for group in self.group_list:
            # All motor groups need to be killed (disabled and unreferenced).
            self.np.kill(group)
        self.np.disconnect()

    def move_relative_positive(self):
        self.np.move_relative_positive(self.motor)

    def move_relative_negative(self):
        self.np.move_relative_negative(self.motor)

    def move_absolute(self):
        self.np.move_absolute(self.motor)

    def stop_motion(self):
        self.np.stop_motion(self.group)

    def set_position(self, value):
        self.np.position = value

    def set_distance(self, value):
        self.np.distance = value

    # The validation if the controller is connected is done here, without decorators.
    # It is done in this way to avoid returning back wrong values to the PyQt5 indicators due
    # to the decorators.
    def get_position(self):
        if self.np.connection:
            position = self.np.get_position(self.group)
            return position
        else:
            return None

    def get_connection(self):
        return self.np.connection

    def get_moving(self):
        if self.np.connection:
            motor_state = self.np.get_motor_state(self.group)
            moving = motor_state == 1
            return moving
        else:
            return False
