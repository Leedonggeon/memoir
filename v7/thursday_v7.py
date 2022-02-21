import os
import json
import requests
from pandas.io.json import json_normalize
import pandas as pd
from datetime import datetime, date, time, timedelta
import time
import openpyxl

from utils.util import *
# 환경 변수로 슬랙 토큰을 입력 후 사용해주세요.

def merge_excel_memoir(term_length):
    #dataframe 
    merge_df = load_excel('memoir/' + str(1) + '_week_check')
    for term in range(term_length+1):
        if term > 1:
            df = load_excel('memoir/' + str(term) + '_week_check')
            merge_df = pd.concat([merge_df, df], axis = 1)
    down_excel(merge_df, 'memoir_check'+ '_'+ str(term_length))

def count(oldest, latest, edit_start, late_latest, term):
    print(str(term) + '주차')
   
    #### make DataFrame ####
    all_members, df = get_data(oldest, latest)

    #### 회고 지각 제출 ####
    users = filter_completed(df)
    user_completed = list(set(users))
    user_completed = filter_members(user_completed)

    on_time_df = load_excel('memoir/' + str(term) + '_week_check')
    on_time_df = on_time_df.transpose()
    for _ in user_completed:
        if on_time_df[_]['memoir_'+str(term)+'th'] == 'X':
            on_time_df.loc['memoir_'+str(term)+'th', _] = 'L'

    sunday_all_members, sunday_df = get_data(edit_start, oldest)

    sunday_users = filter_completed(sunday_df)
    sunday_user_completed = list(set(sunday_users))
    sunday_user_completed = filter_members(sunday_user_completed)
    for _ in sunday_user_completed:
        if on_time_df[_]['memoir_'+str(term)+'th'] == 'S':
            on_time_df.loc['memoir_'+str(term)+'th', _] = 'E'

    user_shorted = filter_shorted(df)
    user_shorted = filter_members(user_shorted)
    for _ in user_shorted:
        if on_time_df[_]['memoir_'+str(term)+'th'] == 'X':
            on_time_df.loc['memoir_'+str(term)+'th', _] = 'S'


    fin_df = on_time_df.transpose()
    fin_df = fin_df.sort_index(ascending=True)
    
    # 엑셀파일로 저장
    down_excel(fin_df,'memoir/' + str(term) + '_week_check')
    
def thursday():
    oldests, latests, edit_starts, late_latests = list(), list(), list(), list()
#    oldest = datetime(2021, 12, 27, minute = 10)
    oldest = datetime(2022, 1, 3, minute = 10) - timedelta(hours=9)
    latest = datetime(2022, 1, 6, minute = 0) - timedelta(hours=9)
    edit_start = latest - timedelta(days=7)
    late_latest = datetime(2022, 1, 10, minute = 0) - timedelta(hours=9)
     
    term_length = 13
    oldests, latests = find_time(oldest, latest, interval = 7, term_length = term_length)
    edit_starts, late_latests = find_time(edit_start, late_latest, interval = 7, term_length = term_length)
    now = datetime.now()
    i = 0
    current_term  = 1
    for oldest, latest, edit_start, late_latest in zip(oldests, latests, edit_starts, late_latests):
        i = i + 1
        if now > oldest and now < late_latest:
            oldest = time.mktime(oldest.timetuple())
            latest = time.mktime(latest.timetuple())
            edit_start = time.mktime(edit_start.timetuple())
            late_latest = time.mktime(late_latest.timetuple())
            count(oldest, latest, edit_start, late_latest, i)
            current_term = i
    if current_term >= 1:
        merge_excel_memoir(current_term)    

    
