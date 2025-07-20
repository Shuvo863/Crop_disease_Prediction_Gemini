# plant_diseases/detector/api_urls.py

from django.urls import path
from . import views

app_name = 'api_detector' # API URL গুলোর জন্য একটি আলাদা namespace

urlpatterns = [
    # সকল রোগ নির্ণয় রেকর্ড দেখার জন্য API
    path('records/', views.DiagnosisRecordListAPIView.as_view(), name='record-list'),
    # নির্দিষ্ট ID এর রোগ নির্ণয় রেকর্ড দেখার জন্য API
    path('records/<int:pk>/', views.DiagnosisRecordDetailAPIView.as_view(), name='record-detail'),
]