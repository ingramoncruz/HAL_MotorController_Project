from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QLCDNumber
from PyQt5.QtCore import QSize, Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.label = QLabel()
        self.Display_Number = QLCDNumber()
        self.input = QLineEdit()
        self.input.textChanged.connect(self.print_in_label)
        self.input.textChanged.connect(self.check_size_text)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)
        layout.addWidget(self.Display_Number)

        container = QWidget()
        container.setLayout(layout)

        self.setFixedSize(QSize(400, 300))

        self.setCentralWidget(container)

    def print_in_label(self):
        self.text = self.input.displayText()
        self.label.setText(self.text)
        # self.label.setText(self.input.displayText())


    def check_size_text(self, displayText):
        self.size = len(displayText)
        self.Display_Number.display(self.size)


    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            # handle the left-button press in here
            self.label.setText("mousePressEvent LEFT")

        elif e.button() == Qt.MiddleButton:
            # handle the middle-button press in here.
            self.label.setText("mousePressEvent MIDDLE")

        elif e.button() == Qt.RightButton:
            # handle the right-button press in here.
            self.label.setText("mousePressEvent RIGHT")

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.label.setText("mouseReleaseEvent LEFT")

        elif e.button() == Qt.MiddleButton:
            self.label.setText("mouseReleaseEvent MIDDLE")

        elif e.button() == Qt.RightButton:
            self.label.setText("mouseReleaseEvent RIGHT")

    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.label.setText("mouseDoubleClickEvent LEFT")

        elif e.button() == Qt.MiddleButton:
            self.label.setText("mouseDoubleClickEvent MIDDLE")

        elif e.button() == Qt.RightButton:
            self.label.setText("mouseDoubleClickEvent RIGHT")




app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
