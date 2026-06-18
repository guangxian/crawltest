import requests
import time
import json
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class Mx:
    def __init__(self):
        pass

    def get_data(self):
        api_url1 = "http://xxfb.mw"
        api_url2 = "r.cn/hydroSe"
        api_url3 = "arch/mapSearch"
        api_url = api_url1 + api_url2 + api_url3
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        payload = {
            "name": '周堂桥'  # 可根据需求动态生成
        }
        response = requests.post(
            api_url,
            json=payload,  # 自动设置 JSON 格式并序列化
            headers=headers,
            timeout=100
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
        url = self.general_url() + "stage/create_stage"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Authorization": self.general_key()
        }
        session = requests.Session()
        # retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504],
        #                 allowed_methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"])
        # adapter = HTTPAdapter(max_retries=retries)
        # session.mount("https://", adapter)
        # session.mount("http://", adapter)

        try:
            resp = session.post(
                url=url,
                headers=headers,
                json=data,
                timeout=300)  # 增加 timeout
            resp.raise_for_status()
            print(resp.text)
        except requests.exceptions.RequestException as e:
            print("请求失败：", e)

    def go(self):
        now = datetime.now()
        print("request time: ", now.strftime("%Y-%m-%d %H:%M:%S"))
        self.get_data()

    def general_url(self):
        return 'https://open.fedd' + 'on.com/api/edq/'
        pass

    def general_key(self):
        return 'yH5l9Mx9V4NZg' + 'JWV5NDI4rfWbmCUPsnh'
        pass

    def check_crawl_no(self):
        print('check_crawl_no')
        url = self.general_url() + "stage/has_crawl_no"
        payload = {
            "crawlNo": datetime.now().strftime("%Y-%m-%d"),
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Authorization": self.general_key(),
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            # 解析 JSON 响应为 Python 字典
            result = response.json()
            print("请求成功，返回数据：", result)
            if result['code'] == 0:
                if result['data']['exists']:
                    print('采集号已存在，结束本次任务')
                else:
                    print('采集号不存在，可以采集')
                    self.start_crawl()
            else:
                print('code != 0, 结束任务')

        else:
            print(f"请求失败，状态码：{response.status_code}")
            print("响应内容：", response.text)

    def start_crawl(self):
        print('start_crawl')
        self.get_data()

if __name__ == '__main__':
    m = Mx()
    # m.go()


    m.check_crawl_no()
    # print(datetime.now().strftime("%Y-%m-%d"))