"""
    Name: Hemant Koti
    UB ID: 50338178
    UB Name: hemantko
"""

import sys

from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from FaceDetectionWidget import FaceDetectionWidget
from RecordVideo import RecordVideo

qtFile = "FaceDetection.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtFile)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.vwcStack.setCurrentWidget(self.detectFaceWidget)

        self.face_detection_widget = FaceDetectionWidget()
        self.record_video = RecordVideo()

        self.homeButton.triggered.connect(self.NavigateToHome)        
        self.exitButton.triggered.connect(self.Exit)

        # Connect the image data signal and slot together
        image_data_slot = self.face_detection_widget.facerec_from_webcam
        self.record_video.image_data.connect(image_data_slot)

        self.record_video.start_recording()

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(self.face_detection_widget)

        self.recordVideoWidget.setLayout(layout)

    def Exit(self):
        self.record_video.destroy()
        sys.exit()

    def NavigateToHome(self):
        self.vwcStack.setCurrentWidget(self.detectFaceWidget)