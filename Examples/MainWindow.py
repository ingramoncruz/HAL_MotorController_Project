# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.DisplayPosition = QtWidgets.QLCDNumber(self.centralwidget)
        self.DisplayPosition.setObjectName("DisplayPosition")
        self.gridLayout.addWidget(self.DisplayPosition, 0, 0, 1, 1)
        self.LabelDisplayText = QtWidgets.QLabel(self.centralwidget)
        self.LabelDisplayText.setObjectName("LabelDisplayText")
        self.gridLayout.addWidget(self.LabelDisplayText, 1, 0, 1, 1)
        self.ButtonMoveRelativeNegative = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonMoveRelativeNegative.setObjectName("ButtonMoveRelativeNegative")
        self.gridLayout.addWidget(self.ButtonMoveRelativeNegative, 3, 0, 1, 1)
        self.ButtonMoveRelativePositive = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonMoveRelativePositive.setObjectName("ButtonMoveRelativePositive")
        self.gridLayout.addWidget(self.ButtonMoveRelativePositive, 5, 0, 1, 1)
        self.LineEditDisplayText = QtWidgets.QLineEdit(self.centralwidget)
        self.LineEditDisplayText.setObjectName("LineEditDisplayText")
        self.gridLayout.addWidget(self.LineEditDisplayText, 2, 0, 1, 1)
        self.ButtonStop = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonStop.setObjectName("ButtonStop")
        self.gridLayout.addWidget(self.ButtonStop, 6, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.LabelDisplayText.setText(_translate("MainWindow", "TextLabel"))
        self.ButtonMoveRelativeNegative.setText(_translate("MainWindow", "Move Relative Negative"))
        self.ButtonMoveRelativePositive.setText(_translate("MainWindow", "Move Relative Positive"))
        self.ButtonStop.setText(_translate("MainWindow", "STOP"))
