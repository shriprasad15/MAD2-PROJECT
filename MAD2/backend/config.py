import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI= os.environ.get('SQLALCHEMY_DATABASE_URI','sqlite:///grocery.db')
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
    CELERY_IMPORTS = ('backend.applicaiton.task')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY= 'HashValue'
    SECURITY_DEFAULT_REMEMBER_ME= True
    CACHE_TYPE = 'RedisCache'
    USER_ENABLE_EMAIL = False
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_HOST = os.environ.get('CACHE_REDIS_HOST')
    CACHE_REDIS_PASSWORD = os.environ.get('CACHE_REDIS_PASSWORD')
    CACHE_REDIS_PORT = 19788
