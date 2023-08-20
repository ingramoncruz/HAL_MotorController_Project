""" This is the main class with all the methods for sending the correct commands to the PI
Controller. Don't forget to update the ip_address value at the Config.ini at
HAL_MotorController\config path.
The IP Address is provided after you Connect the simulator, and then you Connect the Ethernet Comm
The .NET dll used here is set at the specific path after installing the SPiiPlus-ADK-Suite.
"""
import clr
import logging
import sys
# Relative imports
from ..utils.decorators import error_handler, check_connection
from ..utils.functions import read_ip_address
from ..utils.properties import PropertyPosition, PropertyDistance
# Relative import .NET dll for PI Controller
clr.AddReference('C:\Program Files (x86)\ACS Motion Control\CommonFiles\ACS.SPiiPlusNET')
from ACS.SPiiPlusNET import *


logging.basicConfig(
    level = logging.INFO,
    format = '%(threadName)s-%(levelname)s-%(message)s')


project_path = sys.path[0]  # Getting the project path
INI_PATH = '\config\pi_motor_config.ini'
ip_address = read_ip_address(project_path, INI_PATH)


class PiControllerApi(PropertyPosition, PropertyDistance):
    """Class with the methods which connects with all the .dll methods of the .NET api from PI
    controller."""
    def __init__(self, distance, position):
        self.distance = distance
        self.position = position
        self.command = Api()
        self.port = int(EthernetCommOption.ACSC_SOCKET_STREAM_PORT)
        self.__connected = False

    @property
    def connection(self):
        return self.__connected

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
    @check_connection
    def enable(self, axis):
        self.command.Enable(axis)
        logging.info(f"Axis = {axis} enabled.")

    @error_handler
    @check_connection
    def disable(self):
        self.command.DisableAll()
        logging.info("All axis disabled")

    @error_handler
    @__get_attribute_axis
    @check_connection
    def commut(self, axis):
        self.command.Commut(axis)
        logging.info(f"Axis = {axis} commuted.")

    @error_handler
    @__get_attribute_axis
    @check_connection
    def move_relative_positive(self, axis):
        self.command.ToPoint(MotionFlags.ACSC_AMF_RELATIVE, axis, self.distance)
        logging.info(f"Positive relative move in Axis = {axis} for Distance = {self.distance}.")

    @error_handler
    @__get_attribute_axis
    @check_connection
    def move_relative_negative(self, axis):
        self.command.ToPoint(MotionFlags.ACSC_AMF_RELATIVE, axis, -abs(self.distance))
        logging.info(f"Negative relative move in Axis = {axis} for Distance = {-abs(self.distance)}.")

    @error_handler
    @__get_attribute_axis
    @check_connection
    def move_absolute(self, axis):
        self.command.ToPoint(MotionFlags.ACSC_NONE, axis, self.position)
        logging.info(f"Absolute move in Axis = {axis} to Position = {self.position}.")

    @error_handler
    @__get_attribute_axis
    @check_connection
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
