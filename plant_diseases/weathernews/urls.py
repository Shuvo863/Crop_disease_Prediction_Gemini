# plant_diseases/weathernews/urls.py
from django.urls import path, include
from . import views

app_name = 'weathernews'

urlpatterns = [
    # প্রধান ওয়েব UI পৃষ্ঠা
    path('', views.weather_forecast_page, name='weather_forecast_page'),
    
    # API এন্ডপয়েন্ট যা জেমিনি থেকে ডেটা আনবে এবং সংরক্ষণ করবে (AJAX কল দ্বারা ব্যবহৃত)
    path('get-and-save-data/', views.get_and_save_weather_data, name='get_and_save_weather_data'),
    
    # API endpoints (serializers.py এবং rest_framework ব্যবহার করে)
    path('api/', include('weathernews.api_urls')), # API specific URLs
]