from source.controller_hal.pi_controller.pi_controller_api import *
from source.user_interfaces.main_window import *
import sys
from threading import Thread, Event
import time


def function_get_position(self):
    while not self.event_stop.is_set():
        self.Indicator_Position.display(self.motors.get_position())
        time.sleep(0.3)
    return


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.event_stop = Event()
        self.motors = PiControllerApi()
        self.Input_Position.valueChanged.connect(self.motors.property_position.set_position)
        self.Input_Distance.valueChanged.connect(self.motors.property_distance.set_distance)
        self.Button_MoveRelativePositive.released.connect(self.motors.move_relative_positive)
        self.Button_MoveRelativeNegative.released.connect(self.motors.move_relative_negative)
        self.Button_MoveAbsolute.released.connect(self.motors.move_absolute)
        self.Button_Stop.released.connect(self.motors.stop_motion)
        self.Button_Connect.released.connect(self.motors.connect)
        self.Button_Disconnect.released.connect(self.motors.disconnect)
        self.thread_get_position = Thread(
            target=function_get_position,
            args=(self,))
        self.thread_get_position.start()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
window.event_stop.set()
window.motors.disconnect()
