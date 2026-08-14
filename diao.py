import requests
import json

class A:
    def __init__(self):
        pass

    def get_detail(self, ids):
        url = 'https://www.bkdiao.com/wp-admin/admin-ajax.php'
        headers = {
            'User-Agent': 'Mozilla/5.0',
            # 'Cookie': 'Hm_lvt_ca860721dce125856eb54faa9f7565a1=1786700246; HMACCOUNT=894AB083B6956AD6; prefers-color-scheme=light; bkdiao_spot_view_4748=1; bkdiao_spot_view_4608=1; Hm_lpvt_ca860721dce125856eb54faa9f7565a1=1786700741'
            'Referer': 'Tokyo District 1 Street Decos'
        }
        params = {
            'action': 'bkdiao_get_spot_viewport_details',
            'ids': ids
        }
        response = requests.get(url, headers=headers, params=params, timeout=30)

        data = response.json()

        # print(data)

        if isinstance(data['data'], dict):
            result = list(data['data'].values())
            return len(result)
        else:
            return 0


    def get_list(self):
        url = 'https://www.bkdiao.com/wp-admin/admin-ajax.php'
        headers = {
            'User-Agent': 'Mozilla/5.0',
            # 'Cookie': 'Hm_lvt_ca860721dce125856eb54faa9f7565a1=1786700246; HMACCOUNT=894AB083B6956AD6; prefers-color-scheme=light; bkdiao_spot_view_4748=1; bkdiao_spot_view_4608=1; Hm_lpvt_ca860721dce125856eb54faa9f7565a1=1786700741'
            'Referer': 'Tokyo District 1 Street Decos'
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
            'west': 29.081794599999995,
            'east': 180,
            'south': 20.265079280000002,
            'north': 47.835157720000005,
            'limit': 9890
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

    arrays = [
        [str(i) for i in range(start, start + 100)]
        for start in range(4000, 4500, 100)
    ]
    # print(arrays[2])

    total = 0
    for array in arrays:
        result = ",".join(array)
        _count = a.get_detail(result)
        total += _count

    print(f'ok 全部结束，总共 {total} 条数据')

    # a.get_detail('5112')

    # a.get_list()


    # 上传到github 测试文件下载