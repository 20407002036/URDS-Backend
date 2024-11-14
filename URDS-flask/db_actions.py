from dotenv import load_dotenv
import os
from comm import Comm
import mysql.connector

load_dotenv()


class DBStorage:

    def __init__(self):
        db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('BD_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()
        
    def save(self, sensor_id, data_value):
        
        self.cursor.execute("INSERT INTO sensor_data (sensor_id, data_value) VALUES (%s, %s)", (sensor_id, data_value))
        self.conn.commit()
        if(data_value > 50): #Data value is subject to chanage depending on the sensor
            emails= self.get_user_emails(sensor_id)
            phone_numbers = self.get_user_phone_numbers(sensor_id)
            self.send_notifications(sensor_id, data_value, emails, phone_numbers)

    def send_notifications(self, sensor_id, data_value, emails, phone_numbers):
        comm = Comm()
        # Send SMS notification
        # send_sms_notification(f"New data received from sensor {sensor_id}: {data_value}")
        comm.sendSMS(f"New data received from sensor {sensor_id}: {data_value}", phone_numbers)
        
        # Send email notification
        # send_email_notification("New Sensor Data", f"Data from sensor {sensor_id}: {data_value}")
        comm.sendEmail("New Sensor Data", f"Data from sensor {sensor_id}: {data_value}", emails)
    def get_user_emails(self, sensor_id):
        self.cursor.execute("SELECT Email FROM Users WHERE DeviceID = %s", (sensor_id,))
        return self.cursor.fetchall()
    
    def get_user_phone_numbers(self, sensor_id):
        self.cursor.execute("SELECT Phone FROM Users WHERE DeviceID = %s", (sensor_id,))
        return self.cursor.fetchall()
    
    def close(self):
        self.cursor.close()
        self.conn.close()