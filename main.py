from source.controller_hal.pi_controller.hal_pi_controller import *
from source.user_interfaces.main_window import *
import sys
from threading import Thread, Event
import time


def function_get_position(*args):
    """This function is activated by a Thread to continuously adquire the current position
    of the axis set. It is shutdown before closing the app.
    """
    # Unwrapping the tuple args
    event, display_indicator, method = args
    while not event.is_set():
        display_indicator(method())
        time.sleep(0.3)
    return


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """ This is the main class which suppots all the user interface for the App, and connects
    everything with the hal controller to be used with the app.
    """
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.event_stop = Event()
        self.motors = PiHalClass()
        # The hal pi function is called to receive the set_position instance function
        self.Input_Position.valueChanged.connect(self.motors.set_position())
        # The hal pi function is called to receive the set_distance instance function
        self.Input_Distance.valueChanged.connect(self.motors.set_distance())
        self.Button_MoveRelativePositive.released.connect(self.motors.move_relative_positive)
        self.Button_MoveRelativeNegative.released.connect(self.motors.move_relative_negative)
        self.Button_MoveAbsolute.released.connect(self.motors.move_absolute)
        self.Button_Stop.released.connect(self.motors.stop_motion)
        self.Button_Connect.released.connect(self.motors.connect)
        self.Button_Disconnect.released.connect(self.motors.disconnect)
        self.thread_get_position = Thread(
            target=function_get_position,
            args=(self.event_stop, self.Indicator_Position.display, self.motors.get_position,))
        self.thread_get_position.start()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
window.event_stop.set()  # Stopping the while loop in function_get_position()
window.motors.disconnect()  # The controller is disconnected in case the user forgets to do it.
