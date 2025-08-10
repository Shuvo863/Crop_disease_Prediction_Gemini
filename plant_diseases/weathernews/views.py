# plant_diseases/weathernews/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings # সেটিংস থেকে API কী লোড করার জন্য
import json
import re
import datetime
import requests # API রিকোয়েস্টের জন্য

from .models import WeatherData, DailyForecast
from .serializers import WeatherDataSerializer, DailyForecastSerializer

# জেমিনি এপিআই কনস্ট্যান্টস (settings.py থেকে লোড করা হচ্ছে)
GEMINI_API_KEY = settings.GEMINI_API_KEY
GEMINI_MODEL_NAME = settings.GEMINI_MODEL_NAME
GEMINI_API_URL = settings.GEMINI_API_URL

# Gradio অ্যাপ থেকে স্থানান্তরিত ইউটিলিটি ফাংশন
def parse_date_range(date_range_str):
    """তারিখ পরিসরের স্ট্রিং থেকে দিনের সংখ্যা পার্স করে।"""
    match = re.search(r'Next (\d+) Days', date_range_str)
    if match:
        return int(match.group(1))
    return 7 # ডিফল্ট

def get_condition_icon(condition_text):
    """আবহাওয়ার অবস্থা বর্ণনা করা একটি টেক্সটের উপর ভিত্তি করে একটি ইমোজি আইকন ফেরত দেয়।"""
    if "Sunny" in condition_text or "রৌদ্রোজ্জ্বল" in condition_text:
        return "☀️"
    elif "Cloudy" in condition_text or "মেঘলা" in condition_text or "Partly Cloudy" in condition_text:
        return "☁️"
    elif "Rain" in condition_text or "বৃষ্টি" in condition_text or "Moderate Rain" in condition_text or "Heavy Rain" in condition_text:
        return "🌧️"
    elif "Thunderstorm" in condition_text or "বজ্রপাত" in condition_text:
        return "⛈️"
    else:
        return "❓"

def parse_value_unit(s):
    """একটি স্ট্রিং থেকে সংখ্যাসূচক মান এবং ইউনিট পার্স করে।"""
    if not isinstance(s, str):
        return None, ''
    match = re.match(r'([\d.]+)\s*(.*)', s.strip()) # Updated regex to handle float values
    if match:
        try:
            value = float(match.group(1))
            unit = match.group(2).strip()
            return value, unit
        except ValueError:
            pass
    return None, s


