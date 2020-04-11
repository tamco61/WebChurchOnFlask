import requests
import os


def search_coord(text):
    if text != '':
        server = 'https://geocode-maps.yandex.ru/1.x/'
        params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            'geocode': text,
            'format': 'json'
        }
        resp = requests.get(server, params=params).json()
        if resp['response']['GeoObjectCollection']['featureMember'] != []:
            address_ll = resp['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            address_ll = ','.join(i for i in address_ll.split(' '))
            return address_ll
        return 0
    return 0


def get_request(ll):
    response = None
    server = 'https://static-maps.yandex.ru/1.x/'
    params = {
        'l': 'map',
        'z': 16,
        'll': ll,
        'pt': f'{ll},pm2bll'
    }
    response = requests.get(server, params=params)
    return response


def write_image(response):
    with open('static/img/map.png', "wb") as file:
        file.write(response.content)


def remove():
    os.remove('static/img/map.png')


def main(text):
    write_image(get_request(search_coord(text)))