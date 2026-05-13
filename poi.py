import requests

class Poi:
    def __init__(self):
        pass
    def bd(self, lat, lng):
        # baidu lbs
        url = 'https://api.map.baidu.com/reverse_geocoding/v3/'
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        params = {
            'ak': 'IIyMOG9GMGWCU0Yu5PVdHgvSzdg4tpIo',
            'location': str(lat) + ',' + str(lng), #'31.289301,104.514',
            # 'extensions_poi': '1',
            # 'entire_poi': '1',
            # 'sort_strategy': 'distance',
            'output': 'json',
            # 'coordtype': 'bd09ll'
        }
        response = requests.get(url, headers=headers, params=params, timeout=30)

        data = response.json()

        print(data)

        addr = {
            'province': data['result']['addressComponent']['province'],
            'city': data['result']['addressComponent']['city'],
            'district': data['result']['addressComponent']['district'],
            'town': data['result']['addressComponent']['town'],
            'adcode': data['result']['addressComponent']['adcode'],
        }

        return addr

if __name__ == '__main__':
    poi = Poi()
    poi.bd(30.036389, 104.046944)