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

        self.userDetailsCollection = self.user_details_db[str(self.constants.user_details_collection_name)]

        self.email_address_list = []
        self.jobtitle_list = []
        self.lastlogin_list = []
        self.visiting_purpose_list = []
        self.appointment_time_list = []

        self.known_face_encodings = []
        self.known_face_names = []
        self.picture_list = []

        self.update_db_state()
        self.update_details()

    def update_db_state(self):
        """
           Updates the state of the database for every frame
        """

        # Get known face encodings and namees from the DB
        print()
        print()
        print()
        print("Updating database state...")

        encodings = self.userDetailsCollection.find({"Encodings": {"$exists": False }})

        try:
            for record in encodings:
                picture = face_recognition.load_image_file(BytesIO(record["Picture"]))

                face_locations = face_recognition.face_locations(picture)
                face_encoding = face_recognition.face_encodings(picture, face_locations)[0]

                encode_blob = bson.Binary(pickle.dumps(face_encoding, protocol=2))
                self.userDetailsCollection.update({"_id": record["_id"]}, {"$set": {"Encodings": encode_blob}})

                now = datetime.utcnow().strftime(self.constants.date_time_format)
                self.userDetailsCollection.update({"_id": record["_id"]}, {"$set": {"LastLogin": now }})
        except Exception as ex:
            print(ex)

    def update_details(self):
        """
           Updates the encodings for all the images/frames
        """

        print("Fetching user details...")

        faces = self.userDetailsCollection.find({})

        for record in faces:
            try:
                if record["EmailAddress"] not in self.email_address_list:
                    picture = face_recognition.load_image_file(BytesIO(record["Picture"]))
                    self.picture_list.append(picture)

                    self.email_address_list.append(record["EmailAddress"])
                    self.jobtitle_list.append(record["JobTitle"])
                    self.lastlogin_list.append(record["LastLogin"])                
                    self.visiting_purpose_list.append(record["VisitingPurpose"])
                    self.appointment_time_list.append(record["AppointmentDate"])
                    
                    self.known_face_encodings.append(pickle.loads(record["Encodings"]))
                    self.known_face_names.append(record["Name"])                
            except Exception as ex:
                print(ex)    