import math
import requests
import sys
import requests
from io import BytesIO
from PIL import Image


def getMapByCoords(longitude: float, lattitude: float, width: int, height: int, pt: list, map_type='map', zoom=0.01):
    map_params = {
        "ll": f'{longitude},{lattitude}',
        "spn": f'{zoom},{zoom}',
        "l": map_type,
        "size": f"{width},{height}",
        'pt': f'{pt[0]},{pt[1]},pm2rdm'
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    return response.content


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b

    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    distance = math.sqrt(dx * dx + dy * dy)

    return distance


def find_obj(obj):
    toponym_to_find = "+".join(obj)

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        raise (Exception('Неправильный ввод'))

    return response
