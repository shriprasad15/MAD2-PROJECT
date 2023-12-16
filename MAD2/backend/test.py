# from flask import Flask, request
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
#
# app = Flask(__name__)
#
#
# @app.route('/webhook', methods=['POST'])
# def process_webhook():
#     # Assuming the webhook data contains email content and details
#     data = request.get_json()  # Assuming webhook data is in JSON format
#
#     # Extract necessary details from the webhook payload
#     recipient_email = data.get('recipient_email')
#     subject = data.get('subject')
#     message_body = data.get('message_body')
#
#     # Your email configuration
#     sender_email = 'your_email@gmail.com'
#     sender_password = 'your_password'
#
#     # Create the email message
#     message = MIMEMultipart()
#     message['From'] = sender_email
#     message['To'] = recipient_email
#     message['Subject'] = subject
#
#     # Attach message body
#     message.attach(MIMEText(message_body, 'plain'))
#
#     # Connect to the SMTP server and send the email
#     with smtplib.SMTP('smtp.gmail.com', 587) as server:
#         server.starttls()
#         server.login(sender_email, sender_password)
#         server.sendmail(sender_email, recipient_email, message.as_string())
#
#     return 'Email sent successfully'
#
#
# if __name__ == '__main__':
#     app.run(debug=True)

import requests
import json

# import requests
# import json
#
# def send_message(webhook_url, message):
#     headers = {
#         'Content-Type': 'application/json; charset=UTF-8'
#     }
#
#     payload = {
#         'text': message
#     }
#
#     try:
#         response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
#
#
#         if response.status_code == 200:
#             print("Message sent successfully")
#         else:
#             print(f"Failed to send message. Status code: {response.status_code}")
#     except requests.RequestException as e:
#         print(f"Error sending message : {str(e)}")

# Replace 'YOUR_WEBHOOK_URL' with your actual Google Space webhook URL
# webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAABN4yDm8/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=bdFYUNx6xyL2btWwQDrHKIflDVhQBJ66rSs-vcREwjA'
#
# # Message content to send
# message = 'Hello, this is a test message '
#
# # File path of the CSV file to attach
# csv_file_path = '/Users/shriprasad/Desktop/MAD2-PROJECT/MAD2/backend/instance/name.csv'
#
# # Send the message with the attachment
# send_message(webhook_url, message)

from weasyprint import HTML
HTML('http://localhost:8080/user-dashboard/home').write_pdf('weasyprint-website.pdf')

