import requests
import json

class A:
    def __init__(self):
        pass

    def get_detail(self):
        url = 'https://www.bkdiao.com/wp-admin/admin-ajax.php'
        headers = {
            'User-Agent': 'Mozilla/5.0',
            # 'Cookie': 'Hm_lvt_ca860721dce125856eb54faa9f7565a1=1786700246; HMACCOUNT=894AB083B6956AD6; prefers-color-scheme=light; bkdiao_spot_view_4748=1; bkdiao_spot_view_4608=1; Hm_lpvt_ca860721dce125856eb54faa9f7565a1=1786700741'
            # 'Referer': 'HangZhou'
        }
        params = {
            'action': 'bkdiao_get_spot_viewport_details',
            'ids': '5012,4581'
        }
        response = requests.get(url, headers=headers, params=params, timeout=30)

        data = response.json()

        print(data)


    def get_list(self):
        url = 'https://www.bkdiao.com/wp-admin/admin-ajax.php'
        headers = {
            'User-Agent': 'Mozilla/5.0',
            # 'Cookie': 'Hm_lvt_ca860721dce125856eb54faa9f7565a1=1786700246; HMACCOUNT=894AB083B6956AD6; prefers-color-scheme=light; bkdiao_spot_view_4748=1; bkdiao_spot_view_4608=1; Hm_lpvt_ca860721dce125856eb54faa9f7565a1=1786700741'
            'Referer': 'HangZhou'
        }
        # params = {
        #     'action': 'bkdiao_get_spots_in_bounds',
        #     'west': 104.63530364,
        #     'east': 106.27546636,
        #     'south': 30.743205,
        #     'north': 31.023704,
        #     'limit': 320
        # }
        params = {
            'action': 'bkdiao_get_spots_in_bounds',
            'west': 62.01484884,
            'east': 145.46371416,
            'south': 24.558246360000002,
            'north': 42.888923639999994,
            'limit': 10000
        }
        response = requests.get(url, headers=headers, params=params, timeout=30)

        data = response.json()

        # print(data)

        if data.get('success'):
            print(f'len: {len(data.get("data"))}')
            # with open('result.json', 'w', encoding='utf-8') as f:
            #     json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            print('error...')

if __name__ == "__main__":
    a = A()
    a.get_list()


    # 上传到github 测试文件下载