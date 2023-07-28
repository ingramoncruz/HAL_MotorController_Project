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


def Error_Handler(Method):
    def Wrapper(*args, **kwargs):
        try:
            Method(*args, **kwargs)
        except TypeError:
            logging.error(f"Error in {Method.__qualname__}")
        else:
            logging.info(f"{Method.__qualname__} completed successfully.")
    return Wrapper



class PiControllerApi():
    def __init__(self):
        self.Command = Api()
        self.port = int(EthernetCommOption.ACSC_SOCKET_STREAM_PORT)
        self.Axis = Axis.ACSC_AXIS_0
        self.Axes = [
            Axis.ACSC_AXIS_0, Axis.ACSC_AXIS_1, Axis.ACSC_AXIS_2, Axis.ACSC_AXIS_3, Axis.ACSC_AXIS_4,
            Axis.ACSC_AXIS_5, Axis.ACSC_AXIS_6, Axis.ACSC_AXIS_7, Axis.ACSC_AXIS_8, Axis.ACSC_AXIS_9,
            Axis.ACSC_AXIS_10, Axis.ACSC_AXIS_11, Axis.ACSC_AXIS_12, Axis.ACSC_AXIS_13, Axis.ACSC_AXIS_14,
            Axis.ACSC_AXIS_15, Axis.ACSC_AXIS_16, Axis.ACSC_AXIS_17, Axis.ACSC_AXIS_18, Axis.ACSC_AXIS_19
            #Axis.ACSC_NONE -> No Axis selected
            #Axis.ACSC_PAR_ALL -> All axes selected
        ]

    @Error_Handler
    def Connect(self):
        self.Command.OpenCommEthernetTCP(Ip_Address, self.port)


    @Error_Handler
    def Enable(self):
        self.Command.Enable(self.Axis)


    @Error_Handler
    def Disable(self):
        self.Command.Disable(self.Axis)


    @Error_Handler
    def Wait_for_Enable(self):
        self.Command.WaitMotorEnabled(self.Axis, 1, 5000)


    @Error_Handler
    def Commut(self):
        self.Command.Commut(self.Axis)


    @Error_Handler
    def Move_Relative(self):
        self.Command.ToPoint(MotionFlags.ACSC_AMF_RELATIVE, self.Axis, 30)


    @Error_Handler
    def Stop_Motion(self):
        self.Command.Halt(self.Axis)


    def Get_Position(self):
        return self.Command.GetFPosition(self.Axis)


    @Error_Handler
    def Disconnect(self):
        self.Command.CloseComm()



def read_ini_file(PROJECT_PATH):
    inifile_path = PROJECT_PATH + '\config\pi_motor_config.ini'
    config = configparser.ConfigParser()
    config.read(inifile_path)
    return config['General']['IP Address']


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
