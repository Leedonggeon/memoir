import schedule
import time
from reply_v7 import reply
from replied_v7 import replied

def run_reply():
    reply()

def run_replied():
    replied()

schedule.every().wednesday.at("18:00").do(run_reply)
schedule.every().wednesday.at("20:00").do(run_replied)
schedule.every().tuesday.at("15:21").do(run_replied)

while True:
    schedule.run_pending()
    time.sleep(1)
