# plant_diseases/weathernews/serializers.py
from rest_framework import serializers
from .models import WeatherData, DailyForecast

class DailyForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyForecast
        fields = [
            'forecast_date', 'max_min_temp', 'condition', 'rainfall',
            'humidity', 'wind_speed_direction', 'farmer_advice'
        ]

class WeatherDataSerializer(serializers.ModelSerializer):
    daily_forecasts = DailyForecastSerializer(many=True, read_only=True)
    
    class Meta:
        model = WeatherData
        fields = [
            'id', 'location',
            'max_temperature_value', 'max_temperature_unit',
            'min_temperature_value', 'min_temperature_unit',
            'avg_temperature_value', 'avg_temperature_unit',
            'rainfall_value', 'rainfall_unit',
            'humidity_value', 'humidity_unit',
            'wind_speed_value', 'wind_speed_unit',
            'wind_description', 'recorded_at',
            'daily_forecasts'
        ]
        read_only_fields = ['recorded_at']