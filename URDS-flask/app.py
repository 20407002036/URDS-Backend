#!/usr/bin/python3
from crypt import methods

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

db = DBStorage()

# Route to add sensor data
@app.route('/add_sensor_data', methods=['POST'])
def add_sensor_data():
    data = request.json
    DeviceID = data.get('sensor_id')
    data_value = data.get('data_value')
    
    try:
        db.save(DeviceID, data_value)
        return jsonify({'status': 'success', 'message': 'Data added and notifications sent.'}), 201
    except mysql.connector.Error as err:
        return jsonify({'status': 'error', 'message': str(err)}), 500
    finally:
        db.close()
        
#Register Users
@app.route('/users/register', methods=['POST'])
def register_user():
    data = request.json
    DeviceID = data.get('device_id')
    user_email = data.get('user_email')
    user_name= data.get('user_name')
    user_phone_number = data.get('user_phone')

    try:
        db.register_user(DeviceID, user_email, user_name, user_phone_number)
        return jsonify({'status': 'success', 'message': 'User registered.'}), 201
    except mysql.connector.Error as err:
        return jsonify({'status': 'error', 'message': str(err)}), 500
    finally:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
