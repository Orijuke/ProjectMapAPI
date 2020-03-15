import requests
import os
import sys
from math import sqrt
import pygame

# !/usr/bin/python3
import pygame_textinput
from button import Mode_Button, Clear_Button


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

def get_address(object):
    response = requests.get(
        f'https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={object}&format=json')

    if response:
        response_data = response.json()
        GeoObject = response_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        GeocoderMetaData = GeoObject['metaDataProperty']['GeocoderMetaData']
        return GeocoderMetaData['text']


# Инициализируем pygame
pygame.init()
size = (600, 450)
screen = pygame.display.set_mode(size)
position = get_coords('Москва')
xy = [float(position.split(',')[0]), float(position.split(',')[1])]

textinput = pygame_textinput.TextInput()

all_sprites = pygame.sprite.Group()
buttons = []
mode_btn = Mode_Button(all_sprites)
clear_btn = Clear_Button(all_sprites)

buttons.append(mode_btn)
buttons.append(clear_btn)
zoom = 12
k = 1 / (2 ** zoom)
modes = ['map', 'sat']
text = ''
points = []
does = True
updated = False
clock = pygame.time.Clock()
while does:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            does = False
        all_sprites.update(event)

        for button in buttons:
            if button.get_event(event):
                updated = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN:
                if zoom != 0:
                    zoom -= 1
            if event.key == pygame.K_PAGEUP:
                if zoom != 17:
                    zoom += 1
            k = 1 / (2 ** zoom)

            if event.key == pygame.K_UP:
                xy[1] += k * size[1] / sqrt(2) / 5
                if xy[1] > 90:
                    xy[1] -= k * size[1] / sqrt(2) * 5
                position = str(xy[0]) + ',' + str(xy[1])
            if event.key == pygame.K_DOWN:
                xy[1] -= k * size[1] / sqrt(2) / 5
                if xy[1] < -90:
                    xy[1] += k * size[1] / sqrt(2) * 5
                position = str(xy[0]) + ',' + str(xy[1])

            if event.key == pygame.K_LEFT:
                xy[0] -= k * size[0] * sqrt(2) / 5
                if xy[0] < -180:
                    xy[0] += k * size[0] * sqrt(2) * 5
                position = str(xy[0]) + ',' + str(xy[1])
            if event.key == pygame.K_RIGHT:
                xy[0] += k * size[0] * sqrt(2) / 5
                if xy[0] > 180:
                    xy[0] -= k * size[0] * sqrt(2) * 5
                position = str(xy[0]) + ',' + str(xy[1])
        updated = False

    if not updated:
        response = None
        if clear_btn.get_mode():
            points = []
            text = ''
            clear_btn.i = False
        map_request = "https://static-maps.yandex.ru/1.x/?ll=" + position + f"&z={zoom}&size=600,450&l=" + modes[
            mode_btn.get_mode() % 2] + f"&pt={'~'.join(points)}"
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

    if textinput.update(events):
        object = textinput.get_text()
        position = get_coords(object)
        text = get_address(object)
        points.append(position + ',pm2rdm')
        xy = [float(position.split(',')[0]), float(position.split(',')[1])]

    screen.blit(pygame.image.load(map_file), (0, 0))
    screen.blit(textinput.get_surface(), (60, 15))
    all_sprites.draw(screen)
    f1 = pygame.font.SysFont('serif', 20)
    text1 = f1.render(text, 0, (0, 0, 0))
    screen.blit(text1, (40, 60))
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
