from django.shortcuts import render
import requests
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import WeatherSerializer
from django.conf import settings
import datetime

# Create your views here.
class WeatherAPIView(APIView):
    def get(self, request, city_name):
        cached_data = cache.get(city_name)
        if cached_data:
            return Response(cached_data)

        api_key = settings.OPENWEATHERMAP_API_KEY
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'

        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return Response({"error": "Ciudad no encontrada"}, status=404)

        weather_data = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"]
        }

        cache.set(city_name, weather_data, timeout=600)

        serializer = WeatherSerializer(weather_data)
        return Response(serializer.data)

class ForecastAPIView(APIView):
    def get(self, request, city_name):
        api_key = settings.OPENWEATHERMAP_API_KEY
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}&units=metric'

        response = requests.get(url)
        data = response.json()

        if data.get("cod") != "200":
            return Response({"error": data.get("message", "Ciudad no encontrada")}, status=404)

        forecast_data = []
        for entry in data["list"]:
            forecast_data.append({
                "date": entry["dt_txt"],
                "temperature": entry["main"]["temp"],
                "description": entry["weather"][0]["description"],
                "humidity": entry["main"]["humidity"],
                "pressure": entry["main"]["pressure"]
            })

        return Response(forecast_data)
class HistoricalWeatherAPIView(APIView):
    def get(self, request, city_name, date):
        api_key = settings.OPENWEATHERMAP_API_KEY

        geo_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()

        if geo_data.get("cod") != 200:
            return Response({"error": "Ciudad no encontrada"}, status=404)

        lat = geo_data['coord']['lat']
        lon = geo_data['coord']['lon']

        timestamp = int(datetime.datetime.strptime(date, '%Y-%m-%d').timestamp())

        url = f'http://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={timestamp}&appid={api_key}'

        response = requests.get(url)
        data = response.json()

        if "current" not in data:
            return Response({"error": "Datos históricos no encontrados"}, status=404)

        historical_data = {
            "city": city_name,
            "date": date,
            "temperature": data["current"]["temp"],
            "description": data["current"]["weather"][0]["description"],
            "humidity": data["current"]["humidity"],
            "pressure": data["current"]["pressure"]
        }

        return Response(historical_data)
class WeatherByCoordinatesAPIView(APIView):
    def get(self, request, lat, lon):
        if not lat or not lon:
            return Response({"error": "Se requieren latitud y longitud."}, status=400)

        api_key = settings.OPENWEATHERMAP_API_KEY
        url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'

        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return Response({"error": data.get("message", "Datos no encontrados")}, status=404)

        weather_data = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"]
        }

        return Response(weather_data)

class MultipleCitiesWeatherAPIView(APIView):
    def get(self, request, cities):
        cities_list = cities.split('-')
        weather_data_list = []

        for city in cities_list:
            api_key = settings.OPENWEATHERMAP_API_KEY
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

            response = requests.get(url)
            data = response.json()

            if data.get("cod") != 200:
                weather_data_list.append({"city": city, "error": "Ciudad no encontrada"})
            else:
                weather_data = {
                    "city": data["name"],
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"]
                }
                weather_data_list.append(weather_data)

        return Response(weather_data_list)

class WeatherWithUnitsAPIView(APIView):
    def get(self, request, city_name, unit):
        api_key = settings.OPENWEATHERMAP_API_KEY
        if unit not in ['metric', 'imperial', 'standard']:
            return Response({"error": "Unidad no válida"}, status=400)

        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units={unit}'

        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return Response({"error": "Ciudad no encontrada"}, status=404)

        weather_data = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"]
        }

        return Response(weather_data)
