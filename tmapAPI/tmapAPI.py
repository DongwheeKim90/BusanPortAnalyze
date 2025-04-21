import requests
from urllib.parse import quote
import folium

class tmapAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            'appKey': self.api_key
        }

    def get_coord(self, keyword: str):
        url = f"https://apis.openapi.sk.com/tmap/pois?version=1&searchKeyword=\
            {quote(keyword,encoding='utf-8')}&count=1"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            res = response.json()
            if res['searchPoiInfo']:
                result = res['searchPoiInfo']['pois']['poi'][0]
                name = result['name']
                lat = result['frontLat']
                lng = result['frontlng']
                address = result['newAddressList']['newAddress'][0]\
                    ['fullAddressRoad']
                return {'name': name, 'lat': lat, 'lng': lng, 'address': address}
            else:
                return {'error': 'No results found'}
        else:
            return {'error': f"Request failed{response.status_code} /\
                     {response.text}"}
        
    def get_route_raw(self, start: dict, end: dict):
        url_car = "https://apis.openapi.sk.com/tmap/routes?version=1&callback=function"
        url_peds = "https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1&callback=function"

        payload_car = {
            'startX': start['lng'],
            'startY': start['lat'],
            'endX': end['lng'],
            'endY': end['lat']
        }

        payload_peds = {
            'startX': start['lng'],
            'startY': start['lat'],
            'endX': end['lng'],
            'endY': end['lat'],
            'startName': quote(start['name'], encoding='utf-8'),
            'endName': quote(end['name'], encoding='utf-8')
        }

        headers = {
            'appKey': self.api_key
        }

        response_car = requests.post(url_car, headers=headers, json=payload_car)
        response_peds = requests.post(url_peds, headers=headers, json=payload_peds)

        routes = {
            'car': None,
            'peds': None,
            'startName': start['name'],
            'endName': end['name']
        }

        if response_car.status_code == 200:
            res = response_car.json()
            if res['features']:
                routes['car'] = res['features']
            else:
                routes['car'] = {'error': 'No results found'}
        else:
            routes['car'] = {'error': f"Request failed{response_car.status_code} /\
                     {response_car.text}"}
            
        if response_peds.status_code == 200:
            res = response_peds.json()
            if res['features']:
                routes['peds'] = res['features']
            else:
                routes['peds'] = {'error': 'No results found'}
        else:
            routes['peds'] = {'error': f"Request failed{response_peds.status_code} /\
                     {response_peds.text}"}
        return routes
    
    def get_route(self, routes: dict):
        route = {'car': {}, 'peds': {},
                 'startName': routes['startName'],
                 'endName': routes['endName']}
        route['car']['distance'] = round(routes['car'][0]\
            ['properties']['totalDistance'] / 1000,1)
        route['car']['time'] = round(routes['car'][0]\
            ['properties']['totalTime'] / 60)
        route['car']['startPoint'] = routes['car'][0]['geometry']['coordinates']
        route['car']['endPoint'] = routes['car'][-1]['geometry']['coordinates']
        route['car']['path'] = []
        for point in routes['car']:
            if point['geometry']['type'] == 'LineString':
                route['car']['path'] += point['geometry']['coordinates']

        route['peds']['distance'] = round(routes['peds'][0]\
            ['properties']['totalDistance'] / 1000,1)
        route['peds']['time'] = round(routes['peds'][0]\
            ['properties']['totalTime'] / 60)
        route['peds']['startPoint'] = routes['peds'][0]['geometry']['coordinates']
        route['peds']['endPoint'] = routes['peds'][-1]['geometry']['coordinates']
        route['peds']['path'] = []
        for point in routes['peds']:
            if point['geometry']['type'] == 'LineString':
                route['peds']['path'] += point['geometry']['coordinates']
        return route
    
    def draw_route(self, routes: dict, mode: str):
        route = routes[mode]
        startPoint = route['startPoint']
        endPoint = route['endPoint']
        mapCenter = [(startPoint[0] + endPoint[0])/2,
                      (startPoint[1] + endPoint[1])/2]
        m = folium.Map(location=[mapCenter[1], mapCenter[0]], zoom_start=15)

        folium.Marker(location=[startPoint[1],startPoint[0]],
                      popup=f"<b>{routes['startName']}</b>",
                      icon=folium.Icon(color='green')).add_to(m)
        folium.Marker(location=[endPoint[1],endPoint[0]],
                      popup=f"<b>{routes['endName']}</b>",
                      icon=folium.Icon(color='red')).add_to(m)
        
        coordinates = [(point[1], point[0]) for point in route['path']]
        folium.PolyLine(locations=coordinates, color="blue",
                        weight=2.5, opacity=1).add_to(m)
        return m