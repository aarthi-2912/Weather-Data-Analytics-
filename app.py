import os
from pathlib import Path

import joblib
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
MODEL_FILE = BASE_DIR / "Super_ML.joblib"

API_KEY = os.getenv("OPENWEATHER_API_KEY", "").strip()
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "Chennai").strip()

GEOCODE_URL = "https://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

FEATURES = [
    "humidity_percent","pressure_hpa","visibility_km",
    "wind_speed_mps","cloudiness_percent","latitude","longitude"
]

def get_model():
    if not MODEL_FILE.exists():
        raise RuntimeError("Super_ML.joblib is missing. Run: py Super_ML.py")
    return joblib.load(MODEL_FILE)

def require_key():
    if not API_KEY:
        raise RuntimeError("OPENWEATHER_API_KEY is missing in .env")

def geocode(city):
    require_key()
    r=requests.get(GEOCODE_URL,params={
        "q":city,"limit":1,"appid":API_KEY
    },timeout=15)
    if r.status_code==401:
        raise RuntimeError("OpenWeather API key is invalid or not active.")
    if r.status_code==429:
        raise RuntimeError("OpenWeather API rate limit reached.")
    r.raise_for_status()
    places=r.json()
    if not places:
        raise RuntimeError(f"City '{city}' was not found.")
    p=places[0]
    return p["lat"],p["lon"]

def live_weather(lat,lon):
    require_key()
    r=requests.get(WEATHER_URL,params={
        "lat":lat,"lon":lon,"appid":API_KEY,"units":"metric"
    },timeout=15)
    if r.status_code==401:
        raise RuntimeError("OpenWeather API key is invalid or not active.")
    if r.status_code==429:
        raise RuntimeError("OpenWeather API rate limit reached.")
    r.raise_for_status()
    d=r.json()
    return {
        "city":d.get("name","Unknown"),
        "country":d.get("sys",{}).get("country",""),
        "latitude":d["coord"]["lat"],
        "longitude":d["coord"]["lon"],
        "temperature_c":round(d["main"]["temp"],1),
        "humidity_percent":d["main"]["humidity"],
        "pressure_hpa":d["main"]["pressure"],
        "visibility_km":round(d.get("visibility",0)/1000,2),
        "wind_speed_mps":round(d.get("wind",{}).get("speed",0),1),
        "cloudiness_percent":d.get("clouds",{}).get("all",0),
        "weather_main":d["weather"][0]["main"],
        "weather_description":d["weather"][0]["description"].title(),
    }

def predict(weather):
    model=get_model()
    values=[[weather[f] for f in FEATURES]]
    return round(float(model.predict(values)[0]),1)

@app.get("/")
def index():
    return render_template("index.html",default_city=DEFAULT_CITY)

@app.get("/api/predict")
def api_predict():
    city=request.args.get("city",DEFAULT_CITY).strip()
    if not city:
        return jsonify({"error":"Enter a city name."}),400
    try:
        lat,lon=geocode(city)
        w=live_weather(lat,lon)
        w["ml_predicted_temperature_c"]=predict(w)
        w["difference_c"]=round(
            w["temperature_c"]-w["ml_predicted_temperature_c"],1
        )
        return jsonify(w)
    except RuntimeError as e:
        return jsonify({"error":str(e)}),400
    except requests.RequestException as e:
        return jsonify({"error":f"Could not connect to OpenWeather: {e}"}),502

if __name__=="__main__":
    print("Weather ML Website: http://127.0.0.1:5000")
    app.run(host="127.0.0.1",port=5000,debug=False)
