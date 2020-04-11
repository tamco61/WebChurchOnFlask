import requests
import os


def draw_map(address):
    req = "http://geocode-maps.yandex.ru/1.x/" \
          "?apikey=40d1649f-0493-4b70-98ba-98533de7710b" \
          "&geocode={}&format=json".format(address)

    response = requests.get(req)

    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = ','.join(toponym["Point"]["pos"].split())

        return toponym_coodrinates
