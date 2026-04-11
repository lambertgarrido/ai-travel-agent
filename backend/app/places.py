import requests
import os

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_places(city):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    
    params = {
        "query": f"top tourist attractions in {city}",
        "key": API_KEY
    }

    res = requests.get(url, params=params)
    return res.json().get("results", [])[:5]