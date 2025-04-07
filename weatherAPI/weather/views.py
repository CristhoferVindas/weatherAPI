from django.shortcuts import render
import requests
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import WeatherSerializer
from django.conf import settings

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
