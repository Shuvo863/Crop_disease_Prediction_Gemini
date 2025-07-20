# plant_diseases/detector/admin.py

from django.contrib import admin
from .models import DiagnosisRecord
from django.utils.html import format_html # format_html ইমপোর্ট করুন

@admin.register(DiagnosisRecord)
class DiagnosisRecordAdmin(admin.ModelAdmin):
    # display_crop_image ফাংশনটি image ফিল্ডের থাম্বনেইল দেখানোর জন্য
    def display_crop_image(self, obj):
        if obj.image:
            # ছোট থাম্বনেইল দেখানোর জন্য
            return format_html('<img src="{}" width="50" height="50" style="object-fit: contain; border-radius: 4px;" />', obj.image.url)
        return "No Image"
    
    display_crop_image.short_description = 'ছবি' # কলামের হেডার

    # list_display এ নতুন ফিল্ডগুলো যোগ করা হয়েছে
    list_display = (
        'crop_name',
        'scientific_name', # নতুন ফিল্ড
        'disease_name',
        'insect',
        'weed',
        'display_crop_image', # ফসলের ছবি দেখানোর জন্য
        'additional_comment',
        'timestamp',
    )
    
    # search_fields এ scientific_name যোগ করা হয়েছে
    search_fields = (
        'crop_name',
        'scientific_name',
        'disease_name',
        'insect',
        'weed',
        'cause',
        'symptoms',
        'additional_comment'
    )
    
    list_filter = (
        'crop_name',
        'disease_name',
        'insect',
        'weed',
        'timestamp',
    )
    
    # অ্যাডমিন ডিটেইল ভিউতে ফিল্ডগুলো সাজানোর জন্য
    # fieldsets এ scientific_name যোগ করা হয়েছে
    fieldsets = (
        (None, {
            'fields': ('image', 'crop_name', 'scientific_name', 'disease_name', 'insect', 'weed', 'additional_comment')
        }),
        ('বিস্তারিত তথ্য', {
            'fields': ('cause', 'symptoms', 'preventive_measure', 'curative_measure', 'chemical_control', 'biological_control', 'aci_products'),
            'classes': ('collapse',) # এই সেকশনটি ডিফল্টভাবে কলাপসড থাকবে
        }),
        ('সময়', {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('timestamp', 'display_crop_image',) # timestamp এবং image display শুধুমাত্র পড়ার জন্য