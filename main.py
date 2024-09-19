""" This is the main.py which starts all the modules to be controlled or used in the user
interface provided and created in PyQt5.
"""

import PyQt5
#from PyQt5.QtCore import QObject, QThread, pyqtSignal
from threading import Thread, Event
import time
# Relative import for the modules to be used
from source.controller_hal.pi_controller.hal_pi_controller import *
from source.controller_hal.newport_controller.hal_newport_controller import *
from source.user_interfaces.main_window import *


def function_indicators(self):
    """ This function is activated by a Thread to continuously adquire the current position, the
    connection status and if the motor is moving."""
    event = self.event_stop
    while not event.is_set():
        # The function needs to be called to pass that data in the indicators (slots)
        self.led_connected.setChecked(self.motors.get_connection())
        self.indicator_position.display(self.motors.get_position())
        self.led_moving.setChecked(self.motors.get_moving())
        time.sleep(0.2)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """ This is the main class which suppots all the user interface for the App, and connects
    everything with the hal controller to be used with the app."""
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.event_stop = Event()
        self.select_motor.addItems(['Motor 1', 'Motor 2'])
        self.select_controller.addItems(['PI', 'Newport'])
        self.select_controller.currentTextChanged.connect(self.initialize_controller_instance)

    def initialize_controller_instance(self, controller):
        """ This function is used to start the controller instance according with the selected
        controller."""
        # Initializing inputs with the current values in the controllers
        current_distance = self.input_distance.value()
        current_position = self.input_position.value()
        # Checking connection to shut it down before changing connection to a new controller.
        # If not connected, an exception is raised up. That means we can discard it and
        # proceed with normal initialization for connection with the controller selected.
        try:
            if self.motors.get_connection():
                self.event_stop.set()
                self.motors.disconnect()
        except:
            pass
        finally:
            if controller == 'PI':
                self.motors = PiHalClass(current_distance, current_position)
            else:
                self.motors = NewportHalClass(current_distance, current_position)
            self.motors.motor_select(self.select_motor.currentText())
            # Connecting all controllers (signals) with their respective methods.
            self.input_position.valueChanged.connect(self.motors.set_position)
            self.input_distance.valueChanged.connect(self.motors.set_distance)
            self.select_motor.currentTextChanged.connect(self.motors.motor_select)
            self.button_move_relative_positive.released.connect(self.motors.move_relative_positive)
            self.button_move_relative_negative.released.connect(self.motors.move_relative_negative)
            self.button_move_absolute.released.connect(self.motors.move_absolute)
            self.button_connect.released.connect(self.motors.connect)
            self.button_disconnect.released.connect(self.motors.disconnect)
            self.button_stop.released.connect(self.motors.stop_motion)
            # Creating Thread for Indicators
            self.event_stop.clear()
            self.thread_get_connection = Thread(
                target=function_indicators,
                args=(self,))
            self.thread_get_connection.start()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.initialize_controller_instance('PI') # Initializing a default controller
window.show()
app.exec()
window.event_stop.set()  # Setting event after closing the UI to stop the while loop in function_indicators()
window.motors.disconnect()  # The controller is disconnected in case the user forgets to do it.
