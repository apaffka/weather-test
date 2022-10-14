import json
import os
import warnings

import pandas as pd
import requests
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from dotenv import load_dotenv
from geopy.geocoders import Nominatim

from .dicts import CONDITION_DICT, DATA_DICT
from .models import Loging

load_dotenv()

warnings.simplefilter(action='ignore', category=FutureWarning)


# Получаем координаты города по названию
def get_coordinate(city: str):
    geolocator = Nominatim(user_agent='a.paffka@yandex.ru')
    location = geolocator.geocode(city, timeout=10)
    return location.latitude, location.longitude


# отправляем get запрос и получаем данные по прогнозу
# в формате json
def get_weather(link: str, coordinates: tuple):
    params = {
        'lat': str(coordinates[0]),
        'lon': str(coordinates[1]),
        'extra': 'true',
    }
    headers = {
        'X-Yandex-API-Key': os.getenv('YANDEX_WEATHER_TOKEN'),
    }
    data = requests.get(
        link, params=params, headers=headers).content.decode('utf8')
    return json.loads(data)['forecasts']


def collect_data(predict: dict):
    needed_data = []
    for day in predict:
        # дёргаем дату
        ex_data = []
        ex_data.append(day['date'])
        # дёргаем и считаем среднюю температуру
        avg_temp = 0
        for day_part_up in ['morning', 'day', 'evening']:
            avg_temp += day['parts'][day_part_up]['temp_avg']
        ex_data.append(round(avg_temp/3))

        # дёргаем данные о магнитном поле
        try:
            ex_data.append(day['biomet']['condition'])
        except KeyError:
            ex_data.append(' ')

        # считаем изменение давления
        # дергаем основные данные о температуре, давлении, влажности
        # и данные о погодном явлении
        pressure = []
        for day_part in ['night', 'morning', 'day', 'evening']:
            pressure.append(day['parts'][day_part]['pressure_mm'])
            for param in ['temp_avg', 'pressure_mm', 'humidity', 'condition']:
                try:
                    ex_data.append(
                        CONDITION_DICT[day['parts'][day_part][param]])
                except KeyError:
                    ex_data.append(day['parts'][day_part][param])
        # не хватило времени придумать как сделать про падение и повышение
        # постараюсь допилить позже
        if abs(max(pressure) - min(pressure)) >= 5:
            ex_data.append('Резкое изменение давления')
        else:
            ex_data.append('')
        # собираем все данные в масив
        needed_data.append(ex_data)
    return needed_data


def prepare_file(data_list: list, city: str):
    df = pd.DataFrame(data_list, columns=DATA_DICT)
    writer = pd.ExcelWriter('files/forecast.xlsx')
    df.to_excel(writer, sheet_name=f'{city}', index=False, na_rep='NaN')

    # Подгоняем ширину столбцов
    for column in df:
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets[f'{city}'].set_column(col_idx, col_idx, column_width)
    writer.save()


# Вьюха для главной страницы
# GET отдаёт форму, POST загружает файл
def index(request):
    template = 'index.html'
    if request.method == 'POST':
        town = request.POST.get('city')
        try:
            coordinate = get_coordinate(town)
        except AttributeError:
            Loging.objects.create(
                city=town,
                latitude='None',
                longitude='None',
                status='Введён несуществующий город',
            )
            return HttpResponse('Ой! Нет такого города!')
        forecast = get_weather(os.getenv('API_LINK'), coordinate)
        col_data = collect_data(forecast)
        prepare_file(col_data, town)
        Loging.objects.create(
            city=town,
            latitude=coordinate[0],
            longitude=coordinate[1],
            status=HttpResponse(request).status_code,
        )
        return FileResponse(open('files/forecast.xlsx', 'rb'))
    return render(request, template)
