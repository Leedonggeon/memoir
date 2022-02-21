import os
import json
import requests
from pandas.io.json import json_normalize
import pandas as pd
from datetime import datetime, date, time, timedelta
import time
import openpyxl

from utils.util import *

def merge_excel_archive(term_length):
    #dataframe 
    merge_df = load_excel('archive/' + str(1) + 'th_archiving')
    for term in range(term_length):
        if term > 1:
            df = load_excel('archive/' + str(term) + 'th_archiving')
            merge_df = pd.concat([merge_df, df], axis = 1)
    down_excel(merge_df, 'archiving'+ '_' + str(term_length-1))


def update_archive_df(archive_df, archives, users):
    for user in users:
        archive_df[user] = archives[user][0]
    return archive_df

def do_archive(oldest, latest, term):
    print(str(term) + '주차')
    #### make DataFrame ####
    all_members, df = get_data(oldest, latest)

    archives = filter_archived(df, all_members)
    archive_df = pd.DataFrame(columns = all_members)
    
    archive_df.loc['archive_' + str(term) + 'th'] = 'X'
    archive_df = update_archive_df(archive_df, archives, all_members)
    archive_df = archive_df.transpose()
    archive_df = archive_df.sort_index(ascending=True)

    # 엑셀파일로 저장
    down_excel(archive_df,'archive/' + str(term) + 'th_archiving')
    
def find_time(oldest, latest, interval, term_length):
    oldests, latests = list(), list()
    oldests.append(oldest)
    latests.append(latest)

    for i in range(term_length-1):
        oldest = oldest + timedelta(days=interval)
        oldests.append(oldest)
        latest = latest + timedelta(days=interval)
        latests.append(latest)
    return oldests, latests
    
def archive():
    oldests, latests = list(), list()
    oldest = datetime(2021, 12, 30, minute = 0) - timedelta(hours=9)
    latest = datetime(2022, 1, 6, minute = 0) - timedelta(hours=9)
     
    now = datetime.now()
    term_length = 13
    oldests, latests = find_time(oldest, latest, interval = 7, term_length = term_length)

    current_term = 0
    i = 0 
    for oldest, latest in zip(oldests, latests):
        i = i + 1
        if now > latest and now < latest + timedelta(days=2):    
            oldest = time.mktime(oldest.timetuple())
            latest = time.mktime(latest.timetuple())
            do_archive(oldest, latest, i)
            current_term = i
    
    merge_excel_archive(current_term+1)    
    
