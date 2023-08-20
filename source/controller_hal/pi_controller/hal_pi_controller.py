""" This is the HAL Class for the PI Controller. The methods defined by the hal_controller.py
are going to be implemented here for the correct control of the PI Controller.
"""
import logging
import sys
# Relative import modules
from ..hal_controller import MotorController
from .pi_controller_api import *
from ..utils.functions import read_motor_names


logging.basicConfig(
    level = logging.INFO,
    format = '%(threadName)s-%(levelname)s-%(message)s')


class PiHalClass(MotorController):
    def __init__(self, distance, position):
        self.pi = PiControllerApi(distance, position)
        project_path = sys.path[0]  # Getting the project path
        INI_PATH = '\config\pi_motor_config.ini'
        self.motor_list = read_motor_names(project_path, INI_PATH)
        self.motor1, self.motor2 = self.motor_list
        self.motor = self.motor1  #Setting up a default motor value.

    def motor_select(self, motor_selected):
        if motor_selected == 'Motor 2':
            self.motor = self.motor2
        else:
            self.motor = self.motor1

    def connect(self):
        if self.pi.connection:
            logging.info(f"{self.connect.__qualname__} not done. The controller is connected already.")
        else:
            self.pi.connect()
            for motor in self.motor_list:
                # All motors need to be enabled and commuted to be used.
                self.pi.enable(motor)
                self.pi.commut(motor)

    def disconnect(self):
        self.pi.disable() #Disabling all motors.
        self.pi.disconnect()

    def move_relative_positive(self):
        self.pi.move_relative_positive(self.motor)

    def move_relative_negative(self):
        self.pi.move_relative_negative(self.motor)

    def move_absolute(self):
        self.pi.move_absolute(self.motor)

    def stop_motion(self):
        self.pi.stop_motion(self.motor)

    def set_position(self, value):
        self.pi.position = value

    def set_distance(self, value):
        self.pi.distance = value

    # The validation if the controller is connected is done here, without decorators.
    # It is done in this way to avoid returning back wrong values to the PyQt5 indicators due
    # to the decorators.
    def get_position(self):
        if self.pi.connection:
            return self.pi.get_position(self.motor)
        else:
            return None

    def get_connection(self):
        return self.pi.connection

    def get_moving(self):
        if self.pi.connection:
            # Getting binary number to check the moving state of the motor.
            # [-6] is the position of the moving state bit.
            motor_state = self.pi.get_motor_state(self.motor)
            moving_motor_state = str(bin(motor_state))[-6]
            moving = moving_motor_state == '1'
            return moving
        else:
            return False
