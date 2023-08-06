""" This is the main class with all the methods for sending the correct commands to the PI
Controller. Don't forget to update the ip_address value at the Config.ini at
HAL_MotorController\config path.
The IP Address is provided after you Connect the simulator, and then you Connect the Ethernet Comm
The .NET dll used here is set at the specific path after installing the SPiiPlus-ADK-Suite.
"""
import clr
import configparser
import logging
import sys
# Relative import .NET dll for PI Controller
clr.AddReference('C:\Program Files (x86)\ACS Motion Control\CommonFiles\ACS.SPiiPlusNET')
from ACS.SPiiPlusNET import *


logging.basicConfig(
    level = logging.INFO,
    format = '%(threadName)s-%(levelname)s-%(message)s')


def error_handler(method):
    """Decorator function to check if the method is runnable."""
    def wrapper(*args, **kwargs):
        try:
            method(*args, **kwargs)
        except:
            logging.error(f"Error in {method.__qualname__}")
    return wrapper


def read_ini_file(path):
    """Function to read the IP Address at the Config.ini file"""
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
    """Class with the methods which connects with all the .dll methods of the .NET api
    from PI controller.
    """
    def __init__(self):
        self.property_distance = PropertyDistance()
        self.property_position = PropertyPosition()
        self.command = Api()
        self.port = int(EthernetCommOption.ACSC_SOCKET_STREAM_PORT)
        self.__connected = False
        self.distance = 0

    # Public method to read private method __connected.
    def get_connected(self):
        return self.__connected

    # Decorators to be used here in this class
    def __check_connection(method):
        """Decorator to check if the controller is connected, if so, it runs the method"""
        def wrapper(*args):
            self = args[0]
            if self.get_connected():
                return method(*args)
            else:
                logging.info(f"Action in {method.__qualname__} not done, because you are not connected.")
        return wrapper

    def __get_attribute_axis(method):
        """Decorator to set the correct axis attribute from Axis object"""
        def wrapper(*args):
            self = args[0]
            axis = getattr(Axis, args[1])
            return method(self, axis)
        return wrapper


    # PI Controller Methods
    @error_handler
    def connect(self):
        self.command.OpenCommEthernetTCP(ip_address, self.port)
        self.__connected = True
        logging.info(f"Controller connected with IP Address = {ip_address} and Port = {self.port}.")

    @error_handler
    @__get_attribute_axis
    @__check_connection
    def enable(self, axis):
        self.command.Enable(axis)
        logging.info(f"Axis = {axis} enabled.")

    @error_handler
    @__check_connection
    def disable(self):
        self.command.DisableAll()
        logging.info("All axis disabled")

    @error_handler
    @__get_attribute_axis
    @__check_connection
    def commut(self, axis):
        self.command.Commut(axis)
        logging.info(f"Axis = {axis} commuted.")

    @error_handler
    @__get_attribute_axis
    @__check_connection
    def move_relative_positive(self, axis):
        self.distance = self.property_distance.get_distance()
        self.command.ToPoint(MotionFlags.ACSC_AMF_RELATIVE, axis, self.distance)
        logging.info(f"Positive relative move in Axis = {axis} for Distance = {self.distance}.")

    @error_handler
    @__get_attribute_axis
    @__check_connection
    def move_relative_negative(self, axis):
        self.distance = -abs(self.property_distance.get_distance())
        self.command.ToPoint(MotionFlags.ACSC_AMF_RELATIVE, axis, self.distance)
        logging.info(f"Negative relative move in Axis = {axis} for Distance = {self.distance}.")

    @error_handler
    @__get_attribute_axis
    @__check_connection
    def move_absolute(self, axis):
        position = self.property_position.get_position()
        self.command.ToPoint(MotionFlags.ACSC_NONE, axis, position)
        logging.info(f"Absolute move in Axis = {axis} to Position = {position}.")

    @error_handler
    @__get_attribute_axis
    @__check_connection
    def stop_motion(self, axis):
        self.command.Halt(axis)
        logging.info(f"Motion stopped in Axis = {axis}.")

    @__get_attribute_axis
    def get_position(self, axis):
        return self.command.GetFPosition(axis)

    @__get_attribute_axis
    def get_motor_state(self, axis):
        motor_state = self.command.GetMotorState(axis)
        return motor_state

    @error_handler
    def disconnect(self):
        self.__connected = False
        self.command.CloseComm()
        logging.info("Controller disconnected.")


# In case of running this specific .py file for Unit Test, we obtain the imports in a different way.
if __name__ == '__main__':
    import os
    # Getting root path of Project in folder HAL_MotorController
    PROJECT_PATH = (os.path.split(os.path.split(os.path.split(sys.path[0])[0])[0])[0])
    ip_address = read_ini_file(PROJECT_PATH)
    api = PiControllerApi()
    axis = 'ACSC_AXIS_0'
    api.connect()
    api.enable(axis)
    api.disconnect()
else:
    PROJECT_PATH = sys.path[0]  # Getting the project path
    ip_address = read_ini_file(PROJECT_PATH)
