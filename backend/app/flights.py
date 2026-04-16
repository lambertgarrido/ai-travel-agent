import requests
import os

API_KEY = os.getenv("RAPIDAPI_KEY")

CITY_TO_IATA = {
    "new york": "JFK",
    "paris": "CDG",
    "london": "LHR",
    "tokyo": "HND",
    "rome": "FCO",
    "atlanta": "ATL"
}

def get_iata(city):
    if not city:
        return None
    return CITY_TO_IATA.get(city.lower())

def search_flights(origin, destination, date):
    url = "https://skyscanner-flights-travel-api.p.rapidapi.com/flights/searchFlights"

    origin_code = get_iata(origin)
    destination_code = get_iata(destination)

    if not origin_code or not destination_code:
        return []

    querystring = {
        "origin": origin_code,
        "destination": destination_code,
        "departureDate": date,
        "adults": "1",
        "currency": "USD"
    }

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "skyscanner-flights-travel-api.p.rapidapi.com"
    }

    params = {
        "countryCode": "US",
        "market": "US",
        "currency": "USD",
        "adults": "1",
        "childrens": "0",
        "infants": "0",
        "cabinClass": "economy",

        # ✅ Example: London → New York
        "originSkyId": "LOND",
        "destinationSkyId": "NYCA",
        "originEntityId": "27544008",
        "destinationEntityId": "27537542",

        "date": "2026-08-01",
        "returnDate": "2026-08-15"
    }

    response = requests.get(url, headers=headers, params=params)

    data = response.json()
    print("RAW SKYSCANNER RESPONSE:", data)

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