# plant_diseases/agrinews/views.py

from django.shortcuts import render
import requests
# Consider using an actual news API for real agricultural news
# For this example, we'll mock some data.

def agri_news(request):
    """
    Renders the agricultural news page.
    In a real application, this would fetch news from an API or database.
    """
    # Mock data for demonstration
    news_items = [
        {
            'title': 'ধানের বাম্পার ফলন আশা করা হচ্ছে',
            'summary': 'এ বছর আবহাওয়া অনুকূল থাকায় ধানের উৎপাদন বৃদ্ধি পাবে বলে কৃষি বিভাগ জানিয়েছে।',
            'link': '#'
        },
        {
            'title': 'সবজি চাষে নতুন প্রযুক্তি ব্যবহার',
            'summary': 'কৃষকরা আধুনিক প্রযুক্তি ব্যবহার করে সবজি উৎপাদনে নতুন দিগন্ত উন্মোচন করছেন।',
            'link': '#'
        },
        {
            'title': 'সার ও বীজের দাম বৃদ্ধি',
            'summary': 'কৃষি উপকরণের দাম বাড়ায় কৃষকদের মধ্যে উদ্বেগ দেখা দিয়েছে।',
            'link': '#'
        },
        {
            'title': 'আধুনিক সেচ ব্যবস্থায় ফসলের উন্নতি',
            'summary': 'স্মার্ট সেচ পদ্ধতি ব্যবহার করে পানির অপচয় রোধ ও ফলন বৃদ্ধি করা সম্ভব হচ্ছে।',
            'link': '#'
        },
        {
            'title': 'মাটি পরীক্ষার গুরুত্ব',
            'summary': 'সুস্থ ফসলের জন্য নিয়মিত মাটি পরীক্ষা অপরিহার্য, যা পুষ্টি ব্যবস্থাপনায় সহায়তা করে।',
            'link': '#'
        },
    ]
    context = {
        'news_items': news_items
    }
    return render(request, 'agrinews/agrinews.html', context)