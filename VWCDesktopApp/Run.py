"""
    Name: Hemant Koti
    UB ID: 50338178
    UB Name: hemantko
"""

import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from MainWindowComponent import MainWindow
from Constants import Constants


class Run():
    def __init__(self):
        constants = Constants()
        application = QtWidgets.QApplication(sys.argv)
        window = MainWindow()
        window.setMinimumSize(constants.width, constants.height)
        window.setWindowIcon(QtGui.QIcon(constants.icon))
        window.show()
        sys.exit(application.exec_())


if __name__ == "__main__":
    Run()
