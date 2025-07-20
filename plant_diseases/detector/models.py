# plant_diseases/detector/models.py

from django.db import models

class DiagnosisRecord(models.Model):
    image = models.ImageField(upload_to='diagnosis_images/')
    crop_name = models.CharField(max_length=255, blank=True, null=True)
    scientific_name = models.CharField(max_length=255, blank=True, null=True) # নিশ্চিত করুন এই লাইনটি আছে
    disease_name = models.CharField(max_length=255, blank=True, null=True)
    insect = models.CharField(max_length=255, blank=True, null=True)
    weed = models.CharField(max_length=255, blank=True, null=True)
    cause = models.TextField(blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    preventive_measure = models.TextField(blank=True, null=True)
    curative_measure = models.TextField(blank=True, null=True)
    chemical_control = models.TextField(blank=True, null=True)
    biological_control = models.TextField(blank=True, null=True)
    aci_products = models.TextField(blank=True, null=True)
    additional_comment = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop_name} - {self.disease_name} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        ordering = ['-timestamp']