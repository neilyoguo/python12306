# -*- coding: utf-8 -*-


import time
import requests
import os


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from train_info import TrainInfo


#获取selenium版本
import selenium
print(selenium.__version__)

#open chrome

def get_usr_info() -> dict:
    config_file_path = 'config'
    config_dict = {}
    with open(config_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line and '=' in line:
                key, value = line.split('=', 1)  
                config_dict[key.strip()] = value.strip()  
    return config_dict



def station_table(from_station: str, to_station: str) ->tuple:
    path = os.path.join(os.path.dirname(__file__), 'station_name.txt')
    try:
        with open(path, encoding="utf-8") as result:
            info = result.read().split('=')[1].strip("'").split('@')
    except Exception:
        with open(path) as result:
            info = result.read().split('=')[1].strip("'").split('@')
    del info[0]
    station_name = {}
    for i in range(0, len(info)):
        n_info = info[i].split('|')
        station_name[n_info[1]] = n_info[2]
    try:
        from_station = station_name[from_station.encode("utf8")]
        to_station = station_name[to_station.encode("utf8")]
    except KeyError:
        from_station = station_name[from_station]
        to_station = station_name[to_station]
    return from_station, to_station



def get_train_number(train_num: str, list_train_info: list) -> int:
    count = 1
    num = 0
    for item in list_train_info:
        if (item['车次'] == train_num) and (item['一等座'] == '有'or item['一等座'].isdigit())  :
            num = count*2 - 1
            return num
        else :
            count = count + 1
    return num

    
usr_info = get_usr_info()

open_chrome = webdriver.Chrome()

open_chrome.get('https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc')

open_chrome.find_element(By.ID, 'login_user').click()
#账号
open_chrome.find_element(By.ID, 'J-userName').send_keys(usr_info['用户名'])
#密码
open_chrome.find_element(By.ID, 'J-password').send_keys(usr_info['密码'])

open_chrome.find_element(By.ID, 'J-login').click()

time.sleep(1)

open_chrome.find_element(By.ID, 'id_card').send_keys(usr_info['id_card'])
time.sleep(1)
open_chrome.find_element(By.ID, 'verification_code').click()
code = input('验证码:')


open_chrome.find_element(By.ID, 'code').send_keys(code)

open_chrome.find_element(By.ID, 'sureClick').click()

time.sleep(1)

#点击车票预订
open_chrome.find_element(By.ID, 'link_for_ticket').click()

list_info = []
list_train_number = []
train_num = usr_info['车次']
trainInfo = TrainInfo(usr_info['出发地'], usr_info['目的地'],  usr_info['时间'])

# 输出出发站
edit_from_station = open_chrome.find_element(By.ID, 'fromStationText')
edit_from_station.click()
edit_from_station.clear()
edit_from_station.send_keys(usr_info['出发地'])

# 如果需要，使用箭头键在建议列表中导航
edit_from_station.send_keys(Keys.ARROW_DOWN)
edit_from_station.send_keys(Keys.ENTER)


#输入目的地
edit_to_station = open_chrome.find_element(By.ID, 'toStationText')
edit_to_station.click()
edit_to_station.clear()
edit_to_station.send_keys(usr_info['目的地'])
edit_to_station.send_keys(Keys.ENTER)

#输入时间
edit_time = open_chrome.find_element(By.ID, 'train_date')
edit_time.click()
edit_time.clear()
edit_time.send_keys(usr_info['时间'])
while True:

    #查询
    btn = open_chrome.find_element(By.ID, 'query_ticket')
    btn.click()

 
    # open_chrome.refresh()
    list_info,list_train_number = trainInfo.station_info()
    num = get_train_number(train_num , list_info)
    print(num)
    if(num != 0):
        # 等待元素的出现
        time.sleep(1)

        open_chrome.find_element(By.CSS_SELECTOR, f'#queryLeftTable tr:nth-child({num}) .btn72').click()  

        # 等待元素的出现
        time.sleep(1)
        
        #选择一等座， 默认时二等座
        select_seat = open_chrome.find_element(By.ID, 'seatType_1')
        select_seat.send_keys(Keys.ARROW_DOWN)
        select_seat.send_keys(Keys.ENTER)
        

        #选择乘车人
        open_chrome.find_element(By.ID, 'normalPassenger_0').click()
        open_chrome.find_element(By.ID, 'normalPassenger_2').click()

        open_chrome.find_element(By.ID, 'submitOrder_id').click()

        time.sleep(3)
        #确认
        open_chrome.find_element(By.ID, 'qr_submit_id').click()
        break
    time.sleep(1)


input("按回车键继续...")
exit()
