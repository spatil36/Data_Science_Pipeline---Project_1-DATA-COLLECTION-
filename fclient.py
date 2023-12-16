import faktory
import time

time.sleep(3600)

with faktory.connection() as client:
    while True:
        client.queue('call_api')
        time.sleep(3600)