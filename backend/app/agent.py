from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_agent(message: str, user_id: str):
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

    return response.choices[0].message.content