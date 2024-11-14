from dotenv import load_dotenv
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import smtplib

load_dotenv()

class Comm:
    def __init__(self):
        self.ozeki_sms_url = os.getenv('OZEKI_SMS_URL')
        self.ozeki_username = os.getenv('OZEKI_USERNAME')
        self.ozeki_password = os.getenv('OZEKI_PASSWORD')
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = os.getenv('SMTP_PORT')
        self.smtp_user = os.getenv('SMTP_USER')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
    
    def sendEmail(self, subject, message, emails):
        smtp_server = self.smtp_server
        smtp_port = self.smtp_port
        smtp_user = self.smtp_user
        smtp_password = self.smtp_password
        for email in emails:
            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))
        
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            text = msg.as_string()
            server.sendmail(smtp_user, smtp_user, text)
            server.quit()

    def sendSMS(self, message, phone_numbers):
        ozeki_sms_url = self.ozeki_sms_url
        ozeki_username = self.ozeki_username
        ozeki_password = self.ozeki_password
        
        for phone_number in phone_numbers:
            payload = {
                'username': ozeki_username,
                'password': ozeki_password,
                'recipient': phone_number,  # Replace with recipient's phone number
                'messagetype': 'SMS:TEXT',
                'messagedata': message
            }
            response = requests.post(ozeki_sms_url, data=payload)
            if response.status_code == 200:
                print('SMS sent successfully')
            else:
                print('Failed to send SMS', response.content)
