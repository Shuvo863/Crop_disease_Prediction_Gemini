# plant_diseases/detector/serializers.py

from rest_framework import serializers
from .models import DiagnosisRecord

class DiagnosisRecordSerializer(serializers.ModelSerializer):
    # image_url একটি কাস্টম ফিল্ড যা ইমেজ ফাইলের সম্পূর্ণ URL দেবে
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = DiagnosisRecord
        # API তে আপনি যে ফিল্ডগুলো দেখতে চান, সেগুলোর নাম এখানে উল্লেখ করুন
        fields = [
            'id', 'image', 'image_url', 'crop_name', 'scientific_name', 'disease_name',
            'insect', 'weed', 'cause', 'symptoms', 'preventive_measure',
            'curative_measure', 'chemical_control', 'biological_control',
            'aci_products', 'additional_comment', 'timestamp'
        ]
        # যদি সব ফিল্ড দেখতে চান, তাহলে fields = '__all__' ব্যবহার করতে পারেন।
        # কিন্তু সুনির্দিষ্টভাবে উল্লেখ করা ভালো।

    def get_image_url(self, obj):
        # ইমেজ ফাইলের সম্পূর্ণ URL তৈরি করে
        # request context serializer এ পাস করা হলে এটি কাজ করবে
        if obj.image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url # যদি request context না থাকে
        return None