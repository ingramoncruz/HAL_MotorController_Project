import time
import logging
import clr
clr.AddReference('C:\Program Files (x86)\ACS Motion Control\CommonFiles\ACS.SPiiPlusNET')
from ACS.SPiiPlusNET import *
from threading import Thread, Event
import sys
from PyQt5 import QtWidgets, uic
from MainWindow import Ui_MainWindow


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




class Manual_Control():
    def __init__(self):
        self.Ch = Api()
        self.port = int(EthernetCommOption.ACSC_SOCKET_STREAM_PORT)
        self.Axis = Axis.ACSC_AXIS_0
        self.event_Stop = Event()
        self.Connect()

    @Error_Handler
    def Connect(self):
        self.Ch.OpenCommEthernetTCP("172.22.112.1", self.port)
        self.Ch.Enable(self.Axis)
        self.Ch.WaitMotorEnabled(self.Axis, 1, 5000)
        self.Ch.Commut(self.Axis)


    @Error_Handler
    def Move_Relative(self):
        self.Ch.ToPoint(MotionFlags.ACSC_AMF_RELATIVE, self.Axis, 30)


    @Error_Handler
    def Stop_Motion(self):
        self.Ch.Halt(self.Axis)


    def Get_Position(self, Position):
        self.Position = Position
        while not self.event_Stop.is_set():
            self.Position(self.Ch.GetFPosition(self.Axis))
            time.sleep(0.2)

    @Error_Handler
    def Disconnect(self):
        self.Ch.CloseComm()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.Motors = Manual_Control()
        self.ButtonMoveRelativeNegative.released.connect(self.Motors.Move_Relative)
        self.ButtonStop.released.connect(self.Motors.Stop_Motion)
        thread_Get_Position = Thread(target=self.Motors.Get_Position, args=(self.DisplayPosition.display,))
        thread_Get_Position.start()



app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
window.Motors.event_Stop.set()
window.Motors.Disconnect()
