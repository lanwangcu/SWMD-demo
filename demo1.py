# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'demo1.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Security(object):
    def setupUi(self, Security):
        Security.setObjectName("Security")
        Security.resize(1089, 422)
        self.StartButton = QtWidgets.QPushButton(Security)
        self.StartButton.setGeometry(QtCore.QRect(60, 80, 141, 81))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.StartButton.setFont(font)
        self.StartButton.setObjectName("StartButton")
        self.StopButton = QtWidgets.QPushButton(Security)
        self.StopButton.setGeometry(QtCore.QRect(60, 170, 141, 81))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.StopButton.setFont(font)
        self.StopButton.setObjectName("StopButton")
        self.fig_metal = QtWidgets.QLabel(Security)
        self.fig_metal.setEnabled(True)
        self.fig_metal.setGeometry(QtCore.QRect(220, 80, 800, 241))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fig_metal.sizePolicy().hasHeightForWidth())
        self.fig_metal.setSizePolicy(sizePolicy)
        self.fig_metal.setMaximumSize(QtCore.QSize(800, 480))
        self.fig_metal.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fig_metal.setFrameShadow(QtWidgets.QFrame.Plain)
        self.fig_metal.setText("")
        self.fig_metal.setPixmap(QtGui.QPixmap("C:/Users/XikoL/.designer/backup/Figs/check.png"))
        self.fig_metal.setScaledContents(True)
        self.fig_metal.setWordWrap(False)
        self.fig_metal.setObjectName("fig_metal")

        self.retranslateUi(Security)
        QtCore.QMetaObject.connectSlotsByName(Security)

    def retranslateUi(self, Security):
        _translate = QtCore.QCoreApplication.translate
        Security.setWindowTitle(_translate("Security", "Self-powered wireless metal detection system"))
        self.StartButton.setText(_translate("Security", "Start"))
        self.StopButton.setText(_translate("Security", "Stop"))