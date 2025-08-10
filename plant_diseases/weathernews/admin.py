# plant_diseases/weathernews/admin.py
from django.contrib import admin

from .models import WeatherData, DailyForecast


class DailyForecastInline(admin.TabularInline):
    model = DailyForecast
    extra = 1
    fields = ('forecast_date', 'max_min_temp', 'condition', 'rainfall', 'humidity', 'wind_speed_direction', 'farmer_advice')
    can_delete = True


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = (
        'location',
        'max_temperature_value',
        'min_temperature_value',
        'avg_temperature_value',
        'rainfall_value',
        'humidity_value',
        'wind_speed_value',
        'recorded_at'
    )
    search_fields = ('location', 'wind_description')
    list_filter = ('location', 'recorded_at')
    inlines = [DailyForecastInline]
    readonly_fields = ('recorded_at',)
    fieldsets = (
        (None, {
            'fields': ('location',)
        }),
        ('Current Day Summary', {
            'fields': (
                'max_temperature_value', 'max_temperature_unit',
                'min_temperature_value', 'min_temperature_unit',
                'avg_temperature_value', 'avg_temperature_unit',
                'rainfall_value', 'rainfall_unit',
                'humidity_value', 'humidity_unit',
                'wind_speed_value', 'wind_speed_unit',
                'wind_description'
            )
        }),
        ('Metadata', {
            'fields': ('recorded_at',)
        }),
    )