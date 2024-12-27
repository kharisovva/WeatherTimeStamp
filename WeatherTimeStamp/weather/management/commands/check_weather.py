from django.core.management.base import BaseCommand
import requests
import time
from weather.models import City, WeatherTimeStamp

class Command(BaseCommand):
    help = 'Собирает данные о погоде и записывает их в WeatherTimeStamp'

    def handle(self, *args, **kwargs):
        # получаем города из БД
        cities = City.objects.all()

        try:
            while True:
                # делаем запрос к API
                for city in cities:
                    weather = requests.get(
                        f'https://api.openweathermap.org/data/2.5/weather?lat={city.latitude}&lon={city.longitude}&appid=fc15c6c6c25ff737a402c0b5f8f49d3e')
                    # проверяем, что запрос был успешным
                    if 200 <= weather.status_code <= 299:
                        weather_data = weather.json()

                        # получаем нужные данные
                        humidity = weather_data['main']['humidity']
                        temperature = weather_data['main']['temp']

                        # сохраняем данные в БД
                        WeatherTimeStamp.objects.create(
                            city=city,
                            humidity=humidity,
                            temperature=temperature - 273.5  # здесь я конвертирую Кельвин в Цельсий :)
                        )

                        self.stdout.write(self.style.SUCCESS(f"Данные для города {city.name} собраны и сохранены!"))
                    else:
                        self.stdout.write(self.style.ERROR(f"Ошибка получения данных для города {city.name}"))

                # таймер стопа бесконечной функции, повторный сбор данных через 5 минут
                time.sleep(300)
        except KeyboardInterrupt:
            print('Сбор данных о погоде приостановлен')