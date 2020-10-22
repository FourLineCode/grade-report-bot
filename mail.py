import os
import smtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

load_dotenv()


def send_mail(address, mail_content):
    # The mail addresses and password
    sender_address = os.getenv('BOT_EMAIL')
    sender_pass = os.getenv('BOT_PASSWORD')
    receiver_address = address
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    # The subject line
    message['Subject'] = f'Grade report - {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', os.getenv('PORT'))
    session.starttls()
    # login with mail_id and password
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print(f'Grade Report Sent to {address}')
