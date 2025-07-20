# plant_diseases/weathernews/models.py
from django.db import models

# আপনি যদি পরে ডেটাবেসে আবহাওয়ার তথ্য সংরক্ষণ করতে চান, তবে এখানে মডেল যোগ করতে পারেন।
# উদাহরণস্বরূপ:
# class WeatherData(models.Model):
#     location = models.CharField(max_length=100)
#     temperature = models.FloatField()
#     condition = models.CharField(max_length=100)
#     recorded_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.location} - {self.condition}"