import requests
import time
import json
from datetime import datetime, timedelta, timezone
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import random

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

    def start(self):
        self.check_crawl_no()

    def general_url(self):
        return ('https://open.fedd' +
                'on.com/a' +
                'pi/edq/')

    def general_key(self):
        return ('yH5l9Mx9V4NZg' +
                'JWV5NDI4rf' +
                'WbmCUPsnh'
                )

    def check_crawl_no(self):
        print('check_crawl_no 检查采集号是否已存在')
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
        print('start_crawl 开始采集')
        api_url1 = "http://xxfb.mw"
        api_url2 = "r.cn/hydroSe"
        api_url3 = "arch/mapSearch"
        url = api_url1 + api_url2 + api_url3
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        payload = {
            "name": '周堂桥'  # 可根据需求动态生成
        }

        response = requests.post(url, json=payload, headers=headers, timeout=100)
        if response.status_code == 200:
            print("请求成功")
            data = response.json()
            result = data.get('result', [])
            print(f'result长度: {len(result)}')
            if len(result) > 0:
                checked = self.check_is_target_date(result)
                if checked:
                    self.insert_data(result)
            else:
                print(f'结束任务')
        else:
            print(f"请求失败，状态码：{response.status_code}")
            print("响应内容：", response.text)

    def check_is_target_date(self, items):
        print('check_is_target_date 检查采集的数据中的日期是否为指定日期')
        checked = False
        if len(items) > 0:
            random_numbers = [random.randint(0, len(items)) for _ in range(3)]
            for number in random_numbers:
                print(f'随机抽查成员的创建日期是否为今日，抽查对象，i: {number}, stnm: {items[number]['stnm']}')
                print(f'随机抽查成员的创建日期是否为今日，抽查对象，i: {number}, createTime: {items[number]['createTime']}')
                checked = self.is_today(items[number]['createTime'])
                if not checked:
                    print(f'不通过')
                    break
        return checked

    def insert_data(self, items):
        print('insert_data 插入数据')
        data = {
            'result': items
        }
        self.format_data(data)

    def is_today(self, target_time_str):
        # target_time_str = '2026-06-21 10:20:28'

        # 1. 定义固定的东八区 (UTC+8)
        beijing_tz = timezone(timedelta(hours=8))

        # 2. 解析字符串并赋予北京时区
        target_time = datetime.strptime(target_time_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=beijing_tz)

        # 3. 获取当前的北京时间
        now_beijing = datetime.now(beijing_tz)

        # 4. 比较日期部分
        is_today = target_time.date() == now_beijing.date()

        # print(f"当前北京时间: {now_beijing.strftime('%Y-%m-%d %H:%M:%S')}")
        # print(f"是否为今天: {is_today}")
        return is_today

if __name__ == '__main__':
    m = Mx()
    # m.check_crawl_no()
    m.start()