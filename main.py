from source.controller_hal.pi_controller.pi_controller_api import *
from source.user_interfaces.main_window import *
import sys
from threading import Thread, Event
import time
Example() # This is just a class called by a module from other module in different packages at runtime


def Get_Position(*args):
    Read_Position = args[0]
    Event = args[1]
    Indicator_Function = args[2]
    while not Event.is_set():
        Indicator_Function(Read_Position())
        time.sleep(0.2)
    return


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.event_Stop = Event()
        self.Motors = PiControllerApi()
        self.Motors.Connect()
        self.Motors.Enable()
        self.Motors.Commut()
        self.Button_MoveRelativePositive.released.connect(self.Motors.Move_Relative)
        self.Button_Stop.released.connect(self.Motors.Stop_Motion)
        thread_Get_Position = Thread(target=Get_Position, args=(self.Motors.Get_Position, self.event_Stop, self.Indicator_Position.display,))
        thread_Get_Position.start()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
window.event_Stop.set()
window.Motors.Disable()
window.Motors.Disconnect()
