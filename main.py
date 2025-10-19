import requests
import time
import json
from datetime import datetime, timedelta

class Mx:
    def __init__(self):
        pass

    def w(self, path, data):
        if len(data) > 0:
            data['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

    def r(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def go(self):
        # data = self.r('tides.json')
        url = 'https://open.feddon.com/api/edq/tide/tide/test'
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Authorization": 'yH5l9Mx9V4NZgJWV5NDI4rfWbmCUPsnh'
        }
        response = requests.post(
            url=url,
            json={},
            headers=headers,
            timeout=153
        )
        response.raise_for_status()
        # response_data = response.json()
        # print(response_data)

if __name__ == '__main__':
    m = Mx()
    m.go()