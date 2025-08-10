# plant_diseases/weathernews/api_urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('weather-records/', views.WeatherDataListAPIView.as_view(), name='weather_record_list'),
    path('weather-records/<int:pk>/', views.WeatherDataDetailAPIView.as_view(), name='weather_record_detail'),
    path('daily-forecasts/', views.DailyForecastListAPIView.as_view(), name='daily_forecast_list'),
    path('daily-forecasts/<int:pk>/', views.DailyForecastDetailAPIView.as_view(), name='daily_forecast_detail'),
]