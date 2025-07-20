# plant_diseases/plant_disease/views.py

from django.shortcuts import render

def home_view(request):
    """
    Renders the home page of the application with links to different sections.
    """
    return render(request, 'home.html')