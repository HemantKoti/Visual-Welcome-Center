"""
    Name: Hemant Koti
    UB ID: 50338178
    UB Name: hemantko
    Description: This class handles all the database operations
"""

import sys
import pymongo
import numpy as np
import face_recognition
import pickle
import bson

from io import BytesIO
from PIL import Image
from datetime import datetime
from Constants import Constants


class DatabaseManager:

    def __init__(self):
        """
            Database Manager Init. Used to initialize the database manager and Azure Cosmos Mongo DB instance
        """
        self.constants = Constants()

        self.myclient = pymongo.MongoClient(str(self.constants.conn_str))
        self.user_details_db = self.myclient[str(self.constants.database_name)]

        self.userDetailsCollection = self.user_details_db[str(
            self.constants.user_details_collection_name)]

        self.update_db_state()
        self.update_encodings()

    def update_db_state(self):
        """
           Updates the state of the database for every frame
        """
        # Get known face encodings and namees from the DB
        faces = self.userDetailsCollection.find(
            {"Encodings": {"$exists": False}})

        for record in faces:
            try:
                picture = face_recognition.load_image_file(BytesIO(record["Picture"]))

                face_locations = face_recognition.face_locations(picture)
                face_encodings = face_recognition.face_encodings(picture, face_locations)

                encode_blob = bson.Binary(pickle.dumps(face_encodings, protocol=2))
                self.userDetailsCollection.update(
                    {"_id": record["_id"]}, {"$set": {"Encodings": encode_blob}})
            except:
                print()

    def update_encodings(self):
        """
           Updates the encodings for all the images/frames
        """
        faces = self.userDetailsCollection.find({})

        self.email_address_list = []
        self.visiting_purpose_list = []
        self.appointment_time_list = []

        self.known_face_encodings = []
        self.known_face_names = []
        self.picture_list = []

        for record in faces:
            try:
                if record["Name"] not in self.known_face_names:
                    picture = face_recognition.load_image_file(BytesIO(record["Picture"]))
                    self.picture_list.append(picture)

                    self.email_address_list.append(record["EmailAddress"])
                    self.visiting_purpose_list.append(record["VisitingPurpose"])
                    self.appointment_time_list.append(record["AppointmentDate"])
                    
                    self.known_face_encodings.append(
                        pickle.loads(record["Encodings"]))
                    self.known_face_names.append(record["Name"])                
            except:
                print()

    def write_login_text(self, index):
        """
           Writes the login text to the widget labels
        """
        name = str(self.known_face_names[index])
        logintime = str(datetime.now())
        email = str(self.email_address_list[index])
        vistingpurpose = str(self.visiting_purpose_list[index])
        appointmentdate = str(self.appointment_time_list[index])

        self.constants.welcomeLoginLabel = "Welcome {0}".format(name)        

        self.constants.welcomeLoginTextBox = "User Details" + "\nLogin Time: {0}\nEmailAddress: {1}\nVisiting Purpose: {2}\nAppointment Date: {3}".format(logintime, email, vistingpurpose, appointmentdate)

        print(self.constants.welcomeLoginTextBox)
        print(self.constants.welcomeLoginLabel)

