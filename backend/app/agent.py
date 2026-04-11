from logging import info
from re import search

from openai import OpenAI
from app.places import get_places
from app.flights import search_flights
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_agent(message: str, user_id: str):

    if "flight" in message.lower() or "flights" in message.lower():
        info = extract_flight_info(message)

        origin = info.get("origin")
        destination = info.get("destination")
        date = info.get("date")

        if not origin or not destination:
            return {
                "type": "text",
                "data": "Please specify origin and destination."
            }

        flights = search_flights(origin, destination, date)

        return {
            "type": "flights",
            "data": flights
        }

    if "things to do" in message.lower():
        city = extract_city(message)

        if not city:
            return {"type": "text", "data": "Please specify a city."}

        places = get_places(city)

        return {
            "type": "places",
            "data": places
        }

    system_prompt = """
    You are an AI travel agent.
    Help users plan trips with:
    - destinations
    - itinerary
    - travel tips
    - budget suggestions
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
        temperature=0.7,
    )

    return {
        "type": "text",
        "data": response.choices[0].message.content
    }   

def extract_city(message: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Extract the city name from the user's message. Return JSON: {\"city\": \"...\"}"
            },
            {"role": "user", "content": message}
        ],
        response_format={"type": "json_object"}
    )

    data = json.loads(response.choices[0].message.content)
    return data.get("city")

import json

def extract_flight_info(message: str):

    flight_system_prompt = """
    Extract flight search info from user input.
    Return JSON with:
    {
        "origin": "...",
        "destination": "...",
        "date": "YYYY-MM-DD"
    }
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": flight_system_prompt},
            {"role": "user", "content": message},
        ],
        response_format={"type": "json_object"}
    )

    data = json.loads(response.choices[0].message.content)
    return data
