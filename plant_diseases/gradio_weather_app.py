import gradio as gr
import requests

def weather_forecast(location, date_range):
    response = requests.get(f"http://127.0.0.1:8003/weather-news/get_forecast/", params={"location": location, "date_range": date_range})
    return response.json()

with gr.Interface(fn=weather_forecast, inputs=["text", "text"], outputs="json") as demo:
    demo.launch()