def get_gemini_forecast_structured(district_name, num_days):
    """
    জেমিনি এপিআই থেকে স্ট্রাকচারড (JSON) আবহাওয়ার পূর্বাভাস গ্রহণ করে।
    """
    prompt = f"""
    আপনি বাংলাদেশের {district_name} জেলার জন্য একটি আবহাওয়ার পূর্বাভাস তৈরি করুন।
    বর্তমান দিনের জন্য (gemini, give first weather data of today), নিম্নলিখিত ডেটা পয়েন্টগুলি সরবরাহ করুন:
    - সর্বোচ্চ তাপমাত্রা (সেলসিয়াস) যেমন: "৩২°C"
    - সর্বনিম্ন তাপমাত্রা (সেলসিয়াস) যেমন: "২৫°C"
    - গড় তাপমাত্রা (সেলসিয়াস) যেমন: "৩০°C"
    - বৃষ্টিপাত (মিমি) যেমন: "৫মিমি"
    - আর্দ্রতা (শতাংশ) যেমন: "৮০%"
    - বাতাসের গতি (কিমি/ঘণ্টা) এবং একটি সংক্ষিপ্ত বিবরণ (যেমন: "হালকা বাতাস।") যেমন: "১০ কিমি/ঘণ্টা"

    এছাড়াও, আগামী {num_days} দিনের জন্য একটি বিস্তারিত আবহাওয়ার পূর্বাভাস দিন। (gemini you will give here data of from today+1 day)
    প্রতিটি দিনের জন্য নিম্নলিখিত তথ্যগুলি JSON ফরম্যাটে সরবরাহ করুন:
    {{
        "date": "DD/MM/YYYY",
        "max_min_temp": "H° / L°",
        "condition": "রৌদ্রোজ্জ্বল/মেঘলা/বৃষ্টি/বজ্রপাত/হালকা বৃষ্টি",
        "rainfall": "Xmm",
        "humidity": "Y%",
        "wind_speed_direction": "Z km/h ডিরেকশন",
        "farmer_advice": "কৃষি প্রভাবের জন্য সংক্ষিপ্ত পরামর্শ to the farmers"
    }}
    
    সম্পূর্ণ আউটপুটটি একটি JSON অবজেক্ট হিসাবে দিন যেখানে দুটি মূল কী থাকবে:
    "current_day_summary": বর্তমান দিনের সারাংশ ডেটা।
    "daily_forecast": আগামী {num_days} দিনের জন্য একটি অ্যারে, যেখানে প্রতিটি দিনের জন্য উপরে বর্ণিত JSON অবজেক্ট থাকবে।
    
    ডেটা বাস্তবসম্মত মনে হলেও এটি একটি সিমুলেশন, প্রকৃত রিয়েল-টাইম ডেটা নয়।
    """

    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "current_day_summary": {
                        "type": "OBJECT",
                        "properties": {
                            "max_temperature": {"type": "STRING"},
                            "min_temperature": {"type": "STRING"},
                            "avg_temperature": {"type": "STRING"},
                            "rainfall": {"type": "STRING"},
                            "humidity": {"type": "STRING"},
                            "wind_speed": {"type": "STRING"},
                            "wind_description": {"type": "STRING"}
                        },
                        "required": ["max_temperature", "min_temperature", "avg_temperature", "rainfall", "humidity", "wind_speed", "wind_description"]
                    },
                    "daily_forecast": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "date": {"type": "STRING"},
                                "max_min_temp": {"type": "STRING"},
                                "condition": {"type": "STRING"},
                                "rainfall": {"type": "STRING"},
                                "humidity": {"type": "STRING"},
                                "wind_speed_direction": {"type": "STRING"},
                                "farmer_advice": {"type": "STRING"}
                            },
                            "required": ["date", "max_min_temp", "condition", "rainfall", "humidity", "wind_speed_direction", "farmer_advice"]
                        }
                    }
                },
                "required": ["current_day_summary", "daily_forecast"]
            }
        }
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()

        if result.get("candidates") and result["candidates"][0].get("content") and \
           result["candidates"][0]["content"].get("parts") and result["candidates"][0]["content"]["parts"][0].get("text"):
            json_string = result["candidates"][0]["content"]["parts"][0]["text"]
            
            # Remove markdown code block if present
            if json_string.startswith("json\n") and json_string.endswith("\n```"):
                json_string = json_string[5:-3].strip()
            
            # Clean up escape characters and extra spaces
            json_string = json_string.replace('\\', '')
            json_string = re.sub(r'[\t\n\r]+', ' ', json_string)
            json_string = re.sub(r'\s{2,}', ' ', json_string)
            
            parsed_data = json.loads(json_string)
            
            print("\n--- জেমিনি প্রম্পট আউটপুট (JSON) ---")
            print(json.dumps(parsed_data, indent=2, ensure_ascii=False))
            print("------------------------------------\n")
            
            return parsed_data
        else:
            print("Error: Gemini response structure unexpected or content missing.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}. Raw response: {response.text if 'response' in locals() else 'N/A'}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


# প্রধান ওয়েব ভিউ যা UI রেন্ডার করবে
def weather_forecast_page(request):
    """আবহাওয়ার পূর্বাভাস প্রদর্শনের জন্য প্রধান HTML পৃষ্ঠা রেন্ডার করে।"""
    bangladesh_districts = [
        "ঢাকা", "চট্টগ্রাম", "খুলনা", "রাজশাহী", "সিলেট", "বরিশাল", "রংপুর", "ময়মনসিংহ",
        "ফরিদপুর", "কুমিল্লা", "নোয়াখালী", "বগুড়া", "দিনাজপুর", "যশোর", "কুষ্টিয়া",
        "টাঙ্গাইল", "কিশোরগঞ্জ", "চাঁদপুর", "ব্রাহ্মণবাড়িয়া", "গাজীপুর", "নারায়ণগঞ্জ",
        "মুন্সিগঞ্জ", "গোপালগঞ্জ", "মাদারীপুর", "শরীয়তপুর", "রাজবাড়ী", "মানিকগঞ্জ",
        "নেত্রকোণা", "শেরপুর", "জামালপুর", "নওগাঁ", "নাটোর", "জয়পুরহাট", "চাঁপাইনবাবগঞ্জ",
        "পাবনা", "সিরাজগঞ্জ", "পঞ্চগড়", "ঠাকুরগাঁও", "নীলফামারী", "লালমনিরহাট",
        "কুড়িগ্রাম", "গাইবান্ধা", "নড়াইল", "সাতক্ষীরা", "চুয়াডাঙ্গা", "মেহেরপুর",
        "ঝিনাইদহ", "মাগুরা", "বাগেরহাট", "পিরোজপুর", "ভোলা", "পটুয়াখালী", "বরগুনা",
        "ঝালকাঠি", "লক্ষ্মীপুর", "ফেনী", "কক্সবাজার", "বান্দরবান", "রাঙ্গামাটি", "খাগড়াছড়ি"
    ]
    date_ranges = ["Next 7 Days", "Next 14 Days", "Next 30 Days"]
    
    context = {
        'districts': bangladesh_districts,
        'date_ranges': date_ranges
    }
    return render(request, 'weathernews/weathernews.html', context)


# API ভিউ যা জেমিনি থেকে ডেটা আনবে এবং সংরক্ষণ করবে, তারপর UI এর জন্য JSON ফেরত দেবে
@csrf_exempt # এটি POST রিকোয়েস্টের জন্য CSRF টোকেন বাইপাস করে। প্রোডাকশনে API কী বা টোকেন অথেন্টিকেশন ব্যবহার করুন।
def get_and_save_weather_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            location = data.get('location', 'Unknown')
            date_range_str = data.get('date_range', 'Next 7 Days')
            num_days = parse_date_range(date_range_str)

            gemini_data = get_gemini_forecast_structured(location, num_days)

            if gemini_data:
                current_summary = gemini_data.get("current_day_summary", {})
                daily_forecasts_data = gemini_data.get("daily_forecast", [])

                # WeatherData সংরক্ষণ করুন
                max_temp_val, max_temp_unit = parse_value_unit(current_summary.get('max_temperature'))
                min_temp_val, min_temp_unit = parse_value_unit(current_summary.get('min_temperature'))
                avg_temp_val, avg_temp_unit = parse_value_unit(current_summary.get('avg_temperature'))
                rainfall_val, rainfall_unit = parse_value_unit(current_summary.get('rainfall'))
                humidity_val, humidity_unit = parse_value_unit(current_summary.get('humidity'))
                wind_speed_val, wind_speed_unit = parse_value_unit(current_summary.get('wind_speed'))

                weather_record = WeatherData.objects.create(
                    location=location,
                    max_temperature_value=max_temp_val,
                    max_temperature_unit=max_temp_unit if max_temp_unit else '°C',
                    min_temperature_value=min_temp_val,
                    min_temperature_unit=min_temp_unit if min_temp_unit else '°C',
                    avg_temperature_value=avg_temp_val,
                    avg_temperature_unit=avg_temp_unit if avg_temp_unit else '°C',
                    rainfall_value=rainfall_val,
                    rainfall_unit=rainfall_unit if rainfall_unit else 'mm',
                    humidity_value=humidity_val,
                    humidity_unit=humidity_unit if humidity_unit else '%',
                    wind_speed_value=wind_speed_val,
                    wind_speed_unit=wind_speed_unit if wind_speed_unit else 'km/h',
                    wind_description=current_summary.get('wind_description', '')
                )

                # DailyForecast সংরক্ষণ করুন
                for forecast in daily_forecasts_data:
                    try:
                        forecast_date_str = forecast.get('date', '')
                        forecast_date = datetime.datetime.strptime(forecast_date_str, "%d/%m/%Y").date()
                    except ValueError:
                        print(f"Date parsing error: Could not parse '{forecast_date_str}' with format DD/MM/YYYY. Falling back to today + index.")
                        forecast_date = datetime.date.today() + datetime.timedelta(days=daily_forecasts_data.index(forecast))
                    except Exception as e:
                        print(f"General date parsing error: {e} for date: {forecast.get('date')}")
                        forecast_date = datetime.date.today() + datetime.timedelta(days=daily_forecasts_data.index(forecast))

                    DailyForecast.objects.create(
                        weather_record=weather_record,
                        forecast_date=forecast_date,
                        max_min_temp=forecast.get('max_min_temp', 'N/A'),
                        condition=forecast.get('condition', 'N/A'),
                        rainfall=forecast.get('rainfall', 'N/A'),
                        humidity=forecast.get('humidity', 'N/A'),
                        wind_speed_direction=forecast.get('wind_speed_direction', 'N/A'),
                        farmer_advice=forecast.get('farmer_advice', 'N/A')
                    )
                
                # UI এর জন্য ডেটা ফরম্যাট করে ফেরত পাঠান
                response_data = {
                    'status': 'success',
                    'location': location,
                    'current_summary': current_summary,
                    'daily_forecast': daily_forecasts_data
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse({'status': 'error', 'message': 'Failed to get data from Gemini API'}, status=500)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Only POST method allowed'}, status=405)


# Django REST Framework API Views (List/Retrieve)
class WeatherDataListAPIView(generics.ListAPIView):
    queryset = WeatherData.objects.all().order_by('-recorded_at')
    serializer_class = WeatherDataSerializer

class WeatherDataDetailAPIView(generics.RetrieveAPIView):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer

class DailyForecastListAPIView(generics.ListAPIView):
    queryset = DailyForecast.objects.all().order_by('forecast_date')
    serializer_class = DailyForecastSerializer

class DailyForecastDetailAPIView(generics.RetrieveAPIView):
    queryset = DailyForecast.objects.all()
    serializer_class = DailyForecastSerializer