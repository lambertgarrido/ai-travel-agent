import requests
import os

API_KEY = os.getenv("RAPIDAPI_KEY")

def search_flights(origin, destination, date):
    url = "https://skyscanner44.p.rapidapi.com/search"

    querystring = {
        "origin": origin,
        "destination": destination,
        "departureDate": date,
        "adults": "1",
        "currency": "USD"
    }

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "skyscanner44.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()

    # Extract simplified results
    results = []
    for flight in data.get("itineraries", [])[:3]:
        leg = flight["legs"][0]
        results.append({
            "from": leg["origin"]["displayCode"],
            "to": leg["destination"]["displayCode"],
            "price": flight.get("price", {}).get("formatted", ""),
            "duration": leg.get("durationInMinutes", "")
        })

    return results