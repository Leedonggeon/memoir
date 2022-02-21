import os
import json
import requests
from pandas.io.json import json_normalize
import pandas as pd
from datetime import datetime, date, time, timedelta
import time
import openpyxl

from utils.util import *

def process_reply_excel(term_length):
    #dataframe 
    
    before_df = load_excel('reply_check/' + str(term_length) + '_week_reply_check')
    before_data = before_df.to_dict()
    for key in before_data.keys():
        reply_write_num = before_data[key]['reply_num']
        if term_length == 4 or term_length == 8 or term_length == 12:
            reply_check = 'O' if reply_write_num > 7 else 'X'
        else:
            reply_check = 'O' if reply_write_num > 7 else '_'
        before_data[key]['is_reply'] = reply_check + '(' + str(reply_write_num) + ')'
    new_df = pd.DataFrame.from_dict(before_data)
    
    down_excel(new_df.transpose(), 'reply_check/' + str(term_length) + '_week_reply')

def merge_excel(term_length):
    #dataframe 
    merge_df = load_excel('reply_check/' + str(1) + '_week_reply')
    new_merge_df = merge_df.drop(['reply_num'], axis=1)
    for term in range(term_length):
        if term > 1:
            df = load_excel('reply_check/' + str(term) + '_week_reply')
            new_df = df.drop(['reply_num'], axis=1)
            new_merge_df = pd.concat([new_merge_df, new_df], axis = 1)
    down_excel(new_merge_df, 'reply_output_' + str(term_length-1))

def count(oldest, latest, term):
    print(str(term) + '주차')
    all_members, df = get_data(oldest, latest)

    #### 데이터 정의 ####
    fin_df = pd.DataFrame(columns = all_members, index = ['reply_num'])
    reply_list = list(df['reply_users'])
    user_name = list(fin_df.columns)

    #### 댓글 작성 횟수 카운트 ####
    reply_write_num = [0 for m in range(len(user_name))]
    
    for q in reply_list:
        if type(q) == list:
            for p in q:
                if user_name.count(p) != 0:
                    reply_write_num[user_name.index(p)] += 1
    
    fin_df.loc['reply_num'] = reply_write_num

    #### 댓글 여부 체크 ####
    reply_check = []
    for num in reply_write_num:
        reply_check.append('O' if num >= 8 else 'X')
    fin_df.loc['is_reply'] = reply_check
    
    fin_df = fin_df.sort_index(ascending=True)
    
    #### 엑셀파일로 저장 ####
    down_excel(fin_df, 'reply_check/' + str(term) + '_week_reply_check')

def reply():
    oldests, latests = list(), list()
    oldest = datetime(2021, 12, 30, minute = 0) - timedelta(hours=9)
    latest = datetime(2022, 1, 6, minute = 0) - timedelta(hours=9)
    now = datetime.now()
    term_length = 12
    current_term = 0
    oldests, latests = find_time(oldest, latest, interval = 7, term_length = term_length)
    
    for j in range(len(oldests)):        
        if j == 1 or j == 2 or j == 3:          
            oldests[j] = oldests[0]
        elif j == 5 or j == 6 or j == 7:
            oldests[j] = oldests[4]
        elif j == 9 or j == 10 or j == 11:
            oldests[j] = oldests[8]
    i = 0
    for oldest, latest in zip(oldests, latests):
        i = i + 1
       
        if now > latest and now < latest + timedelta(days=7): 
            oldest = time.mktime(oldest.timetuple())
            latest = time.mktime(latest.timetuple())
            count(oldest, latest, i)
            current_term = i

    process_reply_excel(current_term)
    merge_excel(current_term+1)
