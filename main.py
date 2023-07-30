from source.controller_hal.pi_controller.pi_controller_api import *
from source.user_interfaces.main_window import *
import sys
from threading import Thread, Event
import time
Example() # This is just a class called by a module from other module in different packages at runtime


def Function_Get_Position(self):
    while not self.event_Stop.is_set():
        self.Indicator_Position.display(self.Motors.Get_Position())
        time.sleep(0.3)
    return


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.event_Stop = Event()
        self.Motors = PiControllerApi()
        self.Input_Position.valueChanged.connect(self.Motors.Property_Position.SetPosition)
        self.Input_Distance.valueChanged.connect(self.Motors.Property_Distance.SetDistance)
        self.Button_MoveRelativePositive.released.connect(self.Motors.Move_Relative_Positive)
        self.Button_MoveRelativeNegative.released.connect(self.Motors.Move_Relative_Negative)
        self.Button_MoveAbsolute.released.connect(self.Motors.Move_Absolute)
        self.Button_Stop.released.connect(self.Motors.Stop_Motion)
        self.Button_Connect.released.connect(self.Motors.Connect)
        self.Button_Disconnect.released.connect(self.Motors.Disconnect)
        self.thread_Get_Position = Thread(
            target=Function_Get_Position,
            args=(self,)
            )
        self.thread_Get_Position.start()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
window.event_Stop.set()
