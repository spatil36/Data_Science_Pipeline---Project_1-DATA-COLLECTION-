import time
import logging

from faktory import Worker
from reddit import call_reddit_api

logging.basicConfig(level=logging.INFO)

time.sleep(3600)

def call_api():
    call_reddit_api()

w = Worker(queues=['default'], concurrency=1)
w.register('call_api', call_api)
w.run()