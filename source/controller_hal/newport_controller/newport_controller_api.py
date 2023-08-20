""" This is the main class with all the methods for sending the correct commands to the Newport
Controller. Don't forget to update the ip_address value at the Config.ini at
HAL_MotorController\config path.
The IP Address is 192.168.0.254 when connected to HOST, and 192.168.254.254 when connected to
REMOTE port in the controller.
"""
import clr
import logging
import sys
import time
# Relative imports
from ..utils.decorators import error_handler, check_connection
from ..utils.functions import read_ip_address
from ..utils.properties import PropertyPosition, PropertyDistance, PropertyConnection
# Relative import .NET dll for Newport Controller
sys.path.append(r'C:\Windows\Microsoft.NET\assembly\GAC_64\Newport.XPS.CommandInterface\v4.0_2.3.0.0__9a267756cf640dcf')
clr.AddReference("Newport.XPS.CommandInterface")
from CommandInterfaceXPS import *


logging.basicConfig(
    level = logging.INFO,
    format = '%(threadName)s-%(levelname)s-%(message)s')


project_path = sys.path[0]  # Getting the project path
INI_PATH = '\config\_newport_motor_config.ini'
ip_address = read_ip_address(project_path, INI_PATH)


class NewportControllerApi(PropertyDistance, PropertyPosition, PropertyConnection):
    """Class with the methods which connects with all the .dll methods of the .NET api
    from Newport controller.
    """
    def __init__(self, distance, position):
        # Initializing 3 instances of the XPS class to be able to read position and check moving
        # status in different threads.
        """Current Result: The instances implementation doesn't solve the thread problem"""
        self.command = XPS()
        self.socket_position = XPS()
        self.socket_moving = XPS()
        self.distance = distance
        self.position = position
        self.port = 5001
        self._connected = False
        # Paramaters used as inputs to send commands properly to the newport controller
        # They don't need specific values, they work as placeholders
        self.GetPosition = [0.0]
        self.errstring = ""
        self.status = [0]

    # Newports Controller Methods
    def connect(self):
        # Need to connect in all XPS instances created.
        self.command.OpenInstrument(ip_address, self.port, 10000)
        self.socket_position.OpenInstrument(ip_address, self.port, 10000)
        self.socket_moving.OpenInstrument(ip_address, self.port, 10000)
        logging.info(f"Controller connected with IP Address = {ip_address} and Port = {self.port}.")

    @error_handler
    def disconnect(self):
        # Need to disconnect in all XPS instances created.
        self.connection = False
        self.command.CloseInstrument()
        self.socket_position.CloseInstrument()
        self.socket_moving.CloseInstrument()
        logging.info("Controller disconnected.")

    @error_handler
    def initialize(self, group_name):
        self.command.GroupInitialize(group_name)
        logging.info(f"Group of motors = {group_name} initialized.")

    @error_handler
    def home(self, group_name):
        self.command.GroupHomeSearch(group_name)
        logging.info(f"Group of motors = {group_name} homed.")

    @error_handler
    @check_connection
    def kill(self, group_name):
        self.command.GroupKill(group_name)
        logging.info(f"Group of motors = {group_name} killed.")

    @error_handler
    @check_connection
    def group_disable(self, group_name):
        self.command.GroupMotionDisable(group_name)
        logging.info(f"Group of motors = {group_name} disabled.")

    def get_motor_state(self, group_name):
        result = self.socket_moving.GroupMotionStatusGet(group_name, self.status, 1, self.errstring)[1].GetValue(0)
        return result

    def get_position(self, group_name):
        return self.socket_position.GroupPositionCurrentGet(group_name, self.GetPosition, 1, self.errstring)[1].GetValue(0)

    @error_handler
    @check_connection
    def stop_motion(self, group_name):
        self.socket_moving.GroupMoveAbort(group_name)
        logging.info(f"Motion stopped in Group = {group_name}.")

    def set_velocity_acceleration(self, positioner, velocity, acceleration):
        self.command.PositionerSGammaVelocityAndAccelerationSet(positioner, velocity, acceleration)
        logging.info(f"Velocity = {velocity} and acceleration = {acceleration} set for positioner = {positioner}.")

    @error_handler
    @check_connection
    def move_absolute(self, positioner):
        self.command.GroupMoveAbsolute(positioner, [self.position], 1)
        logging.info(f"Absolute move in Positioner = {positioner} to Position = {self.position}.")

    @error_handler
    @check_connection
    def move_relative_negative(self, positioner):
        self.command.GroupMoveRelative(positioner, [-abs(self.distance)], 1)
        logging.info(f"Positive relative move in Positioner = {positioner} for Distance = {-abs(self.distance)}.")

    @error_handler
    @check_connection
    def move_relative_positive(self, positioner):
        self.command.GroupMoveRelative(positioner, [self.distance], 1)
        logging.info(f"Positive relative move in Positioner = {positioner} for Distance = {self.distance}.")
