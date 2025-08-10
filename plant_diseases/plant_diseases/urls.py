# plant_diseases/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings # settings ইম্পোর্ট করুন
from django.conf.urls.static import static # static ইম্পোর্ট করুন

from . import views # plant_diseases অ্যাপের views কে ইম্পোর্ট করা হয়েছে (যদি থাকে)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'), # আপনার হোম পেজ ভিউ

    path('weather-news/', include('weathernews.urls')), # weathernews অ্যাপের প্রধান URL গুলো অন্তর্ভুক্ত করা হয়েছে
    path('api/weather/', include('weathernews.api_urls')), # weathernews অ্যাপের API URL গুলো অন্তর্ভুক্ত করা হয়েছে

    path('detector/', include('detector.urls')), # detector অ্যাপের URL গুলো অন্তর্ভুক্ত করা হয়েছে (যদি থাকে)
    path('api/detector/', include('detector.api_urls')), # detector অ্যাপের API URL গুলো অন্তর্ভুক্ত করা হয়েছে (যদি থাকে)

    path('agricultural-news/', include('agrinews.urls')), # agrinews অ্যাপের URL গুলো অন্তর্ভুক্ত করা হয়েছে (যদি থাকে)
    # path('api/agrinews/', include('agrinews.api_urls')), # agrinews অ্যাপের API URL গুলো অন্তর্ভুক্ত করা হয়েছে (যদি থাকে)
]

# DEBUG মোডে Media ফাইল সার্ভ করার জন্য (প্রোডাকশনে এভাবে করবেন না)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # নিশ্চিত করুন static ফাইলগুলোও সার্ভ হচ্ছে