from dotenv import load_dotenv
import os
from comm import Comm, infobip_sms
import mysql.connector

load_dotenv()


def send_notifications(sensor_id, data_value, emails, phone_numbers):
    comm = Comm()
    # Send SMS notification
    # send_sms_notification(f"New data received from sensor {sensor_id}: {data_value}")
    # comm.sendSMS(f"New data received from sensor {sensor_id}: {data_value}", phone_numbers)
    infobip_sms(f"New data received from sensor {sensor_id}: {data_value}", phone_numbers)

    # Send email notification
    # send_email_notification("New Sensor Data", f"Data from sensor {sensor_id}: {data_value}")
    comm.sendEmail("New Sensor Data", f"Data from sensor {sensor_id}: {data_value}", emails)


class DBStorage:

    def __init__(self):
        self.db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}
        self.conn = mysql.connector.connect(**self.db_config)
        self.cursor = self.conn.cursor()
        
    def save(self, DeviceID, data_value):
        
        self.cursor.execute("INSERT INTO Readings (DeviceID, MoistureLevel) VALUES (%s, %s)", (DeviceID, data_value))
        self.conn.commit()
        if data_value > 50: #Data value is subject to chanage depending on the sensor
            emails= self.get_user_emails(DeviceID)
            phone_numbers = self.get_user_phone_numbers(DeviceID)
            send_notifications(DeviceID, data_value, emails, phone_numbers)

    def get_user_emails(self, sensor_id):
        self.cursor.execute("SELECT Email FROM Users WHERE DeviceID = %s", (sensor_id,))
        return self.cursor.fetchall()
    
    def get_user_phone_numbers(self, sensor_id):
        self.cursor.execute("SELECT Phone FROM Users WHERE DeviceID = %s", (sensor_id,))
        return self.cursor.fetchall()

    def register_user(self, DeviceID, user_email, user_name, user_phone_number):
        self.cursor.execute("INSERT INTO Users (DeviceID, Email, Name, Phone) VALUES (%s, %s, %s, %s)", (DeviceID, user_email, user_name, user_phone_number))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()