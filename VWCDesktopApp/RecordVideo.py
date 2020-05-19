"""
    Name: Hemant Koti
    UB ID: 50338178
    UB Name: hemantko
    Desciption: Starts video capture feed from the camera
"""

import cv2
import numpy as np

from PyQt5 import QtCore


class RecordVideo(QtCore.QObject):
    image_data = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, camera_port = 0, parent=None):
        super().__init__(parent)
        self.video = cv2.VideoCapture(camera_port)
        self.timer = QtCore.QBasicTimer()

    def start_recording(self):
        self.timer.start(0, self)

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return

        read, data = self.video.read()
        if read:
            self.image_data.emit(data)

    def destroy(self):
        self.timer.stop()
        self.video.release()
