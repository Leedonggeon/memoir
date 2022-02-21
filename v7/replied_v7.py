import os
import json
import requests
from pandas.io.json import json_normalize
import pandas as pd
from datetime import datetime, date, time, timedelta
import time
import openpyxl

from utils.util import *

def merge_excel(term_length):
    #dataframe 
    
    merge_df = load_excel('replied/' + str(1) + '_week_replied')
    for term in range(term_length):
        if term > 1:
            df = load_excel('replied/' + str(term) + '_week_replied')
            merge_df = pd.concat([merge_df, df], axis = 1)
    down_excel(merge_df, 'replied/final'+ '_'+ str(term_length-1))


def count(oldest, latest, term):
    print(str(term) + '주차')
    # 자동화 시작
    
    #### find channels ####
    all_members, df = get_data(oldest, latest)

    #### get members nick ####
    #### 데이터 정의 ####
    replied_df = pd.DataFrame(columns = all_members, index = ['num_replied'])
    user_name = list(replied_df.columns)

    #### 댓글 달린 횟수 카운트 ####
    reply_num = [0 for m in range(len(user_name))]
    data = df.to_dict()
    for id in data['reply_users']:
        user = df['user'][id]
        if str(data['reply_users'][id]) == 'nan':
            num = 0
        else:
            num = len(data['reply_users'][id])

        if all_members.count(user) != 0:
            reply_num[user_name.index(user)] = reply_num[user_name.index(user)] + num
    replied_df.loc['num_replied'] = reply_num
    replied_df = replied_df.transpose() 
    replied_df = replied_df.sort_index(ascending=True)

    down_excel(replied_df, 'replied/' + str(term) + '_week_replied')

def replied():
    oldests, latests = list(), list()
    oldest = datetime(2021, 12, 30, minute = 0) - timedelta(hours=9)
    latest = datetime(2022, 1, 6, minute = 0) - timedelta(hours=9)
    now = datetime.now()
    term_length = 12
    current_term = 0
    oldests, latests = find_time(oldest, latest, interval = 7, term_length = term_length)
    '''    
    for j in range(len(oldests)):        
        if j == 1 or j == 2 or j == 3:          
            oldests[j] = oldests[0]
        elif j == 5 or j == 6 or j == 7:
            oldests[j] = oldests[4]
        elif j == 9 or j == 10 or j == 11:
            oldests[j] = oldests[8]
    '''
    i = 0
    for oldest, latest in zip(oldests, latests):
        i = i + 1
       
#        if now > latest and now < latest + timedelta(days=7): 
        if i == 6:
            oldest = time.mktime(oldest.timetuple())
            latest = time.mktime(latest.timetuple())
            count(oldest, latest, i)
            current_term = i
    merge_excel(current_term+1)
