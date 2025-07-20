# plant_diseases/agrinews/models.py
from django.db import models

# আপনি যদি পরে ডেটাবেসে সংবাদ সংরক্ষণ করতে চান, তবে এখানে মডেল যোগ করতে পারেন।
# উদাহরণস্বরূপ:
# class NewsArticle(models.Model):
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     published_date = models.DateTimeField(auto_now_add=True)
#     source = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.title