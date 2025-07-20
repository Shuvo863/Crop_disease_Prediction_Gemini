# plant_diseases/detector/urls.py

from django.urls import path
from . import views

app_name = 'detector' # Namespace for detector app

urlpatterns = [
    path('', views.detect_disease, name='detect_disease'),
    # path('records/', views.view_all_records, name='view_all_records'), # For a custom view of records, if needed
]