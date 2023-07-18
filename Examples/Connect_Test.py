import time
import logging
import clr
clr.AddReference('C:\Program Files (x86)\ACS Motion Control\CommonFiles\ACS.SPiiPlusNET')
from ACS.SPiiPlusNET import *
from threading import Thread, Lock

logging.basicConfig(
    level = logging.INFO,
    format = '%(threadName)s-%(levelname)s-%(message)s'
)

class Manual_Control:
    def __init__(self):
        self.Ch = Api()
        port = int(EthernetCommOption.ACSC_SOCKET_STREAM_PORT)
        self.Ch.OpenCommEthernetTCP("172.29.80.1", port)
        self.Axis = Axis.ACSC_AXIS_0
        self.Ch.Enable(self.Axis)
        self.Ch.WaitMotorEnabled(self.Axis, 1, 5000)
        self.Ch.Commut(self.Axis)


    def Move_Relative(self):
        self.Ch.ToPoint(MotionFlags.ACSC_AMF_RELATIVE, self.Axis, 30)
        self.Ch.WaitMotionEnd(self.Axis, -1)
        logging.info('Relative Position Reached')

    def Stop_Motion(self):
        stop_indicator = input('If you wanna stop the move, send "y", if not, press enter and wait for being finished.')
        if stop_indicator == "y":
            self.Ch.Halt(self.Axis)
            print('Manual Stop')

    def Disconnect(self):
        try:
            self.Ch.CloseComm()
        except:
            print("Coudn't close the comm.")
        else:
            print('Disconnected')


control = Manual_Control()

thread_command_loop = Thread(target=control.Move_Relative)
thread_stop_loop = Thread(target=control.Stop_Motion)


thread_command_loop.start()
thread_stop_loop.start()


thread_command_loop.join()
thread_stop_loop.join()

control.Disconnect()
