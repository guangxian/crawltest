import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504], allowed_methods=["GET","POST","PUT","DELETE","HEAD","OPTIONS"])
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)
session.mount("http://", adapter)

try:
    resp = session.post(
        "https://open.feddon.com/api/edq/stage/create_stage",
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Authorization": 'yH5l9Mx9V4NZgJWV5NDI4rfWbmCUPsnh'
        },
        json={
            'items': []
        },
        timeout=60)  # 增加 timeout
    resp.raise_for_status()
    print(resp.text)
except requests.exceptions.RequestException as e:
    print("请求失败：", e)