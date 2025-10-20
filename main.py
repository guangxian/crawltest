import requests
import time
import json
from datetime import datetime, timedelta

class Mx:
    def __init__(self):
        pass

    def get_data(self):
        api_url = "http://xxfb.mwr.cn/hydroSearch/mapSearch"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        payload = {
            "name": '罗江'  # 可根据需求动态生成
        }
        response = requests.post(
            api_url,
            json=payload,  # 自动设置 JSON 格式并序列化
            headers=headers,
            timeout=10
        )
        data = response.json()
        self.format_data(data)

    def format_data(self, data):
        items = []
        for i, v in enumerate(data.get('result', [])):
            river_water_level = ''
            reservoir_water_level = ''
            reservoir_fluctuation = ''
            if v['stType'] == 'river':
                site_type = 'RIVER'
                site_type_desc = '河道站'
                river_water_level = str(v['z'])
            elif v['stType'] == 'rsvr':
                site_type = 'RESERVOIR'
                site_type_desc = '水库站'
                reservoir_water_level = str(v['rz'])
                reservoir_fluctuation = str(v['rzRange'])
            else:
                site_type = 'unknown'
                site_type_desc = '站点类型未知'

            row = {
                'siteType': site_type,
                'riverWaterLevel': river_water_level,
                'reservoirWaterLevel': reservoir_water_level,
                'reservoirFluctuation': reservoir_fluctuation,
                'createTime': v['createTime'],
                'idNo': str(v['idNo']),
            }
            items.append(row)
        formatted_data = {
            'crawlNo': datetime.now().strftime("%Y-%m-%d"),
            'items': items
        }
        self.req(formatted_data)

    def req(self, data):
        url = 'https://open.feddon.com/api/edq/tide/tide/create_tide'
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Authorization": 'yH5l9Mx9V4NZgJWV5NDI4rfWbmCUPsnh'
        }
        response = requests.post(
            url=url,
            json=data,
            headers=headers,
            timeout=300
        )
        response.raise_for_status()
        response_data = response.json()
        print("request result: ", response_data)

    def go(self):
        now = datetime.now()
        print("request time: ", now.strftime("%Y-%m-%d %H:%M:%S"))
        self.get_data()

if __name__ == '__main__':
    m = Mx()
    m.go()

    # date_str = datetime.now().strftime("%Y-%m-%d")
    # print(date_str)  # 输出示例：2025-10-19