"""
优化循环采集导致的部分失败
"""
import requests
import time
import json
from datetime import datetime, timedelta
import base64
import random
import binascii

class TideV2:
    def __init__(self):
        self.headers = { "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" }
        self.a_e_u = "GYYTIOBVGIZTANRTGQ4DIZBTGY2GGNZZGM4TONZWGQ2TONDBG4ZTMMJVG42GKMZQGYYTKNZVGI3GGNDDGZSDGNJXGQ2WCNBXGZRTOYJUMM3GIMZZG44TKYJXHEZTKNTBGYZDMOJTHE2TKNRRGU3TKMRWMM2GGMZQGY2DMYZWGQ2DMNJSG4YDKYJUG42TMNBVGU4TKOBVGI3DQ==="
        self.a_i_u = "GYYTIOBVGIZTANRTGQ4DIZBTGY2GGNZZGM4TONRWGM2DONJWG42TIYZWMQ2WCNTDGVQTINZVGI3TMNRSGY4TGNJWME3DEMZSGMYDONRVHE2TQNBSG4YDIYZTGI2TMNTCGYZTKMZTHAZWI==="
        self.a_i_k = "GY2TKNJWG4ZTCNRSGQ2DMYZUMU3DKNBUGZRTKNZUMU2DKMZVGYYTKYJTGA3TANJYGU3DMYJVGY2GMNJSGQ2TMYRTGA3DGNTEGVQTKOBVHE3GIMZRGQ2DKNRVGY2DEN3BGYZDMZBWG4ZWI==="
        pass

    def k(self, str):
        return base64.b64decode(binascii.unhexlify(base64.b32decode(str))).decode('utf-8')

    def get_requirements(self):
        """先获取需要查询的日期集合（本地）"""
        """
        items = [
            {
                "port_code": "T004",
                "dates": ["2026-07-13", "2026-07-14", "2026-07-17", "2026-07-18"]
            },
            {
                "port_code": "T187",
                "dates": ["2026-07-13", "2026-07-14", "2026-07-17", "2026-07-18"]
            }
        ]
        """
        print("第一步：检查缺失数据")

        # 获取当前日期
        today = datetime.now()

        # 计算N天前和N天后的日期
        start = today - timedelta(days=2)
        end = today + timedelta(days=2)

        # 格式化为 'YYYY-MM-DD' 的字符串形式
        str_start = start.strftime('%Y-%m-%d')
        str_end = end.strftime('%Y-%m-%d')

        payload = {
            "start": str_start,
            "end": str_end,
            "portCode": "T193"
        }

        headers = self.headers
        headers["Authorization"] = self.k(self.a_i_k)
        session = requests.Session()

        try:
            resp = session.post(
                url = self.k(self.a_i_u) + "tide/tide/get_missing",
                headers = headers,
                json = payload,
                timeout = 300)  # 增加 timeout
            resp.raise_for_status()
            response_data = resp.json()
            # print(response_data)

            if len(response_data['data']['items']) > 0:
                # 使用列表推导式进行格式化
                format_data = [
                    {
                        'dates': item['missingDates'],
                        'port_code': item['portCode']
                    }
                    for item in response_data['data']['items']
                ]
                self.get_tide(format_data)
            else:
                print("无缺失，任务结束")
        except requests.exceptions.RequestException as e:
            print("请求失败：", e)

    def get_tide(self, items):
        """获取潮汐（采集）"""
        print("第二步：获取数据")
        url = self.k(self.a_e_u)
        response_datas = []
        headers = self.headers
        session = requests.Session()

        for item in items:
            port_code = item["port_code"]
            for date in item["dates"]:
                # print(f"准备获取... 港口代码: {port_code}, 日期: {date}")
                payload = {"Date": date, "PortCode": port_code, "TideType": "0"}

                # 2. 为单个请求增加重试逻辑
                success = False
                for attempt in range(3):  # 最多重试 3 次
                    try:
                        resp = session.post(url=url, headers=headers, json=payload, timeout=10)
                        resp.raise_for_status()
                        response_data = resp.json()
                        response_datas.append(response_data)
                        success = True
                        # print(f"成功获取: {port_code} - {date}")
                        break  # 成功后跳出重试循环
                    except requests.exceptions.RequestException as e:
                        # print(f"第 {attempt + 1} 次请求失败: {e}")
                        if attempt < 2:  # 如果不是最后一次尝试，则等待后重试
                            time.sleep(2 + random.uniform(0, 1))  # 等待 2-3 秒再重试

                if not success:
                    print(f"彻底失败，已记录: {port_code} - {date}")
                    # 可以将失败的任务记录到文件或数据库，以便后续补采
                    # failed_tasks.append({"port_code": port_code, "date": date})

                # 3. 在每次请求后增加随机延时，避免请求过于频繁
                time.sleep(random.uniform(0.1, 1))

        self.transform_data(response_datas)

    def transform_data(self, response_datas):
        print("第三步：转换数据")
        tides = []
        for response_data in response_datas:
            # print(response_data)
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
                    for i in range(6)
                    if clean_result['Data']['data'][f'cs{i}'] is not None # 过滤潮时潮高为null的
                ]
                tides.append({
                    'portCode': clean_result['Data']['report']["SiteCode"],
                    'date': str(clean_result['Data']['report']['Year']) + "-" + str(clean_result['Data']['report']['Month']).zfill(2) + "-" + str(clean_result['Data']['data']['Day']).zfill(2),
                    # 'lunar': to_lunar.solar_str_to_chinese_lunar(_date),
                    'hours': hours,
                    'tideTimes': tideTimes,
                })

            except json.JSONDecodeError as e:
                print("JSON 解析失败:", e)
                print("原始 Data 内容:", response_data["Data"])

        self.add_tide({
            'items': tides,
            'count': len(tides)
        })

    def add_tide(self, data):
        """添加潮汐（本地）"""
        print("第四步：添加数据")
        # print(data)
        payload = {
            "items": data["items"]
        }

        headers = self.headers
        headers["Authorization"] = self.k(self.a_i_k)

        try:
            resp = requests.post(url=self.k(self.a_i_u) + "tide/tide/create_tide_v2", headers=headers, json=payload, timeout=300)  # 增加 timeout
            resp.raise_for_status()
            response_data = resp.json()

            if response_data['code'] == 0:
                print(f"任务结束，总共创建：{response_data["data"]["total"]}条")
            else:
                print(f"任务结束，但有错误，提示：{response_data["msg"]}")

        except requests.exceptions.RequestException as e:
            print("请求失败：", e)

if __name__ == '__main__':
    m = TideV2()
    m.get_requirements()