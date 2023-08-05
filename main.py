from PyQt5.QtCore import * # QObject, QThread, pyqtSignal
from source.controller_hal.pi_controller.hal_pi_controller import *
from source.user_interfaces.main_window import *
import sys
from threading import Thread, Event
import time


def function_get_position(self):
    """This function is activated by a Thread to continuously adquire the current position
    of the axis set. It is shutdown before closing the app.
    """
    event = self.event_stop
    while not event.is_set():
        self.Led_Connected.setChecked(self.motors.get_connected())
        self.Led_Moving.setChecked(self.motors.get_moving())
        self.Indicator_Position.display(self.motors.get_position())
        time.sleep(0.1)
    return


# class WorkerConnection(QObject):
#     def __init__(self, self_window):
#         super(WorkerConnection, self).__init__()
#         self.led_connected = self_window.Led_Connected.setChecked
#         self.get_connected = self_window.motors.get_connected
#         self.text = self_window.Led_Connected.setText
#         self.event = self_window.event_stop

#     finished = pyqtSignal()

#     def run(self):
#         while not self.event.is_set():
#             connection =self.get_connected()
#             self.led_connected(connection)
#             self.text(f"{connection}")
#             time.sleep(0.2)
#         return self.finished.emit()


# class WorkerMoving(QObject):
#     def __init__(self, self_window):
#         super(WorkerMoving, self).__init__()
#         self.led_moving = self_window.Led_Moving.setChecked
#         self.get_moving = self_window.motors.get_moving
#         self.event = self_window.event_stop

#     finished = pyqtSignal()

#     def run(self):
#         while not self.event.is_set():
#             moving =self.get_moving()
#             self.led_moving(moving)
#             time.sleep(0.2)
#         return self.finished.emit()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """ This is the main class which suppots all the user interface for the App, and connects
    everything with the hal controller to be used with the app.
    """
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

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
            args=(self,))
        self.thread_get_position.start()

    # def display_connection(self):
    #     self.thread_connection = QThread()
    #     self.worker_connection = WorkerConnection(self)
    #     self.worker_connection.moveToThread(self.thread_connection)
    #     self.thread_connection.started.connect(self.worker_connection.run)
    #     self.worker_connection.finished.connect(self.thread_connection.quit)
    #     self.worker_connection.finished.connect(self.worker_connection.deleteLater)
    #     self.thread_connection.finished.connect(self.thread_connection.deleteLater)
    #     self.thread_connection.start()

    # def display_moving(self):
    #     self.thread_moving = QThread()
    #     self.worker_moving = WorkerMoving(self)
    #     self.worker_moving.moveToThread(self.thread_moving)
    #     self.thread_moving.started.connect(self.worker_moving.run)
    #     self.worker_moving.finished.connect(self.thread_moving.quit)
    #     self.worker_moving.finished.connect(self.worker_moving.deleteLater)
    #     self.thread_moving.finished.connect(self.thread_moving.deleteLater)
    #     self.thread_moving.start()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
# window.display_connection()
# window.display_moving()
app.exec()
window.event_stop.set()  # Stopping the while loop in function_get_position()
window.motors.disconnect()  # The controller is disconnected in case the user forgets to do it.
