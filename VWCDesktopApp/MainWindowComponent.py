"""
    Name: Hemant Koti
    UB ID: 50338178
    UB Name: hemantko
    Description: This class handles all the operations pertaining to the main window
"""

import sys

from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QEventLoop
from FaceDetectionWidget import FaceDetectionWidget
from RecordVideo import RecordVideo
from Constants import Constants
from DatabaseManager import DatabaseManager
from Utils import Utils
from PIL import Image
from PIL.ImageQt import ImageQt

qtFile = "FaceDetection.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtFile)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        """
            Main Window Init. Handles all the operations pertaining to the Main UI
        """
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.constants = Constants()
        self.utils = Utils()
        
        self.homeButton.triggered.connect(self.Home)        
        self.exitButton.triggered.connect(self.Exit)

        self.startVideoCapture()

    def timer_func(self, count):
        """
            Timer function. Maintains a timer list, 45 seconds across each window period
        """
        if count >= self.constants.timeout:
            try:
                self.loginPhotolayout.deleteLater()
            except:
                print()

            try:
                self.loginLabelLayout.deleteLater()
            except:
                print()                
            
            try:
                self.userDetailsLayout.deleteLater()
            except:
                print()

            try:
                self.scanQRlayout.deleteLater()
            except:
                print()

            try: 
                self.registerPhotolayout.deleteLater()
            except:
                print()

            self.face_detection_widget.foundNewFace = False
            self.face_detection_widget.foundFace = False

            self.startVideoCapture()

    def start_timer(self, slot, count=1, interval=1000):
        """
            Start timer event method
        """
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

    def startVideoCapture(self):
        """
            Starts the video capture sending frames to the face detection module
        """
        print("Start Video Capture")

        self.face_detection_widget = FaceDetectionWidget()
        self.record_video = RecordVideo()

        # Connect the image data signal and slot together
        image_data_slot = self.face_detection_widget.facerec_from_webcam
        self.record_video.image_data.connect(image_data_slot)

        _face_register = self.registerFaceEvent
        self.face_detection_widget.faceRegister.connect(_face_register)

        _face_login = self.loginFaceEvent
        self.face_detection_widget.faceLogin.connect(_face_login)

        self.record_video.start_recording()
        
        self.boxlayout = QtWidgets.QVBoxLayout()
        self.boxlayout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.boxlayout.addWidget(self.face_detection_widget)

        self.recordVideoWidget.setLayout(self.boxlayout)

        self.vwcStack.setCurrentWidget(self.detectFaceWidget)

    def loginFaceEvent(self, frame):
        """
            Login face event method sent by face detection module
        """
        if self.face_detection_widget.foundFace:
            self.boxlayout.deleteLater()
            self.record_video.destroy()
            self.set_login_widget(frame)
            self.start_timer(self.timer_func, self.constants.timeout)

    def registerFaceEvent(self, frame):
        """
            Register event method sent by face detection module
        """
        if self.face_detection_widget.foundNewFace:
            self.boxlayout.deleteLater()
            self.record_video.destroy()
            image = self.face_detection_widget.get_qimage(frame)
            self.set_qrcode_widget(image)
            self.start_timer(self.timer_func, self.constants.timeout)

    def set_login_widget(self, image):
        """
            Sets the screen to the login widget post event detection
        """
        self.loginPhotolayout = QtWidgets.QVBoxLayout(self.loginPhotoWidget)
        label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap.fromImage(ImageQt(Image.fromarray(image).resize((self.constants.loginImageWidth, self.constants.loginImageHeight))))        
        label.setPixmap(pixmap)
        self.loginPhotolayout.addWidget(label)
        self.loginPhotoWidget.setLayout(self.loginPhotolayout)

        self.loginLabelLayout = QtWidgets.QVBoxLayout(self.loginLabelWidget)
        labelLogin = QtWidgets.QLabel()
        labelLogin.setText(self.constants.welcomeLoginLabel)
        self.loginLabelLayout.addWidget(labelLogin)
        self.loginLabelWidget.setLayout(self.loginLabelLayout)
        QtWidgets.QApplication.processEvents()
        QtGui.QGuiApplication.processEvents()

        self.userDetailsLayout = QtWidgets.QVBoxLayout(self.userDetailsWidget)
        userDetailsLabel = QtWidgets.QLabel()
        userDetailsLabel.setText(self.constants.welcomeLoginTextBox)
        self.userDetailsLayout.addWidget(userDetailsLabel)
        self.userDetailsWidget.setLayout(self.userDetailsLayout)
        QtWidgets.QApplication.processEvents() 
        QtGui.QGuiApplication.processEvents()

        self.vwcStack.setCurrentWidget(self.loginWidget)

    def set_qrcode_widget(self, image):
        """
            Sets the screen to the QR code widget post event detection
        """
        self.scanQRlayout = QtWidgets.QVBoxLayout(self.scanQRWidget)
        label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(self.constants.qrcode)
        label.setPixmap(pixmap)
        self.scanQRlayout.addWidget(label)
        self.scanQRWidget.setLayout(self.scanQRlayout)

        self.registerPhotolayout = QtWidgets.QVBoxLayout(self.registerPhotoWidget)
        label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(image)
        label.setPixmap(pixmap.scaled(self.constants.registeredImageWidth, self.constants.registeredImageHeight))
        self.registerPhotolayout.addWidget(label)
        self.registerPhotoWidget.setLayout(self.registerPhotolayout)        

        self.vwcStack.setCurrentWidget(self.completeRegistrationWidget)

    def Exit(self):
        """
            Exit the system
        """
        self.record_video.destroy()
        sys.exit()

    def Home(self):
        """
            Navigate to home
        """
        self.startVideoCapture()
