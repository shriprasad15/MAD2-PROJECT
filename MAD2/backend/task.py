from workers import celery
import time
@celery.task()
def send_welcome_msg(data):
    print(time)
    time.sleep(10)
    print(time)
    return "Gokul"