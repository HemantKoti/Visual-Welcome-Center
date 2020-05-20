"""
    Name: Hemant Koti
    UB ID: 50338178
    UB Name: hemantko
    Desciption: This files contains all the constants required by the system
"""

import os

class Constants:

    def __init__(self):
        """
            Constants Init. Lists all the constants required by the system
        """
        self.width = 800
        self.height = 600

        self.registeredImageWidth = 200
        self.registeredImageHeight = 230

        self.loginImageWidth = self.loginImageHeight = 150

        self.icon = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + os.path.sep + 'resources' + os.path.sep + 'logo.ico'
        self.qrcode = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + os.path.sep + 'resources' + os.path.sep + 'qrcode.png'

        self.conn_str = "mongodb://visualwelcomecenter:WXYWQRt7rJArEKFxWNDp6O0d8delDZC9lUvxTfG0OtjcfjTFR2WQSFwzfMexkTeWQy0ACaDbvq8FMi9bvvmSaw==@visualwelcomecenter.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@visualwelcomecenter@"
        self.database_name = "VisualWelcomeCenter"
        self.user_details_collection_name = "UserDetails"

        self.date_time_format = "%m/%d/%Y %I:%M:%S %p"

        self.timeout = 30
        
        self.welcomeLoginLabel = ""
        self.welcomeLoginTextBox = ""
        self.unknown = "Unknown"

