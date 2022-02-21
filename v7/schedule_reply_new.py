import schedule
import time
from reply_off_sat_v7 import reply_off_sat
from reply_off_sun_v7 import reply_off_sun
from reply_share_v7 import reply_share
from reply_on_v7 import reply_on
from reply_merge_v7 import merge_reply

def run_off_sat_reply():
    reply_off_sat()

def run_off_sun_reply():
    reply_off_sun()

def run_share_reply():
    reply_share()

def run_on_reply():
    reply_on()

def run_merge():
    merge_reply()



#schedule.every().wednesday.at("17:00").do(run_reply)
schedule.every().thursday.at("13:59").do(run_off_sat_reply)
schedule.every().thursday.at("14:30").do(run_off_sun_reply)
schedule.every().thursday.at("14:40").do(run_sharereply)
schedule.every().thursday.at("15:10").do(run_on_reply)
schedule.every().thursday.at("15:10").do(merge_reply)

while True:
    schedule.run_pending()
    time.sleep(1)
