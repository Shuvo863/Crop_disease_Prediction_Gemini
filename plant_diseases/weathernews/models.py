# plant_diseases/weathernews/models.py
from django.db import models
from django.utils import timezone

class WeatherData(models.Model):
    # Summary Data
    location = models.CharField(max_length=100)
    
    max_temperature_value = models.FloatField(null=True, blank=True)
    max_temperature_unit = models.CharField(max_length=10, default='°C')
    min_temperature_value = models.FloatField(null=True, blank=True)
    min_temperature_unit = models.CharField(max_length=10, default='°C')
    
    avg_temperature_value = models.FloatField(null=True, blank=True)
    avg_temperature_unit = models.CharField(max_length=10, default='°C')
    rainfall_value = models.FloatField(null=True, blank=True)
    rainfall_unit = models.CharField(max_length=10, default='mm')
    humidity_value = models.FloatField(null=True, blank=True)
    humidity_unit = models.CharField(max_length=10, default='%')
    wind_speed_value = models.FloatField(null=True, blank=True)
    wind_speed_unit = models.CharField(max_length=10, default='km/h')
    wind_description = models.TextField(blank=True, null=True)

    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location} - {self.recorded_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "Weather Record"
        verbose_name_plural = "Weather Records"

class DailyForecast(models.Model):
    weather_record = models.ForeignKey(WeatherData, on_delete=models.CASCADE, related_name='daily_forecasts')
    forecast_date = models.DateField()
    max_min_temp = models.CharField(max_length=50, blank=True, null=True)
    condition = models.CharField(max_length=100, blank=True, null=True)
    rainfall = models.CharField(max_length=50, blank=True, null=True)
    humidity = models.CharField(max_length=50, blank=True, null=True)
    wind_speed_direction = models.CharField(max_length=100, blank=True, null=True)
    farmer_advice = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.weather_record.location} - {self.forecast_date.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Daily Forecast"
        verbose_name_plural = "Daily Forecasts"
        ordering = ['forecast_date'] # তারিখ অনুযায়ী সাজানো