import requests
import json

class A:
    def __init__(self):
        pass

    def get_detail(self, ids):
        url = 'https://www.bkdiao.com/wp-admin/admin-ajax.php'
        headers = {
            'User-Agent': 'Mozilla/5.0',
        }
        params = {
            'action': 'bkdiao_get_spot_viewport_details',
            'ids': ids
        }
        response = requests.get(url, headers=headers, params=params, timeout=30)

        data = response.json()

        # print(data)

        if isinstance(data['data'], dict):
            items = []
            for item in list(data['data'].values()):
                # if item.get('spot_type') not in ('收费黑坑', '收费水库'):
                items.append({
                    'id': item.get('id'),
                    'fish': item.get('fish_type').replace("、", ",")
                })
            return items
        else:
            return []


    def get_list(self, west, east, south, north):
        url = 'https://www.bkdiao.com/wp-admin/admin-ajax.php'
        headers = {
            'User-Agent': 'Mozilla/5.0',
        }
        params = {
            'action': 'bkdiao_get_spots_in_bounds',
            'west': west,
            'east': east,
            'south': south,
            'north': north,
            'limit': 690
        }
        response = requests.get(url, headers=headers, params=params, timeout=30)

        data = response.json()

        # print(data)

        if data.get('success'):
            items = []
            for item in data.get("data"):
                # if item.get('spot_type') not in ('收费黑坑', '收费水库'):
                items.append({
                    'id': item.get('id'),
                    'fish': "",
                    'type': 'WILD_FISHING',
                    'type_desc': '野钓',
                    'lng': item.get('lng'),
                    'lat': item.get('lat'),
                    'address': item.get('title'),
                })
            return items
        else:
            return []

    def pos_grid(self):
        return [
            # 第1行（最北排）
            {'west': 73.5, 'east': 79.65, 'south': 50.0, 'north': 53.5},
            {'west': 79.65, 'east': 85.8, 'south': 50.0, 'north': 53.5},
            {'west': 85.8, 'east': 91.95, 'south': 50.0, 'north': 53.5},
            {'west': 91.95, 'east': 98.1, 'south': 50.0, 'north': 53.5},
            {'west': 98.1, 'east': 104.25, 'south': 50.0, 'north': 53.5},
            {'west': 104.25, 'east': 110.4, 'south': 50.0, 'north': 53.5},
            {'west': 110.4, 'east': 116.55, 'south': 50.0, 'north': 53.5},
            {'west': 116.55, 'east': 122.7, 'south': 50.0, 'north': 53.5},
            {'west': 122.7, 'east': 128.85, 'south': 50.0, 'north': 53.5},
            {'west': 128.85, 'east': 135.0, 'south': 50.0, 'north': 53.5},

            # 第2行
            {'west': 73.5, 'east': 79.65, 'south': 46.45, 'north': 50.0},
            {'west': 79.65, 'east': 85.8, 'south': 46.45, 'north': 50.0},
            {'west': 85.8, 'east': 91.95, 'south': 46.45, 'north': 50.0},
            {'west': 91.95, 'east': 98.1, 'south': 46.45, 'north': 50.0},
            {'west': 98.1, 'east': 104.25, 'south': 46.45, 'north': 50.0},
            {'west': 104.25, 'east': 110.4, 'south': 46.45, 'north': 50.0},
            {'west': 110.4, 'east': 116.55, 'south': 46.45, 'north': 50.0},
            {'west': 116.55, 'east': 122.7, 'south': 46.45, 'north': 50.0},
            {'west': 122.7, 'east': 128.85, 'south': 46.45, 'north': 50.0},
            {'west': 128.85, 'east': 135.0, 'south': 46.45, 'north': 50.0},

            # 第3行
            {'west': 73.5, 'east': 79.65, 'south': 42.9, 'north': 46.45},
            {'west': 79.65, 'east': 85.8, 'south': 42.9, 'north': 46.45},
            {'west': 85.8, 'east': 91.95, 'south': 42.9, 'north': 46.45},
            {'west': 91.95, 'east': 98.1, 'south': 42.9, 'north': 46.45},
            {'west': 98.1, 'east': 104.25, 'south': 42.9, 'north': 46.45},
            {'west': 104.25, 'east': 110.4, 'south': 42.9, 'north': 46.45},
            {'west': 110.4, 'east': 116.55, 'south': 42.9, 'north': 46.45},
            {'west': 116.55, 'east': 122.7, 'south': 42.9, 'north': 46.45},
            {'west': 122.7, 'east': 128.85, 'south': 42.9, 'north': 46.45},
            {'west': 128.85, 'east': 135.0, 'south': 42.9, 'north': 46.45},

            # 第4行
            {'west': 73.5, 'east': 79.65, 'south': 39.35, 'north': 42.9},
            {'west': 79.65, 'east': 85.8, 'south': 39.35, 'north': 42.9},
            {'west': 85.8, 'east': 91.95, 'south': 39.35, 'north': 42.9},
            {'west': 91.95, 'east': 98.1, 'south': 39.35, 'north': 42.9},
            {'west': 98.1, 'east': 104.25, 'south': 39.35, 'north': 42.9},
            {'west': 104.25, 'east': 110.4, 'south': 39.35, 'north': 42.9},
            {'west': 110.4, 'east': 116.55, 'south': 39.35, 'north': 42.9},
            {'west': 116.55, 'east': 122.7, 'south': 39.35, 'north': 42.9},
            {'west': 122.7, 'east': 128.85, 'south': 39.35, 'north': 42.9},
            {'west': 128.85, 'east': 135.0, 'south': 39.35, 'north': 42.9},

            # 第5行
            {'west': 73.5, 'east': 79.65, 'south': 35.8, 'north': 39.35},
            {'west': 79.65, 'east': 85.8, 'south': 35.8, 'north': 39.35},
            {'west': 85.8, 'east': 91.95, 'south': 35.8, 'north': 39.35},
            {'west': 91.95, 'east': 98.1, 'south': 35.8, 'north': 39.35},
            {'west': 98.1, 'east': 104.25, 'south': 35.8, 'north': 39.35},
            {'west': 104.25, 'east': 110.4, 'south': 35.8, 'north': 39.35},
            {'west': 110.4, 'east': 116.55, 'south': 35.8, 'north': 39.35},
            {'west': 116.55, 'east': 122.7, 'south': 35.8, 'north': 39.35},
            {'west': 122.7, 'east': 128.85, 'south': 35.8, 'north': 39.35},
            {'west': 128.85, 'east': 135.0, 'south': 35.8, 'north': 39.35},

            # 第6行
            {'west': 73.5, 'east': 79.65, 'south': 32.25, 'north': 35.8},
            {'west': 79.65, 'east': 85.8, 'south': 32.25, 'north': 35.8},
            {'west': 85.8, 'east': 91.95, 'south': 32.25, 'north': 35.8},
            {'west': 91.95, 'east': 98.1, 'south': 32.25, 'north': 35.8},
            {'west': 98.1, 'east': 104.25, 'south': 32.25, 'north': 35.8},
            {'west': 104.25, 'east': 110.4, 'south': 32.25, 'north': 35.8},
            {'west': 110.4, 'east': 116.55, 'south': 32.25, 'north': 35.8},
            {'west': 116.55, 'east': 122.7, 'south': 32.25, 'north': 35.8},
            {'west': 122.7, 'east': 128.85, 'south': 32.25, 'north': 35.8},
            {'west': 128.85, 'east': 135.0, 'south': 32.25, 'north': 35.8},

            # 第7行
            {'west': 73.5, 'east': 79.65, 'south': 28.7, 'north': 32.25},
            {'west': 79.65, 'east': 85.8, 'south': 28.7, 'north': 32.25},
            {'west': 85.8, 'east': 91.95, 'south': 28.7, 'north': 32.25},
            {'west': 91.95, 'east': 98.1, 'south': 28.7, 'north': 32.25},
            {'west': 98.1, 'east': 104.25, 'south': 28.7, 'north': 32.25},
            {'west': 104.25, 'east': 110.4, 'south': 28.7, 'north': 32.25},
            {'west': 110.4, 'east': 116.55, 'south': 28.7, 'north': 32.25},
            {'west': 116.55, 'east': 122.7, 'south': 28.7, 'north': 32.25},
            {'west': 122.7, 'east': 128.85, 'south': 28.7, 'north': 32.25},
            {'west': 128.85, 'east': 135.0, 'south': 28.7, 'north': 32.25},

            # 第8行
            {'west': 73.5, 'east': 79.65, 'south': 25.15, 'north': 28.7},
            {'west': 79.65, 'east': 85.8, 'south': 25.15, 'north': 28.7},
            {'west': 85.8, 'east': 91.95, 'south': 25.15, 'north': 28.7},
            {'west': 91.95, 'east': 98.1, 'south': 25.15, 'north': 28.7},
            {'west': 98.1, 'east': 104.25, 'south': 25.15, 'north': 28.7},
            {'west': 104.25, 'east': 110.4, 'south': 25.15, 'north': 28.7},
            {'west': 110.4, 'east': 116.55, 'south': 25.15, 'north': 28.7},
            {'west': 116.55, 'east': 122.7, 'south': 25.15, 'north': 28.7},
            {'west': 122.7, 'east': 128.85, 'south': 25.15, 'north': 28.7},
            {'west': 128.85, 'east': 135.0, 'south': 25.15, 'north': 28.7},

            # 第9行
            {'west': 73.5, 'east': 79.65, 'south': 21.6, 'north': 25.15},
            {'west': 79.65, 'east': 85.8, 'south': 21.6, 'north': 25.15},
            {'west': 85.8, 'east': 91.95, 'south': 21.6, 'north': 25.15},
            {'west': 91.95, 'east': 98.1, 'south': 21.6, 'north': 25.15},
            {'west': 98.1, 'east': 104.25, 'south': 21.6, 'north': 25.15},
            {'west': 104.25, 'east': 110.4, 'south': 21.6, 'north': 25.15},
            {'west': 110.4, 'east': 116.55, 'south': 21.6, 'north': 25.15},
            {'west': 116.55, 'east': 122.7, 'south': 21.6, 'north': 25.15},
            {'west': 122.7, 'east': 128.85, 'south': 21.6, 'north': 25.15},
            {'west': 128.85, 'east': 135.0, 'south': 21.6, 'north': 25.15},

            # 第10行（最南排）
            {'west': 73.5, 'east': 79.65, 'south': 18.0, 'north': 21.6},
            {'west': 79.65, 'east': 85.8, 'south': 18.0, 'north': 21.6},
            {'west': 85.8, 'east': 91.95, 'south': 18.0, 'north': 21.6},
            {'west': 91.95, 'east': 98.1, 'south': 18.0, 'north': 21.6},
            {'west': 98.1, 'east': 104.25, 'south': 18.0, 'north': 21.6},
            {'west': 104.25, 'east': 110.4, 'south': 18.0, 'north': 21.6},
            {'west': 110.4, 'east': 116.55, 'south': 18.0, 'north': 21.6},
            {'west': 116.55, 'east': 122.7, 'south': 18.0, 'north': 21.6},
            {'west': 122.7, 'east': 128.85, 'south': 18.0, 'north': 21.6},
            {'west': 128.85, 'east': 135.0, 'south': 18.0, 'north': 21.6},
        ]

