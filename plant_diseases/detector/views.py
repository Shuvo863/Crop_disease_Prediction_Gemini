# plant_diseases/detector/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import io
import base64
import requests
from .models import DiagnosisRecord 
import re 

# REST Framework এর জন্য নতুন ইম্পোর্ট
from rest_framework import generics
from .serializers import DiagnosisRecordSerializer

# API configuration
GEMINI_API_KEY = "AIzaSyDavysJ4I9atTrzvnGOCNUD_t1TiwQwJwI" # আপনার আচল API Key এখানে দিন
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def call_gemini_api(prompt, image_bytes, retries=3):
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inlineData": {
                            "mimeType": "image/jpeg",
                            "data": base64_image # এখানে base69_image এর বদলে base64_image হবে
                        }
                    }
                ]
            }
        ]
    }

    for attempt in range(retries):
        try:
            response = requests.post(GEMINI_API_URL, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            response_json = response.json()
            if 'candidates' in response_json and response_json['candidates']:
                return response_json['candidates'][0]['content']['parts'][0]['text']
            else:
                print(f"Gemini API did not return valid content. Full Response: {response_json}")
                return f"Error: Gemini API did not return valid content. Check server logs for details."
        except requests.exceptions.Timeout:
            print(f"API call timed out (attempt {attempt + 1}/{retries}).")
            if attempt < retries - 1:
                import time
                time.sleep(5)
            else:
                return "Error: Gemini API call timed out after multiple retries."
        except requests.exceptions.RequestException as e:
            print(f"API call failed (attempt {attempt+1}/{retries}): {e}")
            if attempt < retries - 1:
                import time
                time.sleep(2 ** attempt)
            else:
                return f"Error connecting to Gemini API: {str(e)}"
        except KeyError as e:
            print(f"KeyError in Gemini response: {e}, Response: {response_json}")
            return f"Error parsing Gemini API response: Missing key {e}."
        except Exception as e:
            print(f"An unexpected error occurred in call_gemini_api: {e}")
            return f"Error: An unexpected error occurred: {str(e)}"
    return "Failed to get response from Gemini API after multiple retries."


def simplify_field(text, max_words=200):
    return ' '.join(text.strip().split()[:max_words]) if text else "তথ্য পাওয়া যায়নি"

def analyze_image_with_gemini(image_file, additional_context):
    if not image_file:
        return ["কোনো ছবি দেওয়া হয়নি"] * 13

    try:
        pil_image = Image.open(image_file)
        image_bytes_io = io.BytesIO()
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        pil_image.save(image_bytes_io, format='JPEG')
        processed_image_bytes = image_bytes_io.getvalue()

    except Exception as e:
        print(f"Error processing image for API: {e}")
        return [f"Error processing image for API: {e}"] * 13

    prompt = f"""
Act as a professional agriculturalist and plant disease expert. Analyze the image and provide concise answers (max 10 words each for single fields like Crop Name, Disease Name; for lists like Cause, Symptoms etc. provide 3-4 key points/phrases):

1. Crop Name
2. Scientific Name (Full scientific name including genus and species)
3. Disease Name (with Bangla Name in Bangla Language Recognize in Bangladesh,( example: Potato Early Blight(আলুর আগাম ধ্বসা রোগ)))
4. Insects: Mention if any insect/pest is attacking the crop (Name in Bangla if available). (dont wirte as \"Possibly mites/thrips (মাকড়/থ্রিপস)\", just write \"mites/thrips (মাকড়/থ্রিপস)\")
5. Weeds: Identify if present, write \"No weeds\" if dont found anything.
6. Cause (Give 3-4 key causes in simple small sentences, Clear Cause)
7. Symptoms (3-4 specific symptoms)
8. Preventive Measure (3-4 clear and actionable steps, you will mention must)
9. Curative Measure (3-4 clear steps, you will mention must)
10. Chemical Control Measure (3-4 examples, you will mention must)
11. Biological Control Measure (3-4 suggestions, you will mention must)
12. ACI Limited Products (suggest some products produced in ACI limited)
13. Additional Comment: {additional_context if additional_context else 'None provided'}

Format response exactly:
1. Crop Name: ...
2. Scientific Name: ...
3. Disease Name: ...
4. Insects: ...
5. Weeds: ...
6. Cause: ...
7. Symptoms: ...
8. Preventive Measure: ...
9. Curative Measure: ...
10. Chemical Control Measure: ...
11. Biological Control Measure: ...
12. ACI Products: ...
13. Additional Comment: {additional_context if additional_context else 'None provided'}
"""

    response_text = call_gemini_api(prompt, processed_image_bytes)
    
    print(f"Raw Gemini Response:\n{response_text}\n---")

    if response_text.startswith("Error:"):
        return [response_text] * 13

    lines = response_text.strip().split("\n")
    
    parsed_data = {
        "Crop Name": "তথ্য পাওয়া যায়নি",
        "Scientific Name": "তথ্য পাওয়া যায়নি",
        "Disease Name": "তথ্য পাওয়া যায়নি",
        "Insects": "তথ্য পাওয়া যায়নি",
        "Weeds": "তথ্য পাওয়া যায়নি",
        "Cause": "তথ্য পাওয়া যায়নি",
        "Symptoms": "তথ্য পাওয়া যায়নি",
        "Preventive Measure": "তথ্য পাওয়া যায়নি",
        "Curative Measure": "তথ্য পাওয়া যায়নি",
        "Chemical Control Measure": "তথ্য পাওয়া যায়নি",
        "Biological Control Measure": "তথ্য পাওয়া যায়নি",
        "ACI Products": "তথ্য পাওয়া যায়নি",
        "Additional Comment": "তথ্য পাওয়া যায়নি"
    }

    for line in lines:
        line_stripped = line.strip()

        match = re.match(r'^\s*(\d+)\.\s*(.*?):\s*(.*)$', line_stripped)
        if match:
            field_label = match.group(2).strip()
            field_value = match.group(3).strip()

            if field_label == "ACI Limited Products":
                field_label = "ACI Products"
            
            if field_label in parsed_data:
                parsed_data[field_label] = simplify_field(field_value)
                continue

        match_no_num = re.match(r'^\s*(.*?):\s*(.*)$', line_stripped)
        if match_no_num:
            field_label_no_num = match_no_num.group(1).strip()
            field_value_no_num = match_no_num.group(2).strip()

            if field_label_no_num == "ACI Limited Products":
                field_label_no_num = "ACI Products"

            if field_label_no_num in parsed_data:
                parsed_data[field_label_no_num] = simplify_field(field_value_no_num)
                continue

    ordered_results = [
        parsed_data["Crop Name"],
        parsed_data["Scientific Name"],
        parsed_data["Disease Name"],
        parsed_data["Insects"],
        parsed_data["Weeds"],
        parsed_data["Cause"],
        parsed_data["Symptoms"],
        parsed_data["Preventive Measure"],
        parsed_data["Curative Measure"],
        parsed_data["Chemical Control Measure"],
        parsed_data["Biological Control Measure"],
        parsed_data["ACI Products"],
        parsed_data["Additional Comment"]
    ]

    print(f"Parsed Results (Ordered):\n{ordered_results}\n---")

    return ordered_results


@csrf_exempt
def detect_disease(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            uploaded_image = request.FILES['image']
            additional_context = request.POST.get('additional_context', '')

            gemini_results = analyze_image_with_gemini(uploaded_image, additional_context)

            crop, scientific_name, disease, insect, weed, cause, symptoms, preventive, curative, chemical, biological, products, comment = gemini_results
            
            save_status = ""
            try:
                diagnosis_record = DiagnosisRecord(
                    image=uploaded_image,
                    crop_name=crop,
                    scientific_name=scientific_name,
                    disease_name=disease,
                    insect=insect,
                    weed=weed,
                    cause=cause,
                    symptoms=symptoms,
                    preventive_measure=preventive,
                    curative_measure=curative,
                    chemical_control=chemical,
                    biological_control=biological,
                    aci_products=products,
                    additional_comment=comment
                )
                diagnosis_record.save()

                save_status = "রেকর্ড সফলভাবে সংরক্ষিত হয়েছে।"
            except Exception as e:
                save_status = f"রেকর্ড সংরক্ষণে ত্রুটি: {e}"
                print(f"Database save error: {e}")
            
            response_data = {
                'crop_name': crop,
                'scientific_name': scientific_name,
                'disease_name': disease,
                'insect': insect,
                'weed': weed,
                'cause': cause,
                'symptoms': symptoms,
                'preventive_measure': preventive,
                'curative_measure': curative,
                'chemical_control': chemical,
                'biological_control': biological,
                'aci_products': products,
                'additional_comment': comment,
                'save_status': save_status
            }
            return JsonResponse(response_data)
        else:
            # এই অংশটি নিশ্চিত করবে যে POST রিকোয়েস্টে সবসময় JSON ফিরে আসে
            return JsonResponse({'error': 'কোনো ছবি আপলোড করা হয়নি।'}, status=400)
            
    # GET রিকোয়েস্ট হলে টেমপ্লেট রেন্ডার করুন
    # এই অংশটি শুধুমাত্র GET রিকোয়েস্টের জন্য, POST রিকোয়েস্টের জন্য নয়
    return render(request, 'detector/detect_disease.html')

# API Views
class DiagnosisRecordListAPIView(generics.ListAPIView):
    queryset = DiagnosisRecord.objects.all()
    serializer_class = DiagnosisRecordSerializer

    def get_serializer_context(self):
        # image_url ফিল্ডের জন্য request context পাস করা হচ্ছে
        return {'request': self.request}

class DiagnosisRecordDetailAPIView(generics.RetrieveAPIView):
    queryset = DiagnosisRecord.objects.all()
    serializer_class = DiagnosisRecordSerializer
    lookup_field = 'pk'

    def get_serializer_context(self):
        # image_url ফিল্ডের জন্য request context পাস করা হচ্ছে
        return {'request': self.request}