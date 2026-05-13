import requests
import time
import json
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import os
from pathlib import Path
from poi import Poi

"""
    站点名称：四川省水文水资源勘测中心
    站点地址：http://www.schwr.com:8088/rsvr
    更新时间：每日9时
"""
class Mx:
    def __init__(self):
        pass

    def get_data(self):
        api_url = "http://www.schwr.com:8088/api/sl/stRsvrR/listNew?t=1764569108023"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        payload = {}
        response = requests.get(
            api_url,
            json=payload,  # 自动设置 JSON 格式并序列化
            headers=headers,
            timeout=100
        )
        data = response.json()

        print(Path(__file__).stem)

        if len(data) > 0:
            with open(f'{Path(__file__).stem}_original.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        return data['result']

        # self.format_data(data['result'])

    def format_data(self, data):
        items = []
        for v in data:
            site_type = 'RESERVOIR'
            target_id = 'www.schwr.com'
            out_id = v['stcd']
            reservoir_water_level = v['rz']
            create_time = datetime.fromtimestamp(v['tm'] / 1000).strftime("%Y-%m-%d %H:%M:%S")
            row = {
                'siteType': site_type,
                'targetId': target_id,
                'outId': out_id,
                'reservoirWaterLevel': reservoir_water_level,
                'createTime': create_time,
            }
            items.append(row)

        formatted_data = {
            'crawlNo': f'{datetime.now().strftime('%Y-%m-%d')}_www.schwr.com',
            'items': items
        }

        with open(f'{Path(__file__).stem}_format.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def import_station(self):
        data = self.get_data()
        items = []
        for i, v in enumerate(data):
            # site_type = 'RESERVOIR'
            # target_id = 'www.schwr.com'
            # out_id = v['stcd']
            # reservoir_water_level = v['rz']
            # create_time = datetime.fromtimestamp(v['tm'] / 1000).strftime("%Y-%m-%d %H:%M:%S")
            if i < 2:
                poi_instance = Poi()
                addr = poi_instance.bd(lat=v['lttd'], lng=v['lgtd'])
                print(addr)
            row = {
                'name': v['stnm'],
                'type': 'RESERVOIR',
                'province': addr['province'],
                'city': addr['city'],
                'district': addr['district'],
                'town': addr['town'],
                'adcode': addr['adcode'],
                'longitude': v['lgtd'],
                'latitude': v['lttd'],
                'riverName': v['rvnm'],
                'watershedName': v['hnnm'],
                'outId':  v['stcd'],
                'targetId': 'www.schwr.com',
            }
            items.append(row)

        formatted_data = {
            'items': items
        }
        with open(f'station_format.json', 'w', encoding='utf-8') as f:
            json.dump(formatted_data, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    print("request time: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    m = Mx()
    m.import_station()