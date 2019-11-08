import requests
from tokens import weather_token
from datetime import datetime, timedelta

class BaseWeather:
    def __init__(self):
        self.url_current = 'https://api.openweathermap.org/data/2.5/weather?APPID=' + weather_token + '&units=metric&lang=ru&'
        self.url_forecast = 'https://api.openweathermap.org/data/2.5/forecast?APPID=' + weather_token + '&units=metric&lang=ru&'

    def get_city(self, city=None):
        if city is None:
            city = 'Minsk,by'
        r = requests.get(self.url_current + f'q={city}')
        return r.json()

    def get_city_forecast(self, city=None):
        if city is None:
            city = 'Minsk,by'
        r = requests.get(self.url_forecast + f'q={city}')
        return r.json()

    def get_data(self, city=None):
        data = self.get_city(city)
        result = {
            'id': data['id'],
            'name': data['name'],
            'weather': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'clouds': data['clouds']['all'],
            'temp': data['main']['temp'],
            'temp_max': data['main']['temp_max'],
            'temp_min': data['main']['temp_min'],
            'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S'),
            'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S'),
        }
        return result

    def get_message(self, city=None):
        data = self.get_data(city)
        return f'''Погода {data['name']}:
        {data['weather']}
        давление {data['pressure']} кПа
        влажность {data['humidity']}%
        облачность {data['clouds']}%
        температура {data['temp']}\u00B0
        восход {data['sunrise']}
        закат {data['sunset']}
        '''

    def get_data_forecast(self, city=None):
        data = self.get_city_forecast(city)
        result = {
            'id': data['city']['id'],
            'name': data['city']['name'],
            'list': []
        }
        # timezone = data['city']['timezone']
        current_date = datetime.now()
        for forecast in data['list']:
            forecast_time = datetime.fromtimestamp(forecast['dt'])
            if forecast_time <= current_date + timedelta(days=1, hours=3):
                weather = {
                    'time': forecast_time.strftime('%d.%m %H:%M'),
                    'weather': forecast['weather'][0]['description'],
                    'humidity': forecast['main']['humidity'],
                    'pressure': forecast['main']['pressure'],
                    'clouds': forecast['clouds']['all'],
                    'temp': forecast['main']['temp'],
                    'temp_max': forecast['main']['temp_max'],
                    'tepm_min': forecast['main']['temp_min'],
                }
                result['list'].append(weather)
            else:
                break
        return result

    def get_message_forecast(self, city=None):
        data = self.get_data_forecast(city)
        messages = []
        for forecast in data['list']:
            messages.append(
                f'''Прогноз на {forecast['time']}:
                {forecast['weather']}
                давление {forecast['pressure']} кПа
                влажность {forecast['humidity']}%
                облачность {forecast['clouds']}%
                температура {forecast['temp']}\u00B0\n'''
            )
        return f"Погода в {data['name']}:\n" + ''.join(messages)
        