import os
from dotenv import load_dotenv
load_dotenv()

class Config:

    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
    CELERY_IMPORTS = ('backend.applicaiton.task')
    SECRET_KEY= 'HashValue'
    CACHE_TYPE = 'RedisCache'
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_HOST = os.environ.get('CACHE_REDIS_HOST')
    CACHE_REDIS_PASSWORD = os.environ.get('CACHE_REDIS_PASSWORD')
    CACHE_REDIS_PORT = 19788
