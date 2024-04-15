
import time
import requests
import os
import datetime


class TrainInfo:
    def __init__(self, from_station, to_station, train_date):
        self.from_station = from_station
        self.to_station = to_station
        self.train_date = train_date
            
    def station_table_to_en(self, from_station, to_station):
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
            from_station_en = station_name[from_station.encode("utf8")]
            to_station_en = station_name[to_station.encode("utf8")]
        except KeyError:
            from_station_en = station_name[from_station]
            to_station_en = station_name[to_station]
        return from_station_en, to_station_en
    
    def station_info(self):
        from_station_en, to_station_en = self.station_table_to_en(self.from_station, self.to_station)
        
        #URL可能会随时变动，必要时要更改下
        URL = "https://kyfw.12306.cn/otn/leftTicket/queryG?"
        URL = URL + f"leftTicketDTO.train_date={self.train_date}&leftTicketDTO.from_station={from_station_en}&leftTicketDTO.to_station={to_station_en}&purpose_codes=ADULT"
        headers = {
            #使用时cookie 根据实际的来
            "Cookie" : "_uab_collina=171274396125986918807303; JSESSIONID=6305D5F1A0EE9EE50D21993A8F53488E; BIGipServerpassport=1005060362.50215.0000; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; route=9036359bb8a8a461c164a04f8f50b252; BIGipServerotn=1943601418.24610.0000; _jc_save_fromStation=%u897F%u5B89%2CXAY; _jc_save_toStation=%u97E9%u57CE%2CHCY; _jc_save_fromDate=2024-04-11; _jc_save_toDate=2024-04-10; _jc_save_wfdc_flag=dc" ,
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

        resp = requests.get(URL, headers=headers)
        http_status = resp.status_code
        print(http_status)
        if(http_status == 200):
            json_data =resp.json()
            result  = json_data['data']['result']
            list_info = []
            list_train_number = []
            for i in result:
                index = i.split('|')
                #车次
                num = index[3] 
                list_train_number.append(num)
                #出发站
                from_station = index[6]
                #到达站
                to_station = index[7]
                #出发时间
                start_time = index[8]
                #到达时间
                end_time = index[9]
                #耗时
                offset_time = index[10]
                #商务座特等座
                top_seat = index[32]
                #一等
                first_seat = index[31]
                #二等座二等包座
                second_seat = index[30]
                #高级软卧
                #无座
                no_seat = index[26]
                #其他 
                dit_info = {    
                    '车次' : num ,
                    '出发站' : from_station ,
                    '到达站' : to_station ,
                    '出发时间' : start_time ,
                    '到达时间' : end_time,
                    '耗时' : offset_time ,
                    '商务座特等座' : top_seat , 
                    '一等座' : first_seat ,
                    '二等座' : second_seat       
                }
                list_info.append(dit_info)
            print(datetime.datetime.now())
            print(list_info)
            print(list_train_number)
            return list_info,list_train_number
        else:
            print(f"http request error, http_status = {http_status}")
        
if __name__ == "__main__":
    
    date_info  = datetime.date.today()

    trainInfo = TrainInfo('西安', '韩城', date_info)
    trainInfo.station_info()
