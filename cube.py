import requests
import os
import sys
import math
from find_m import find_m
from PIL import Image
from io import BytesIO


search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

toponym_to_find = input()

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
print(toponym_coodrinates)
w, h = [float(i) for i in toponym_coodrinates.split(" ")]
# w, h = abs(w), abs(h)
w, h = str(w), str(h)
api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
delta = "0.005"
arch_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": ",".join([w, h]),
    "type": "biz"}

resp = requests.get(search_api_server, params=arch_params)
json_response = resp.json()
organization = json_response["features"][0]
# Название организации.
org_name = organization["properties"]["CompanyMetaData"]["name"]
# Адрес организации.
org_address = organization["properties"]["CompanyMetaData"]["address"]

# Получаем координаты ответа.
point = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(point[0], point[1])


params = {
    "bbox": ",".join([w, h]) + "~" + org_point,
    "l": "map",
    "pt": org_point + "~" + ",".join([w, h])}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=params)
Image.open(BytesIO(
    response.content)).show()
x, y = [float(i) for i in org_point.split(",")]
w, h = float(w), float(h)
dist = math.sqrt((x - w) ** 2 + (y - h) ** 2) * 111

time = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
print(org_address, org_name, time, dist, sep="\n")