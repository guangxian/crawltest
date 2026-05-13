import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# 请求的 URL
# url = "http://localhost:8080/user/login"  # 示例接口，用于测试
url = "http://localhost:8080/site/get_site"  # 示例接口，用于测试

# 要发送的 JSON 数据（入参）
payload = {
    "code": "89360",
    "id": "1"
}

# 设置请求头，表明发送的是 JSON 数据
headers = {
    "Content-Type": "application/json",
    # "Authorization": "89360",
    "Authorization": "yH5l9Mx9V4NZgJWV5NDI4rfWbmCUPsnh"
}

def send_post_request(data):
    try:
        response = requests.post(
            url,
            data=json.dumps(data),
            headers=headers,
            timeout=10  # 避免请求卡死
        )
        response.raise_for_status()
        return response.json()  # 返回 JSON 响应
    except Exception as e:
        return {"error": str(e)}

# 并发发送 10 次请求
if __name__ == "__main__":
    t=10
    with ThreadPoolExecutor(max_workers=t) as executor:
        # 提交 10 个任务
        futures = [executor.submit(send_post_request, payload) for _ in range(t)]

        # 获取结果
        for i, future in enumerate(as_completed(futures)):
            result = future.result()
            print(f"请求 {i+1} 结果: {result}")