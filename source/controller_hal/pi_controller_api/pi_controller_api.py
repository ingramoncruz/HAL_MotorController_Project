"""
This is the main class with all the methods for sending the correct commands to the PI Controller.
"""
import configparser
import os
import sys
import clr
clr.AddReference('C:\Program Files (x86)\ACS Motion Control\CommonFiles\ACS.SPiiPlusNET')
from ACS.SPiiPlusNET import *

root_path=(os.path.split(os.path.split(os.path.split(sys.path[0])[0])[0])[0]) # Obtaining root path of Project in folder HAL_MotorController
# sys.path.insert(0, root_path + '\config') # Adding the config folder to python path so it can be imported any module

inifile_path = root_path + '\config\pi_motor_config.ini'
config = configparser.ConfigParser()
config.read(inifile_path)
Ip_Address = config['General']['IP Address']


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


    def Connect(self):
        self.Command.OpenCommEthernetTCP(Ip_Address, self.port)


    def Enable(self):
        self.Command.Enable(self.Axis)


    def Wait_for_Enable():
        self.Command.WaitMotorEnabled(self.Axis, 1, 5000)


    def Commut():
        self.Command.Commut(self.Axis)


    def Move_Relative(self):
        self.Command.ToPoint(MotionFlags.ACSC_AMF_RELATIVE, self.Axis, 30)


    def Stop_Motion(self):
        self.Command.Halt(self.Axis)


    def Get_Position(self):
            self.Position(self.Command.GetFPosition(self.Axis))


    def Disconnect(self):
        self.Command.CloseComm()


if __name__ == '__main__':
    api = PiControllerApi()
    api.Connect()
    api.Enable()
    api.Disconnect()
