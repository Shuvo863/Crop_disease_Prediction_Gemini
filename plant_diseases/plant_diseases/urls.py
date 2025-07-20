# plant_diseases/plant_diseases/urls.py

from django.contrib import admin
from django.urls import path, include
from plant_diseases import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('detection/', include('detector.urls')),
    path('agricultural-news/', include('agrinews.urls')),
    path('weather-news/', include('weathernews.urls')),
    
    # API URLS যোগ করা হয়েছে
    path('api/', include('detector.api_urls')), # 'detector' অ্যাপের API URLS
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)