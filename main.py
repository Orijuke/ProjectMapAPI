import requests
import os
import sys
from math import sqrt
import pygame




def get_boundary(geo_object):
    api_adress = 'https://geocode-maps.yandex.ru/1.x'
    apikey = '40d1649f-0493-4b70-98ba-98533de7710b'
    response = requests.get(f'{api_adress}/?apikey={apikey}&geocode={geo_object},+1&format=json')

    if response:
        response_data = response.json()
        GeoObject = response_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        envelop = GeoObject['boundedBy']['Envelope']
        return envelop['lowerCorner'].replace(' ', ',') + '~' + envelop['upperCorner'].replace(' ', ',')


def get_coords(geo_object):
    api_adress = 'https://geocode-maps.yandex.ru/1.x'
    apikey = '40d1649f-0493-4b70-98ba-98533de7710b'
    response = requests.get(f'{api_adress}/?apikey={apikey}&geocode={geo_object},+1&format=json')

    if response:
        response_data = response.json()
        GeoObject = response_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        return ','.join(GeoObject['Point']['pos'].split(' '))


# Инициализируем pygame
pygame.init()
size = (600, 450)
screen = pygame.display.set_mode(size)
position = get_coords('Москва')
xy = [float(position.split(',')[0]), float(position.split(',')[1])]

zoom = 12
k = 1 / (2 ** zoom)
does = True
updated = False
while does:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            does = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN:
                if zoom != 0:
                    zoom -= 1
            if event.key == pygame.K_PAGEUP:
                if zoom != 17:
                    zoom += 1
            k = 1 / (2 ** zoom)

            if event.key == pygame.K_UP:
                xy[1] += k * size[1] / sqrt(2)
                if xy[1] > 90:
                    xy[1] -= k * size[1] / sqrt(2)
                position = str(xy[0]) + ',' + str(xy[1])
            if event.key == pygame.K_DOWN:
                xy[1] -= k * size[1] / sqrt(2)
                if xy[1] < -90:
                    xy[1] += k * size[1] / sqrt(2)
                position = str(xy[0]) + ',' + str(xy[1])

            if event.key == pygame.K_LEFT:
                xy[0] -= k * size[0] * sqrt(2)
                if xy[0] < -180:
                    xy[0] += k * size[0] * sqrt(2)
                position = str(xy[0]) + ',' + str(xy[1])
            if event.key == pygame.K_RIGHT:
                xy[0] += k * size[0] * sqrt(2)
                if xy[0] > 180:
                    xy[0] -= k * size[0] * sqrt(2)
                position = str(xy[0]) + ',' + str(xy[1])
            print(xy)
            updated = False

    if not updated:

        response = None
        map_request = "https://static-maps.yandex.ru/1.x/?ll=" + position + f"&z={zoom}&size=600,450&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        updated = True

    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()
