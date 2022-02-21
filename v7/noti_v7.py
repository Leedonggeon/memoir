import os
import json
import requests
from pandas.io.json import json_normalize
import pandas as pd
from datetime import datetime, date, time, timedelta
import time
import openpyxl

from utils.util import *
 
def count(oldest, latest, term):
    print(str(term) + '주차')
    # 필요한 값 : 찾으려는 채널명, oldest, latest, 엑셀 파일 저장명
    
    #### make DataFrame ####
    all_members, df = get_data(oldest, latest)

    #### 회고 정상 제출 ####
    users = filter_completed(df)
    user_completed = list(set(users))
    user_short = filter_shorted(df)
    
    user_uncompleted = [j for j in all_members if j not in user_completed]
    fin_df = pd.DataFrame(columns = all_members)
    
    fin_df.loc['noti_' + str(term) + 'th'] = 'O'
    for _ in user_uncompleted:
        if _ in user_short:
            fin_df.loc['noti_' + str(term) + 'th', _] = 'S'
        else:
            fin_df.loc['noti_' + str(term) + 'th', _] = 'X'
    fin_df = fin_df.transpose()
    
    # sorting
    fin_df = fin_df.sort_index(ascending=True)
    
    # 엑셀파일로 저장
    down_excel(fin_df,'noti/' + str(term) + '_week_check')

def noti():
    print('noti!')
    oldests, latests, late_oldest, late_latest = list(), list(), list(), list()
    oldest = datetime(2021, 12, 30, minute = 0) - timedelta(hours=9)
    latest = datetime(2022, 1, 3, minute = 0) - timedelta(hours=11)
    late_oldest = latest
    late_latest = datetime(2022, 1, 6, minute = 0) - timedelta(hours=9)
    
    now = datetime.now()

    term_length = 13
    oldests, latests = find_time(oldest, latest, interval = 7, term_length = term_length)
    late_oldests, late_latests = find_time(late_oldest, late_latest, interval = 7, term_length = term_length)
    i = 0
    for oldest, latest, late_oldest, late_latest in zip(oldests, latests, late_oldests, late_latests):
        i = i + 1
        if now > oldest and now < late_latest:
            oldest = time.mktime(oldest.timetuple())
            latest = time.mktime(latest.timetuple())
            count(oldest, latest, i)
    	 
