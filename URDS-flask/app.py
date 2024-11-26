#!/usr/bin/python3

from flask import Flask, request, jsonify
import mysql.connector
import requests
import smtplib
from db_actions import DBStorage

from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Ozeki SMS Gateway Configuration
ozeki_sms_url = os.getenv('OZEKI_SMS_URL')
ozeki_username = os.getenv('OZEKI_USERNAME')
ozeki_password = os.getenv('OZEKI_PASSWORD')

# Email Configuration
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = os.getenv('SMTP_PORT')
smtp_user = os.getenv('SMTP_USER')
smtp_password = os.getenv('SMTP_PASSWORD')

# Route to add sensor data
@app.route('/add_sensor_data', methods=['POST'])
def add_sensor_data():
    data = request.json
    sensor_id = data.get('sensor_id')
    data_value = data.get('data_value')
    
    try:
        db = DBStorage()
        db.save(sensor_id, data_value)
        
        return jsonify({'status': 'success', 'message': 'Data added and notifications sent.'}), 201
    except mysql.connector.Error as err:
        return jsonify({'status': 'error', 'message': str(err)}), 500
    finally:
        db.close()

# # Function to send SMS
# def send_sms_notification(message):
#     payload = {
#         'username': ozeki_username,
#         'password': ozeki_password,
#         'recipient': '+1234567890',  # Replace with recipient's phone number
#         'messagetype': 'SMS:TEXT',
#         'messagedata': message
#     }
#     response = requests.post(ozeki_sms_url, data=payload)
#     if response.status_code == 200:
#         print('SMS sent successfully')
#     else:
#         print('Failed to send SMS', response.content)

# # Function to send email
# def send_email_notification(subject, message):
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = 'recipient@example.com'  # Replace with recipient's email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(message, 'plain'))
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        print('Email sent successfully')
    except Exception as e:
        print('Failed to send email', e)

if __name__ == '__main__':
    app.run(debug=True)
