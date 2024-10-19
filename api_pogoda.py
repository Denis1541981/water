#! /usr/bin/env python
import datetime
import math

import pytz
import requests
from aiogram.utils.markdown import hbold

from config import API
from geolocation import geolocate


class WeatherAPI:
    def __init__(self, api_key: str, text: str):
        self.api_key = api_key
        self.text = text

    def get_weather_data(self, text:str) -> dict:
        lat, lon = geolocate(self.text)
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&lang=ru&units=metric&appid={self.api_key}"
        proxy = { "http": None, "https": None }
        res = requests.get(url, proxies=proxy)
        if res.status_code == 200:
            return res.json()
        return {}

class WeatherFormatter:
    @staticmethod
    def format_weather_message(data: dict, user_name: str) -> str:
        if data:
            city = data.get("name")
            cur_temp = round(data.get("main", {}).get("temp"))
            humidity = data.get("main", {}).get("humidity")
            pressure = data.get("main", {}).get("pressure")
            wind = data.get("wind").get("speed")
            feels_like = round(data["main"]["feels_like"])
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"].get("sunrise"))
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"].get("sunset"))
            length_of_the_day = sunset_timestamp - sunrise_timestamp
            weather_description = data["weather"][0].get("description")
            wd = WeatherFormatter.get_smile(weather_description)

            message = (
                f"Замер произведен в {WeatherFormatter.get_current_time()}\n"
                f"Привет, {hbold(user_name)}!\n"
                f"Погода в городе {hbold(city)}:\n"
                f"Температура: {hbold(cur_temp)}°C {wd}\n"
                f"Ощущается как: {hbold(feels_like)}°C\n"
                f"Влажность: {hbold(humidity)}%\n"
                f"Давление: {hbold(math.ceil(pressure / 1.333))} мм.рт.ст\n"
                f"Ветер: {hbold(wind)} м/с\n"
                f"Восход солнца: {sunrise_timestamp}\n"
                f"Закат солнца: {sunset_timestamp}\n"
                f"Продолжительность дня: {hbold(length_of_the_day)}\n"
                f"{hbold(WeatherFormatter.get_time_of_the_day())}  {hbold(user_name)}!"
            )

            return message
        else:
            return "Не удалось получить данные о погоде."

    @staticmethod
    def get_smile(weather_description: str) -> str:
        weather_smile = {
            "ясно": "Ясно \U00002600",
            "облачно": "Облачно \U00002601",
            "дождь": "Дождь \U00002614",
            "гроза": "Гроза \U000026A1",
            "снег": "Снег \U0001F328",
            "туман": "Туман \U0001F32B",
            "пасмурно": "Пасмурно \U0001F32B",
        }
        return weather_smile.get(weather_description.lower(), "\nПосмотри в окно, я не понимаю, что там за погода...")

    @staticmethod
    def get_current_time() -> str:
        mess_date = datetime.datetime.now()
        tz = pytz.timezone("Etc/GMT-7")
        mess_date_utc5 = tz.normalize(mess_date.astimezone(tz))
        return mess_date_utc5.strftime("%H:%M:%S")

    @staticmethod
    def get_time_of_the_day() -> str:
        current_time = datetime.datetime.strptime(WeatherFormatter.get_current_time(), "%H:%M:%S")
        if 5 <= current_time.hour <= 9:
            return 'Доброго утра!'
        elif 10 <= current_time.hour <= 16:
            return 'Хорошего дня!'
        elif 17 <= current_time.hour <= 20:
            return 'Добрый вечер!'
        else:
            return 'Доброй ночи!'


if __name__ == "__main__":
    api_key = API
    weather_api = WeatherAPI(api_key, "Москва")
    if weather_api.get_weather_data("Москва"):
        x = WeatherFormatter.format_weather_message(weather_api.get_weather_data("Москва"), "Василий")
        print(x)