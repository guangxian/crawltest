import requests
import time
import json
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class Mx:
    def __init__(self):
        pass

    def get_station(self):
        url1 = 'https://open.fedd'
        url2 = 'on.com/api/edq/tid'
        url3 = 'e/station/list_station'
        url = url1 + url2 + url3
        auth1 = "yH5l9Mx9V4NZg"
        auth2 = "JWV5NDI4rfWbmCUPsnh"
        auth = auth1 + auth2
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Authorization": auth
        }
        session = requests.Session()

        payload = {
            'country': '中国',
            'pageSize': 1000,
        }

        try:
            resp = session.post(
                url=url,
                headers=headers,
                json=payload,
                timeout=300)  # 增加 timeout
            resp.raise_for_status()
            response_data = resp.json()
            # print(response_data)
            self.get_tide(response_data)
        except requests.exceptions.RequestException as e:
            print("请求失败：", e)

    def get_tide(self, data):
        stations = data['data']['items']
        start = datetime.strptime('2025-10-20', '%Y-%m-%d')
        end = datetime.strptime('2025-11-21', '%Y-%m-%d')
        tides = []
        # 使用列表推导式
        dates = [(start + timedelta(days=x)).strftime('%Y-%m-%d')
                 for x in range((end - start).days + 1)]
        for _station in stations[:10]:
            if _station['code'] != 'T1933333333333':
                for _date in dates:
                    time.sleep(0.1)
                    url1 = 'https://publict'
                    url2 = 'ide.nmdis.o'
                    url3 = 'rg.cn/Tide/GetTideData'
                    url = url1 + url2 + url3
                    headers = {
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    }
                    payload = {
                        "Date": _date,
                        "PortCode": _station['code'],
                        "TideType": '0',
                    }
                    response = requests.post(
                        url=url,
                        json=payload,
                        headers=headers,
                        timeout=300
                    )
                    response_data = response.json()
                    # 第一步：把 Data 字段的字符串解析成真正的 JSON 对象
                    try:
                        # 解析 Data 字符串
                        parsed_data = json.loads(response_data["Data"])

                        # 第二步：构建一个“干净”的最终结果，把 Data 替换为解析后的对象
                        clean_result = {
                            "FollowState": response_data["FollowState"],
                            "Code": response_data["Code"],
                            "Data": parsed_data  # 替换为已解析的字典
                        }

                        # 第三步：格式化输出整个结果（取消转义，美化结构）
                        # print(json.dumps(clean_result, indent=4, ensure_ascii=False))

                        hours = [clean_result['Data']['data'][f'a{i}'] for i in range(24)]

                        tideTimes = [
                            {
                                'time': clean_result['Data']['data'][f'cs{i}'],
                                'height': clean_result['Data']['data'][f'cg{i}']
                            }
                            for i in range(4)
                        ]
                        tides.append({
                            'stationName': _station["name"],
                            'date': _date,
                            # 'lunar': to_lunar.solar_str_to_chinese_lunar(_date),
                            'hours': hours,
                            'tideTimes': tideTimes,
                        })

                    except json.JSONDecodeError as e:
                        print("JSON 解析失败:", e)
                        print("原始 Data 内容:", response_data["Data"])

        next_data = {
            'items': tides,
            'count': len(tides)
        }
        self.add_tide(next_data)
        # print(data)

    def add_tide(self, data):
        url1 = 'https://open.fedd'
        url2 = 'on.com/api/edq/tid'
        url3 = 'e/tide/create_tide'
        url = url1 + url2 + url3
        auth1 = "yH5l9Mx9V4NZg"
        auth2 = "JWV5NDI4rfWbmCUPsnh"
        auth = auth1 + auth2
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Authorization": auth
        }
        session = requests.Session()

        try:
            resp = session.post(
                url=url,
                headers=headers,
                json=data,
                timeout=900)  # 增加 timeout
            resp.raise_for_status()
            print(resp.json())
        except requests.exceptions.RequestException as e:
            print("请求失败：", e)

    def go(self):
        now = datetime.now()
        print("request time: ", now.strftime("%Y-%m-%d %H:%M:%S"))
        self.get_station()

if __name__ == '__main__':
    m = Mx()
    m.go()