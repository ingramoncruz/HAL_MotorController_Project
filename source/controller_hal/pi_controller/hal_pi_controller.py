"""
This is the HAL Class for the PI Controller. The methods defined by the hal_controller.py
are going to be implemented here for the correct control of the PI Controller.
"""
import configparser
import logging
import sys
# Relative import modules
from ..hal_controller import MotorController
from .pi_controller_api import *


logging.basicConfig(
    level = logging.INFO,
    format = '%(threadName)s-%(levelname)s-%(message)s')


def read_ini_file(path):
    """Function to read all the parameters at the Config.ini file"""
    inifile_path = path + '\config\pi_motor_config.ini'
    config = configparser.ConfigParser()
    config.read(inifile_path)
    return config['Motors Name']['Motor 1'], config['Motors Name']['Motor 2']


class PiHalClass(MotorController):
    def __init__(self):
        self.pi = PiControllerApi()
        PROJECT_PATH = sys.path[0]  # Getting the project path
        self.motor_list = read_ini_file(PROJECT_PATH)
        self.motor1, self.motor2 = self.motor_list
        self.motor = self.motor1  #Setting up a default value.

    def motor_select(self, motor_selected):
        if motor_selected == 'Motor 2':
            self.motor = self.motor2
        else:
            self.motor = self.motor1

    def connect(self):
        if self.pi.get_connected():
            logging.info(f"{self.connect.__qualname__} not done. The controller is connected already.")
        else:
            self.pi.connect()
            for motor in self.motor_list:
                # All motors need to be enabled and commuted to be used.
                self.pi.enable(motor)
                self.pi.commut(self.motor)

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

    # In order to set the position at main, the instance function has to be returned
    def set_position(self):
        return self.pi.property_position.set_position

    # In order to set the distance at main, the instance function has to be returned
    def set_distance(self):
        return self.pi.property_distance.set_distance

    # The validation if the controller is connected is done here, without decorators.
    # It is done in this way to avoid returning back confusing values to PyQt5 indicator due to Decorators.
    def get_position(self):
        if self.pi.get_connected():
            return self.pi.get_position(self.motor)
        else:
            return None

    def get_connected(self):
        return self.pi.get_connected()

    def get_moving(self):
        if self.pi.get_connected():
            # Getting binary number to check the moving state of the motor.
            # [-6] is the position of the moving state bit.
            motor_state = self.pi.get_motor_state(self.motor)
            moving_motor_state = str(bin(motor_state))[-6]
            moving = moving_motor_state == '1'
            return moving
        else:
            return False
