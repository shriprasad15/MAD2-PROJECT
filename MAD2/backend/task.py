from workers import celery
import time
from datetime import timedelta
import csv, os
from database import exportdetails
from utils import send_message
from celery.schedules import crontab

@celery.task()
def send_welcome_msg(data):
    print(time.time())
    time.sleep(10)
    print(time.time())
    return "Test"

webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAABN4yDm8/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=bdFYUNx6xyL2btWwQDrHKIflDVhQBJ66rSs-vcREwjA'

@celery.task()
def generate_csv():
    time.sleep(5)
    for file in os.listdir('./instance'):
        if file.endswith(".csv"):
            os.remove(f'./instance/{file}')
    with open(f'./instance/name.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Product Name", "stock_left", "rate", "units sold"])
        result = exportdetails()
        for row in result:
            name, stock_left, rate_per_unit, total_quantity = row
            print(
                f"Product Name: {name},Stock Left {stock_left}, Rate per Unit: {rate_per_unit}, Total Quantity: {total_quantity}")

            writer.writerow(row)  # to send file to user as download

    # Message content to send
    message = 'CSV sent after generating. Click here to download: http://127.0.0.1:8081/download_csv'
    return send_message(webhook_url, message)

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=17,minute=6), engagment.s(), name='Monthly Report')
    sender.add_periodic_task(timedelta(seconds=30), engagment.s(), name="Secondly report")
    # sender.add_periodic_task(crontab(minute=0, hour=0), daily_reminder.s(), name='daily reminders')

@celery.task()
def engagment():
    message="This is a reminder mail"
    send_message(webhook_url, message)
