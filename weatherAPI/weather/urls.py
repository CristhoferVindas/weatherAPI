from django.urls import path
from .views import WeatherAPIView, ForecastAPIView, HistoricalWeatherAPIView, WeatherByCoordinatesAPIView, MultipleCitiesWeatherAPIView, WeatherWithUnitsAPIView

urlpatterns = [
    path('weather/<str:city_name>/', WeatherAPIView.as_view(), name='weather'),
    path('forecast/<str:city_name>/', ForecastAPIView.as_view(), name='forecast'),
    path('historical/<str:city_name>/<str:date>/', HistoricalWeatherAPIView.as_view(), name='historical_weather'),
    path('weather/coordinates/<str:lat>/<str:lon>/', WeatherByCoordinatesAPIView.as_view(), name='weather_coordinates'),
    path('weather/multiple/<str:cities>/', MultipleCitiesWeatherAPIView.as_view(), name='weather_multiple'),
    path('weather/<str:city_name>/<str:unit>/', WeatherWithUnitsAPIView.as_view(), name='weather_units'),
]
