# plant_diseases/agrinews/urls.py

from django.urls import path
from . import views

app_name = 'agrinews' # Namespace for agrinews app

urlpatterns = [
    path('', views.agri_news, name='agri_news'),
]