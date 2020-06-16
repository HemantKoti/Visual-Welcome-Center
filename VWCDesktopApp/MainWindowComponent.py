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
from PIL import Image
from PIL.ImageQt import ImageQt
from datetime import datetime

qtFile = "FaceDetection.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtFile)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        """
            Description:
                Main Window. Instantiate all the modules required by the MainWindow.
        """

        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.constants = Constants()
        
        self.homeButton.triggered.connect(self.Home)        
        self.exitButton.triggered.connect(self.Exit)

        self.startVideoCapture()

    def timer_func(self, count):
        """
            Description:
                Timer function. Maintains a timer list, 45 seconds across each window period.

            Args:
                Count: Number of seconds passed by                  
        """

        if count >= self.constants.timeout:
            self.Destroy()
            self.startVideoCapture()

    def start_timer(self, slot, count=1, interval=1000):
        """
            Description:
                Start timer event method

            Args:
                Slot:
                Count: Number 
                Interval:      
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
            Description:
                Starts the video capture sending frames to the face detection module.
        """

        self.face_detection_widget = FaceDetectionWidget()
        self.record_video = RecordVideo()

        # Connect the image data signal and slot together
        image_data_slot = self.face_detection_widget.facerec_from_webcam
        self.record_video.image_data.connect(image_data_slot)

        _face_register = self.registerFaceEvent
        self.face_detection_widget.faceRegister.connect(_face_register)

        _face_login = self.loginFaceEvent
        self.face_detection_widget.faceLogin.connect(_face_login)

        print("Starting video capture...")
        self.record_video.start_recording()
        
        self.boxlayout = QtWidgets.QVBoxLayout()
        self.boxlayout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.boxlayout.addWidget(self.face_detection_widget)

        self.recordVideoWidget.setLayout(self.boxlayout)

        self.vwcStack.setCurrentWidget(self.detectFaceWidget)


    def loginFaceEvent(self, index):
        """
            Description:
                Login face event method sent by face detection module

            Args:
                Index: 
        """

        if self.face_detection_widget.foundFace:
            self.boxlayout.deleteLater()
            self.record_video.destroy()
            self.set_login_widget(index)
            self.start_timer(self.timer_func, self.constants.timeout)

    def registerFaceEvent(self, frame):
        """
            Description:
                Register event method sent by face detection module

            Args:
                Frame: 
        """

        if self.face_detection_widget.foundNewFace:
            self.boxlayout.deleteLater()
            self.record_video.destroy()
            image = self.face_detection_widget.get_qimage(frame)
            self.set_qrcode_widget(image)
            self.start_timer(self.timer_func, self.constants.timeout)

    def set_login_widget(self, index):
        """
            Description:
                Sets the screen to the login widget post event detection

            Args:
                Index:
        """

        email = str(self.face_detection_widget.db_manager.email_address_list[index])
        now = datetime.utcnow().strftime(self.constants.date_time_format)
        self.face_detection_widget.db_manager.userDetailsCollection.update({"EmailAddress": email}, {"$set": {"LastLogin": now}})

        self.loginPhotolayout = QtWidgets.QVBoxLayout(self.loginPhotoWidget)
        label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap.fromImage(ImageQt(Image.fromarray(self.face_detection_widget.db_manager.picture_list[index]).resize((self.constants.loginImageWidth, self.constants.loginImageHeight))))        
        label.setPixmap(pixmap)
        self.loginPhotolayout.addWidget(label)
        self.loginPhotoWidget.setLayout(self.loginPhotolayout)

        name = str(self.face_detection_widget.db_manager.known_face_names[index])
        logintime = str(now)
        jobtitle = str(self.face_detection_widget.db_manager.jobtitle_list[index])
        vistingpurpose = str(self.face_detection_widget.db_manager.visiting_purpose_list[index])
        appointmentdate = str(self.face_detection_widget.db_manager.appointment_time_list[index])  
        
        welcomeLoginLabel = "Welcome\t{0}".format(name)
        welcomeLoginTextBox = "\t\t\t\tUser Details" + "\n\n\tLogin Time:\t\t{0}\n\n\tEmailAddress:\t\t{1}\n\n\tJob Title:\t\t{2}\n\n\tVisiting Purpose:\t{3}\n\n\tAppointment Date:\t{4}".format(logintime, email, jobtitle, vistingpurpose, appointmentdate)

        self.loginLabel.setText(welcomeLoginLabel)
        self.userDetailsLabel.setText(welcomeLoginTextBox)

        self.vwcStack.setCurrentWidget(self.loginWidget)


    def set_qrcode_widget(self, image):
        """
            Description:
                Sets the screen to the QR code widget post event detection

           Args:
                Image: 
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

    def Destroy(self):
        """
            Description:
                Sets the screen to the QR code widget post event detection
        """

        try:
            self.loginPhotolayout.deleteLater()
        except Exception as ex:
            print(ex)

        try:
            self.loginLabelLayout.deleteLater()
        except Exception as ex:
            print(ex)                
            
        try:
            self.userDetailsLayout.deleteLater()
        except Exception as ex:
            print(ex)

        try:
            self.scanQRlayout.deleteLater()
        except Exception as ex:
            print(ex)

        try: 
            self.registerPhotolayout.deleteLater()
        except Exception as ex:
            print(ex)

        self.face_detection_widget.foundNewFace = False
        self.face_detection_widget.foundFace = False

    def Exit(self):
        """
            Description:
                Exit the system
        """

        self.record_video.destroy()
        sys.exit()

    def Home(self):
        """
            Description:
                Navigate to home
        """

        self.Destroy()
        self.startVideoCapture()
