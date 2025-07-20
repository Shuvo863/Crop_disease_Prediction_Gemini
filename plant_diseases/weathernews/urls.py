# plant_diseases/weathernews/urls.py

from django.urls import path
from . import views

app_name = 'weathernews' # Namespace for weathernews app

urlpatterns = [
    path('', views.weather_news, name='weather_news'),
]