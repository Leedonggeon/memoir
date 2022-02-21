import schedule
import time
from sunday_v7 import sunday
from thursday_v7 import thursday
from archive_v7 import archive
from noti_v7 import noti

def run_noti():
    noti()

def run_sunday():
    sunday()

def run_thursday():
    thursday()

def run_archive():
    archive()


schedule.every().sunday.at("13:00").do(run_noti)
schedule.every().sunday.at("15:10").do(run_sunday)
schedule.every().wednesday.at("16:00").do(run_thursday)
schedule.every().wednesday.at("17:00").do(run_archive)
#schedule.every().tuesday.at("11:27").do(run_sunday)
#schedule.every().thursday.at("02:53").do(run_thursday)
#schedule.every().thursday.at("03:04").do(run_archive)

while True:
    schedule.run_pending()
    time.sleep(1)