if __name__ == "__main__":
    a = A()

    # arrays = [
    #     [str(i) for i in range(start, start + 100)]
    #     for start in range(4000, 4500, 100)
    # ]
    #
    # items = []
    # for array in arrays:
    #     result = ",".join(array)
    #     _items = a.get_detail(result)
    #     items.extend(_items)
    #
    # print(f'全部结束，总共 {len(items)} 条数据')

    # a.get_detail('2777')
    # a.get_list()

    # 整理出第一个数组
    simple_array = []
    grid = a.pos_grid()
    # last_10 = grid[46:56]
    for _grid in grid:
        simple_array.extend(a.get_list(_grid['west'], _grid['east'], _grid['south'], _grid['north']))

    # print(simple_array[-2:])

    # 只取id，并每100个id组成一个新数组
    id_batches = [
        [_['id'] for _ in simple_array[i:i + 100]]
        for i in range(0, len(simple_array), 100)
    ]

    # 整理出第二个数组
    complex_array = []
    for id in id_batches:
        complex_array.extend(a.get_detail(",".join(str(i) for i in id)))


    # 根据第二个数组完善第一个数组
    complex_map = {item['id']: item for item in complex_array}

    for item in simple_array:
        if item['id'] in complex_map:
            item['fish'] = complex_map[item['id']]['fish']

    # print(simple_array)



    print(f' 全部结束，总共 {len(simple_array)} 条数据')

    data = {
        'items': simple_array,
    }

    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


    # 上传到github 测试文件下载...........