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


def read_ini_file(PROJECT_PATH):
    inifile_path = PROJECT_PATH + '\config\pi_motor_config.ini'
    config = configparser.ConfigParser()
    config.read(inifile_path)
    return config['General']['IP Address']


def Error_Handler(Method):
    def Wrapper(*args, **kwargs):
        try:
            Method(*args, **kwargs)
        except ACSException:
            logging.error(f"Error in {Method.__qualname__}")
        else:
            logging.info(f"{Method.__qualname__} completed successfully.")
    return Wrapper


def Check_Connection(Method):
    Position = 0
    def Wrapper(self):
        if self.GetConnected():
            return Method(self)
    return Wrapper


class PropertyDistance():
    def __init__(self):
        self._Distance = 0


    def GetDistance(self):
        return self._Distance


    def SetDistance(self, value):
        self._Distance = value


#Unable to use @property with PyQT5, so I need it to use the normal getter and setter.
class PropertyPosition():
    def __init__(self):
        self._Position = 0


    def GetPosition(self):
        return self._Position


    def SetPosition(self, value):
        self._Position = value


class PiControllerApi():
    def __init__(self):
        self.Property_Distance = PropertyDistance()
        self.Property_Position = PropertyPosition()
        # self.Property_Connected = PropertyConnected()
        self.Command = Api()
        self.port = int(EthernetCommOption.ACSC_SOCKET_STREAM_PORT)
        self._Connected = False
        self.Axis = Axis.ACSC_AXIS_0
        self.Axes = [
            Axis.ACSC_AXIS_0, Axis.ACSC_AXIS_1
            #Axis.ACSC_NONE -> No Axis selected
            #Axis.ACSC_PAR_ALL -> All axes selected
        ]


    def GetConnected(self):
        return self._Connected


    @Error_Handler
    def Connect(self):
        if self._Connected:
            pass
        else:
            self.Command.OpenCommEthernetTCP(Ip_Address, self.port)
            self.Enable()
            self.Commut()
            self._Connected = True


    @Error_Handler
    @Check_Connection
    def Enable(self):
        self.Command.Enable(self.Axis)


    @Error_Handler
    @Check_Connection
    def Disable(self):
        self.Command.Disable(self.Axis)


    @Error_Handler
    def Wait_for_Enable(self):
        self.Command.WaitMotorEnabled(self.Axis, 1, 5000)


    @Error_Handler
    @Check_Connection
    def Commut(self):
        self.Command.Commut(self.Axis)


    @Error_Handler
    @Check_Connection
    def Move_Relative_Positive(self):
        self.Command.ToPoint(MotionFlags.ACSC_AMF_RELATIVE, self.Axis, self.Property_Distance.GetDistance())



    @Error_Handler
    @Check_Connection
    def Move_Relative_Negative(self):
        self.Command.ToPoint(MotionFlags.ACSC_AMF_RELATIVE, self.Axis, -abs(self.Property_Distance.GetDistance()))


    @Error_Handler
    @Check_Connection
    def Move_Absolute(self):
        self.Command.ToPoint(MotionFlags.ACSC_NONE, self.Axis, self.Property_Position.GetPosition())


    @Error_Handler
    @Check_Connection
    def Stop_Motion(self):
        self.Command.Halt(self.Axis)

    @Check_Connection
    def Get_Position(self):
        return self.Command.GetFPosition(self.Axis)


    @Error_Handler
    def Disconnect(self):
        self.Command.CloseComm()
        self._Connected = False



if __name__ == '__main__':
    import os
    PROJECT_PATH = (os.path.split(os.path.split(os.path.split(sys.path[0])[0])[0])[0]) # Obtaining root path of Project in folder HAL_MotorController
    sys.path.insert(0, PROJECT_PATH) # Adding the config folder to python path so it can be imported any module
    from source.controller_hal.hal_controller import *

    Ip_Address = read_ini_file()

    api = PiControllerApi()
    api.Connect()
    api.Enable()
    api.Disconnect()

else:
    from ...modtest import *
    PROJECT_PATH = sys.path[0]
    Ip_Address = read_ini_file(PROJECT_PATH)
