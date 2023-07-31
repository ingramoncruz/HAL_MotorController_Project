"""
This is the main class with all the methods for sending the correct commands to the PI Controller.
"""

import clr
import configparser
import logging
import sys
clr.AddReference('C:\Program Files (x86)\ACS Motion Control\CommonFiles\ACS.SPiiPlusNET')
from ACS.SPiiPlusNET import *


logging.basicConfig(
    level = logging.INFO,
    format = '%(threadName)s-%(levelname)s-%(message)s'
)


def error_handler(method):
    def wrapper(*args, **kwargs):
        try:
            method(*args, **kwargs)
        except:
            logging.error(f"Error in {method.__qualname__}")
        else:
            logging.info(f"{method.__qualname__} completed successfully.")
    return wrapper


def read_ini_file(path):
    inifile_path = path + '\config\pi_motor_config.ini'
    config = configparser.ConfigParser()
    config.read(inifile_path)
    return config['General']['IP Address']


class PropertyDistance():
    def __init__(self):
        self._distance = 0


    def get_distance(self):
        return self._distance


    def set_distance(self, value):
        self._distance = value


#Unable to use @property with PyQT5, so I need it to use the normal getter and setter.
class PropertyPosition():
    def __init__(self):
        self._position = 0


    def get_position(self):
        return self._position


    def set_position(self, value):
        self._position = value


class PiControllerApi():
    def __init__(self):
        self.property_distance = PropertyDistance()
        self.property_position = PropertyPosition()
        self.command = Api()
        self.port = int(EthernetCommOption.ACSC_SOCKET_STREAM_PORT)
        self.__connected = False
        self.axis = Axis.ACSC_AXIS_0


    def get_connected(self):
        return self.__connected


    def __CheckConnection(method):
        def wrapper(self):
            if self.get_connected():
                return method(self)
        return wrapper


    @error_handler
    def connect(self):
        if self.get_connected():
            logging.info("Command not sent because system is already Connected.")
        else:
            self.command.OpenCommEthernetTCP(ip_address, self.port)
            self.__connected = True
            self.enable()
            self.commut()


    @__CheckConnection
    def enable(self):
        self.command.Enable(self.axis)


    @error_handler
    @__CheckConnection
    def disable(self):
        self.command.DisableAll()


    @error_handler
    def wait_enable(self):
        self.command.WaitMotorEnabled(self.axis, 1, 5000)


    @__CheckConnection
    def commut(self):
        self.command.Commut(self.axis)


    @error_handler
    @__CheckConnection
    def move_relative_positive(self):
        self.command.ToPoint(MotionFlags.ACSC_AMF_RELATIVE, self.axis, self.property_distance.get_distance())


    @error_handler
    @__CheckConnection
    def move_relative_negative(self):
        self.command.ToPoint(MotionFlags.ACSC_AMF_RELATIVE, self.axis, -abs(self.property_distance.get_distance()))


    @error_handler
    @__CheckConnection
    def move_absolute(self):
        self.command.ToPoint(MotionFlags.ACSC_NONE, self.axis, self.property_position.get_position())


    @error_handler
    @__CheckConnection
    def stop_motion(self):
        self.command.Halt(self.axis)


    @__CheckConnection
    def get_position(self):
        return self.command.GetFPosition(self.axis)


    @error_handler
    def disconnect(self):
        self.disable()
        self.command.CloseComm()
        self.__connected = False


if __name__ == '__main__':
    import os
    PROJECT_PATH = (os.path.split(os.path.split(os.path.split(sys.path[0])[0])[0])[0]) # Obtaining root path of Project in folder HAL_MotorController
    sys.path.insert(0, PROJECT_PATH) # Adding the config folder to python path so it can be imported any module
    from source.controller_hal.hal_controller import *

    ip_address = read_ini_file(PROJECT_PATH)

    api = PiControllerApi()
    api.connect()
    api.enable()
    api.disconnect()
else:
    from ...modtest import *
    PROJECT_PATH = sys.path[0]
    ip_address = read_ini_file(PROJECT_PATH)
