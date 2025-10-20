import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime, timedelta

session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504], allowed_methods=["GET","POST","PUT","DELETE","HEAD","OPTIONS"])
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)
session.mount("http://", adapter)

try:
    url1 = 'https://open.fedd'
    url2 = 'on.com/api/edq/stag'
    url3 = 'e/create_stage'
    url = url1 + url2 + url3
    auth1 = "yH5l9Mx9V4NZg"
    auth2 = "JWV5NDI4rfWbmCUPsnh"
    auth = auth1 + auth2
    now = datetime.now()
    print("request time: ", now.strftime("%Y-%m-%d %H:%M:%S"))
    resp = session.post(
        url,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Authorization": auth
        },
        json={
            'items': []
        },
        timeout=60)  # 增加 timeout
    resp.raise_for_status()
    print(resp.text)
except requests.exceptions.RequestException as e:
    print("请求失败：", e)