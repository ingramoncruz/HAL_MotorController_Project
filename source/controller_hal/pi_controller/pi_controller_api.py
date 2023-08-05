"""
This is the main class with all the methods for sending the correct commands to the PI Controller.
Don't forget to update the ip_address value at the Config.ini at HAL_MotorController\config path.
The IP Address is provided after you Connect the simulator, and then you Connect the Ethernet Comm
"""

import clr
import configparser
import logging
import sys
clr.AddReference('C:\Program Files (x86)\ACS Motion Control\CommonFiles\ACS.SPiiPlusNET')
from ACS.SPiiPlusNET import *


logging.basicConfig(
    level = logging.INFO,
    format = '%(threadName)s-%(levelname)s-%(message)s')


def error_handler(method):
    """Decorator function to check if the method is runnable, returns success/fail message."""
    def wrapper(*args, **kwargs):
        try:
            method(*args, **kwargs)
        except:
            logging.error(f"Error in {method.__qualname__}")
    return wrapper


def read_ini_file(path):
    """Function to read all the parameters at the Config.ini file"""
    inifile_path = path + '\config\pi_motor_config.ini'
    config = configparser.ConfigParser()
    config.read(inifile_path)
    return config['General']['IP Address']


class PropertyDistance():
    """Property class to read the _distance value given by the
    inputDistant controller in the user interface. This is done without
    the usage of @property because PyQt5 does not recognize it when
    trying to set the distance value.
    """
    def __init__(self):
        self._distance = 0

    def get_distance(self):
        return self._distance

    def set_distance(self, value):
        self._distance = value


class PropertyPosition():
    """Property class to read the _position value given by the
    inputPosition controller in the user interface. This is done without
    the usage of @property because PyQt5 does not recognize it when
    trying to set the position value.
    """
    def __init__(self):
        self._position = 0

    def get_position(self):
        return self._position

    def set_position(self, value):
        self._position = value


class PiControllerApi():
    """Class with the methods which connects with all the .dll methods
    of the .NET api from PI controller.
    """
    def __init__(self):
        self.property_distance = PropertyDistance()
        self.property_position = PropertyPosition()
        self.command = Api()
        self.port = int(EthernetCommOption.ACSC_SOCKET_STREAM_PORT)
        self.__connected = False
        self.axis = Axis.ACSC_AXIS_0
        self.MOVING = MotorStates.ACSC_MST_MOVE
        self.distance = 0

    def get_connected(self):
        return self.__connected

    def __check_connection(method):
        """Decorator to check if the controller is connected, if so, runs the method"""
        def wrapper(self):
            if self.get_connected():
                return method(self)
            else:
                logging.info(f"Action in {method.__qualname__} not done, because you are not connected.")
        return wrapper

    @error_handler
    def connect(self):
        self.command.OpenCommEthernetTCP(ip_address, self.port)
        self.__connected = True
        logging.info(f"Controller connected with IP Address = {ip_address} and Port = {self.port}.")

    @error_handler
    @__check_connection
    def enable(self):
        self.command.Enable(self.axis)
        logging.info(f"Axis = {self.axis} enabled.")

    @error_handler
    @__check_connection
    def disable(self):
        self.command.DisableAll()
        logging.info("All axis disabled")

    @error_handler
    @__check_connection
    def wait_enable(self):
        self.command.WaitMotorEnabled(self.axis, 1, 5000)
        logging.info(f"Axis = {self.axis} enabled.")

    @error_handler
    @__check_connection
    def commut(self):
        self.command.Commut(self.axis)
        logging.info(f"Axis = {self.axis} commuted.")

    @error_handler
    @__check_connection
    def move_relative_positive(self):
        self.distance = self.property_distance.get_distance()
        self.command.ToPoint(MotionFlags.ACSC_AMF_RELATIVE, self.axis, self.distance)
        logging.info(f"Positive relative move in Axis = {self.axis} for Distance = {self.distance}.")

    @error_handler
    @__check_connection
    def move_relative_negative(self):
        self.distance = -abs(self.property_distance.get_distance())
        self.command.ToPoint(MotionFlags.ACSC_AMF_RELATIVE, self.axis, self.distance)
        logging.info(f"Negative relative move in Axis = {self.axis} for Distance = {self.distance}.")

    @error_handler
    @__check_connection
    def move_absolute(self):
        position = self.property_position.get_position()
        self.command.ToPoint(MotionFlags.ACSC_NONE, self.axis, position)
        logging.info(f"Absolute move in Axis = {self.axis} to Position = {position}.")

    @error_handler
    @__check_connection
    def stop_motion(self):
        self.command.Halt(self.axis)
        logging.info(f"Motion stopped in Axis = {self.axis}.")

    # Decorator cannot be applied here to get a proper returned value to the main.py file
    def get_position(self):
        return self.command.GetFPosition(self.axis)

    @error_handler
    def disconnect(self):
        self.__connected = False
        self.command.CloseComm()
        logging.info("Controller disconnected.")

    # Decorator cannot be applied here to get a proper returned value to the main.py file
    def get_motor_state(self):
        motor_state = self.command.GetMotorState(self.axis)
        return motor_state


# In case of running this specific .py file, we obtain the imports in a different way.
if __name__ == '__main__':
    import os
    PROJECT_PATH = (os.path.split(os.path.split(os.path.split(sys.path[0])[0])[0])[0])  # Obtaining root path of Project in folder HAL_MotorController
    sys.path.insert(0, PROJECT_PATH)  # Adding the config folder to python path so it can be imported any module
    from source.controller_hal.hal_controller import *

    ip_address = read_ini_file(PROJECT_PATH)

    api = PiControllerApi()
    api.connect()
    api.enable()
    api.disconnect()
else:
    PROJECT_PATH = sys.path[0]  # Getting the project path
    ip_address = read_ini_file(PROJECT_PATH)
