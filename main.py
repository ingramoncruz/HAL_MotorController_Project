""" This is the main.py which starts all the modules to be controlled or used in the user
interface provided and created in PyQt5.
"""
import sys
from threading import Thread, Event
import time
# Relative import for the modules to be used.
from source.controller_hal.pi_controller.hal_pi_controller import *
from source.user_interfaces.main_window import *


def function_indicators(self):
    """This function is activated by a Thread to continuously adquire the current position
    of the axis set. It is shutdown before closing the app.
    """
    event = self.event_stop
    while not event.is_set():
        # The function needs to be called to pass that data in the indicators (slots)
        self.ledConnected.setChecked(self.motors.get_connected())
        self.ledMoving.setChecked(self.motors.get_moving())
        self.indicatorPosition.display(self.motors.get_position())
        time.sleep(0.1)
    return


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """ This is the main class which suppots all the user interface for the App, and connects
    everything with the hal controller to be used with the app.
    """
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.event_stop = Event()
        self.motors = PiHalClass()
        self.selectMotor.addItems(['Motor 1', 'Motor 2'])
        # Connecting all controllers (signals) with their respective methods.
        self.inputPosition.valueChanged.connect(self.motors.set_position())  # Calling function to insert input from signal
        self.inputDistance.valueChanged.connect(self.motors.set_distance())  # Calling function to insert input from signal
        self.selectMotor.currentTextChanged.connect(self.motors.motor_select)
        self.buttonMoveRelativePositive.released.connect(self.motors.move_relative_positive)
        self.buttonMoveRelativeNegative.released.connect(self.motors.move_relative_negative)
        self.buttonMoveAbsolute.released.connect(self.motors.move_absolute)
        self.buttonStop.released.connect(self.motors.stop_motion)
        self.buttonConnect.released.connect(self.motors.connect)
        self.buttonDisconnect.released.connect(self.motors.disconnect)
        # Creating Thread for Indicators
        self.thread_get_position = Thread(
            target=function_indicators,
            args=(self,))
        self.thread_get_position.start()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
window.event_stop.set()  # Setting event after closing the UI to stop the while loop in function_indicators()
window.motors.disconnect()  # The controller is disconnected in case the user forgets to do it.
