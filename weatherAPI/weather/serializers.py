# clima/serializers.py
from rest_framework import serializers

class WeatherSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=100)
    temperature = serializers.FloatField()
    description = serializers.CharField(max_length=100)
    humidity = serializers.IntegerField()
    pressure = serializers.IntegerField()
