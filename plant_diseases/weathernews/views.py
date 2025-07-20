# plant_diseases/weathernews/views.py

from django.shortcuts import render
import requests
# You would typically use an external Weather API here, e.g., OpenWeatherMap, AccuWeather.
# For demonstration, we'll use mock data or a simplified fetch.

def weather_news(request):
    """
    Renders the weather news page.
    In a real application, this would fetch weather data from an API.
    """
    # Mock data for demonstration
    weather_data = {
        'location': 'ঢাকা',
        'temperature': '৩০°C',
        'condition': 'আংশিক মেঘলা',
        'humidity': '৮০%',
        'wind_speed': '১০ কিমি/ঘণ্টা',
        'forecast': [
            {'day': 'আজ', 'temp': '৩০°C', 'cond': 'মেঘলা'},
            {'day': 'আগামীকাল', 'temp': '৩২°C', 'cond': 'রৌদ্রোজ্জ্বল'},
            {'day': 'পরশু', 'temp': '২৯°C', 'cond': 'বৃষ্টির সম্ভাবনা'},
            {'day': 'পরবর্তী ৪-৭ দিন', 'temp': 'গড় ৩১°C', 'cond': 'সাধারণত রৌদ্রোজ্জ্বল'},
        ]
    }
    context = {
        'weather_data': weather_data
    }
    return render(request, 'weathernews/weathernews.html', context)