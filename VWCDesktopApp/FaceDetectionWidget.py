"""
    Name: Hemant Koti
    UB ID: 50338178
    UB Name: hemantko
    Desciption: This program is responsible to handle all the face detection and recognition algorithms.
"""

import cv2
import numpy as np
import face_recognition

from io import BytesIO 
from PIL import Image
from PyQt5 import QtWidgets, QtGui, QtCore
from Constants import Constants
from DatabaseManager import DatabaseManager


class FaceDetectionWidget(QtWidgets.QWidget):

    faceRegister = QtCore.pyqtSignal(np.ndarray)
    faceLogin = QtCore.pyqtSignal(int)


    def __init__(self, parent=None):
        """
            Face Detection Init. Instantiate all the classes required by face detection module.
        """

        super().__init__(parent)
        self.constants = Constants()
        self.db_manager = DatabaseManager()

        self._red = (0, 0, 255)
        self._width = 2

        self.image = QtGui.QImage()
        self.process_this_frame = True
        self.foundNewFace = False
        self.foundFace = False

    def paintEvent(self, event):
        """
            Invokes paint event to update the GUI
        """
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    def get_qimage(self, image: np.ndarray):
        """
            Returns a QImage from the numpy array frame
        """
        height, width, colors = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage

        image = QImage(image.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def facerec_from_webcam(self, frame):
        """
            This method is bound to the Record video capture class where all the frames are captured, connected and sent one by one.
            This method also handles all the necessary operations required for face detection and recognition. 
            First step is to find the the facial locations then find the facial encodings.
            The known facial locations of all the registered people are taken from the Mondgo database and compared with the video frames.
            The feed also displays the frames with name and other details as well.
        """

        face_locations = []
        face_encodings = []
        face_names = []

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of the video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []

            for face_encoding in face_encodings:

                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.db_manager.known_face_encodings, face_encoding)
                first_match_index = 0
                name = self.constants.unknown

                # If a match was found in known_face_encodings, just use the first one.
                try:
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = self.db_manager.known_face_names[first_match_index]
                except Exception as ex:
                    name = self.db_manager.known_face_names[first_match_index]
                    print("Error while finding matches. Match found was not correct, reverting to the first found index: {0}".format(ex))
            
                face_names.append(name)

        self.process_this_frame = not self.process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        font, 1.0, (255, 255, 255), 1)

            self.foundNewFace = (True if name == self.constants.unknown else False)
            self.foundFace = (True if name in self.db_manager.known_face_names else False)

        self.image = self.get_qimage(frame)
        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())

        self.update()

        if self.foundNewFace:
            self.faceRegister.emit(frame)

        if self.foundFace:
            self.faceLogin.emit(first_match_index)