from uuid import uuid4

import firebase_admin
from firebase_admin import credentials, db, auth
from datetime import datetime
import os
from dotenv import load_dotenv
from comm import *

load_dotenv()

def send_notifications(sensor_id, data_value, emails, phone_numbers):
    comm = Comm()
    comm.sendEmail("Bed Alert!", f"Alert, Bed is wet", emails)


class DBStorageCloud:
    def __init__(self):
        # Initialize Firebase
        cred = credentials.Certificate(
            os.getenv('FIREBASESECRESTSPATH'))  # Replace with your Firebase Admin SDK JSON file
        firebase_admin.initialize_app(cred, {
            'databaseURL': os.getenv('FIREBASEDBURL')  # Replace with your Firebase database URL
        })

    # Save data to Firebase
    def save_to_cloud_db(self, device_id, moisture_value):
        # Get current time and date
        now = datetime.now()
        timestamp = now.strftime("%H:%M:%S")  # Format as HH:MM:SS
        date = now.strftime("%Y-%m-%d")  # Format as YYYY-MM-DD

        # Define the database path
        path = f"UrineDetectorSystem/{device_id}/Readings/{date}/{timestamp}"

        # Push data to Firebase
        ref = db.reference(path)
        ref.set({
            "moisturelevel": moisture_value
        })

        if moisture_value > 800:
            emails = self.get_emails(device_id)
            phonenumbers = []
            send_notifications(device_id, moisture_value, emails, phonenumbers)


    def get_from_cloud_db(self, device_id):
        try:
            device_ref = db.reference(f"UrineDetectorSystem/{device_id}")
            data = device_ref.get()
            return data
        except Exception as e:
            raise RuntimeError(f"Error fetching data for DeviceID {device_id}: {e}")

    def get_emails(self, device_id):
        try:
            ref = db.reference("Users")
            users = ref.get()  # Retrieve all users

            # Filter users associated with the given device_id
            emails = []
            for user_id, user_info in users.items():
                if user_info.get("deviceId") == device_id:
                    emails.append(user_info.get("email"))

            return emails

        except Exception as e:
            print("Error fetching emails:", e)
            return None

    def store_user_info(self, device_id, email, username, user_phone_number, password):
        # Define the database path for the user
        user = auth.create_user(
            email=email,
            password=password
        )
        user_ref = db.reference(f"Users/{user.uid}")

        # Set user information
        user_ref.set({
            "email": email,
            "deviceId": device_id,
            "name": username,
            "phone": user_phone_number
        })