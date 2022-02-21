import os
import json
import requests
from pandas.io.json import json_normalize
import pandas as pd
from datetime import datetime, date, time, timedelta
import time
import openpyxl

# 환경 변수로 슬랙 토큰을 입력 후 사용해주세요.

FILTERS = ['메모어D', '메모어', '메모어B', '메모어S', '이동건', '박세훈', '김상엽', 'Counting Bot', 'FlaskBot', 'Count',  's1375811068', 'Bot']

# Counting Bot
headers = {"Authorization": 'Bearer ' + token}

def filter_channel(channel_list, filter:str = '토요일'):
    channels = list()
    for id in channel_list['name']:
        if channel_list['name'][id].find(filter) != -1:
            channels.append(channel_list['name'][id])
    return channels

def get_all_channel():
    URL = 'https://slack.com/api/conversations.list'
    # 파라미터
    params = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'types': 'public_channel, private_channel'
        }

    # API 호출
    res = requests.get(URL, params = params, headers=headers)
    channel_list = json_normalize(res.json()['channels'])

    return channel_list

def find_channel(channel_name:str = '1_공지사항'):
    
    channel_list = get_all_channel()
    channel_id = list(channel_list.loc[channel_list['name'] == channel_name, 'id'])[0]
    return channel_id

# 함수 : get all messages
def get_all_messages(channel:str, start_time:str='0', end_time:str=time.time()):
    URL = 'https://slack.com/api/conversations.history'
    # 파라미터
    params = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'channel' : channel,
        'oldest' : start_time,
        'latest' : end_time
            }
    res = requests.get(URL, params = params, headers=headers)
    conversations = pd.DataFrame(columns = ['ts' , 'user', 'text', 'type', 'reply_users'])
    conversations = pd.concat([conversations, json_normalize(res.json()['messages'])], ignore_index=True)
    
    return conversations[['ts','user','text','type', 'reply_users']]

# 함수 : user id -> user nickname
# Bug 누락되는 이름 발생
def change_to_nick(user_id:str):
    URL = 'https://slack.com/api/users.info'
        # 파라미터
    params = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'user' : user_id
            }
    res = requests.get(URL, params = params, headers=headers)
    try:
        user_nick = list(json_normalize(res.json())['user.profile.real_name'])[0]
        return user_nick
    except:
        pass
    return

# 함수 : members
def get_members(channelid):
    URL = 'https://slack.com/api/conversations.members'
        # 파라미터
    params = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'channel' : channelid
        }
    res = requests.get(URL, params = params, headers=headers)
    mem_list = list(json_normalize(res.json())['members'])
    return mem_list[0]

# 함수 : ts - dt
def to_datetime(ts:str):
    date_time = datetime.fromtimestamp(float(ts)).strftime('%Y-%m-%d %H:%M')
    return date_time

# 함수 : download excel file
def down_excel(dataframe, title):
    title = '7_output/' + title + '.xlsx'
    dataframe.to_excel(title, sheet_name = 'sheet1')

def load_excel(title):
    title = '7_output/' + title + '.xlsx'
    dataframe = pd.read_excel(title, index_col = 0)
    return dataframe

# 함수 : make dataframe
def make_data(channel, oldest, latest):
    df1 = get_all_messages(find_channel(channel), oldest, latest)
    col_ts = pd.DataFrame([to_datetime(x) for x in df1['ts']], columns = ['date'])
    col_user = pd.DataFrame([y for y in df1['user']], columns = ['user'])
    del df1['ts']
    del df1['user']
    df1 = pd.concat([col_ts, col_user, df1], axis=1)
    return df1

def get_all_members(channels):
    all_members = []
    for i in range(len(channels)):
        all_members.extend(get_members(find_channel(channels[i])))
    all_members = list(set(all_members))
    # filter 운영진, 봇
    filtered_members = filter_members(all_members)
    return filtered_members

def get_data(oldest, latest):
    channels = get_channels()
    all_members = get_all_members(channels)
    df = pd.DataFrame(columns = ['date' , 'user', 'text', 'type'])
    ###### get members, data ####
    for i in range(len(channels)):
        # make_data : get the data from server
        df = pd.concat([df, make_data(channels[i], oldest, latest)], ignore_index=True)
    return all_members, df

def filter_archived(df, users):
    archives = dict()
    for user in users:
        archives[user] = list()        
    data = df.to_dict()
    for id in data['text']:
        if str(data['text'][id]).find('회고록') != -1 :
            archives[user].append(data['text'][id])
        else :
            if len(data['text'][id]) > 350 and str(data['text'][id]).find('반갑습니다') == -1 and str(data['text'][id]).find('안녕하세요') == -1 :
                archives[user].append(data['text'][id])
    for user in users:
        if len(archives[user]) == 0:
            archives[user].append('X')
    return archives

def filter_completed(df):
    users = list()
    data = df.to_dict()
    for id in data['text']:
        if len(data['text'][id]) > 390:
            users.append(data['user'][id])
    return users

def filter_shorted(df):
    users = list()
    data = df.to_dict()
    for id in data['text']:
        if 1 < len(data['text'][id]) and len(data['text'][id]) < 390:
            users.append(data['user'][id])
    return users

def filter_uncompleted(total_df):
    reasons = dict()
    users = list()
    data = total_df.to_dict()
    for id in data['text']:
        if str(data['text'][id]).find('회고록') != -1 :
            #users.append(data['user'][id])
            continue
        else :
            if len(data['text'][id]) > 300:
                if str(data['text'][id]).find('반갑습니다') == -1 and str(data['text'][id]).find('안녕하세요') == -1 :
                    continue
             #       users.append(data['user'][id])
                else:
                    reasons[data['user'][id]] = '자기소개'
            else:
                reasons[data['user'][id]] = 'under_300'
                
    return reasons

def filter_members(members, filters=FILTERS):
    real_members = []
    
    for member in members:
        is_real = True
        nick = change_to_nick(member)
        for filter in filters:
            if nick.find(filter) != -1:
                is_real = False
        if is_real:
            real_members.append(member)
    return real_members

def get_channels():
    channel_list = get_all_channel().to_dict()
    off_channel_list = filter_channel(channel_list, '회고_offline')
    on_channel_list = filter_channel(channel_list, '회고_online')
    share_channel_list = filter_channel(channel_list, '회고_shareonly')
    channels = off_channel_list + on_channel_list + share_channel_list
    return channels

def get_mapping_table(all_members):
    mapping_table = dict()
    all_members = list(set(all_members))
    # filter 운영진, 봇
    filters = ['메모어D', '메모어', '메모어B', '메모어S', '이동건', '박세훈', '김상엽', 'Counting Bot', 'FlaskBot', 'Count',  's1375811068', 'Bot']
    for member in all_members:
        nick = change_to_nick(member)
        is_real = True
        for filter in filters:
            if nick.find(filter) != -1:
                is_real = False
        if is_real:
            mapping_table[member] = nick
    return mapping_table
'''
def get_all_members_nick(all_members):
    all_members = list(set(all_members))
    all_members_nick = [change_to_nick(member) for member in all_members]
    # filter 운영진, 봇
    filters = ['메모어D', '메모어', '메모어B', '메모어S', '이동건', '박세훈', '김상엽', 'Counting Bot', 'FlaskBot', 'Count',  's1375811068', '전수빈']
    all_members_nick = filter_members(all_members_nick, filters)
    return all_members_nick
'''
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
    
