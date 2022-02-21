import os
import json
import requests
from pandas.io.json import json_normalize
import pandas as pd
from datetime import datetime, date, time, timedelta
import time
import openpyxl

from utils.util import *
 
def count():
    # 필요한 값 : 찾으려는 채널명, oldest, latest, 엑셀 파일 저장명
    print('count!')
    channels = get_channels()
    print('get_channels!')
    #### make DataFrame ####
    all_members = get_all_members(channels)
    print('get_members!')
    #### get members nick ####
    mapping_table = get_mapping_table(all_members)
    print('get_tables!')
    
    map_df = pd.DataFrame.from_dict([mapping_table]).transpose()
    map_df = map_df.sort_index(ascending=True)
    
    # 엑셀파일로 저장
    down_excel(map_df,'mapping_table')
    print('down excel!')

if __name__ == "__main__":
    count()
    	 
