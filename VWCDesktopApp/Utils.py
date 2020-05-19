"""
    Name: Hemant Koti
    UB ID: 50338178
    UB Name: hemantko
"""

from PyQt5 import QtCore
from Constants import Constants

class Utils:

    def __init__(self):
        self.constants = Constants()

    def timer_func(self, count):
        print("Timer", count)
        if count >= self.constants.timeout:
            return

    def start_timer(self, slot, count=1, interval=1000):
        counter = 0
        def handler():
            nonlocal counter
            counter += 1
            slot(counter)
            if counter >= count:
                timer.stop()
                timer.deleteLater()
        timer = QtCore.QTimer()
        timer.timeout.connect(handler)
        timer.start(interval)
