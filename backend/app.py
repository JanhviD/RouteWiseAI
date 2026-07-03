from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import google.generativeai as genai
import requests
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

# ---------------- DATABASE ----------------

# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="Mysqljd@247",
#     database="routewise_ai"
# )

# cursor = db.cursor()

# ---------------- GEMINI ----------------

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- WEATHER ----------------

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


@app.route("/")
def home():
    return "RouteWise AI Backend Running"


@app.route("/generate-trip", methods=["POST"])
def generate_trip():

    data = request.json

    destination = data.get("destination")
    budget = data.get("budget")
    days = data.get("days")
    travel_style = data.get("travelStyle")

    # Save trip in database

# cursor.execute(
#     """
#     INSERT INTO trips (destination, budget, days, travel_style)
#     VALUES (%s, %s, %s, %s)
#     """,
#     (destination, budget, days, travel_style)
# )

# db.commit()

    # Gemini Prompt
    prompt = f"""
Create a {days}-day travel itinerary for {destination}.

Budget: ₹{budget}
Travel Style: {travel_style}

Return ONLY this format.

📅 Day 1
• 2-3 places to visit
• 1 local food to try

📅 Day 2
• 2-3 places to visit
• 1 local food to try

📅 Day 3
• 2-3 places to visit
• 1 local food to try

⭐ Top Attractions
• Maximum 4

🍴 Must-Try Food
• Maximum 4

💡 Travel Tips
• Maximum 4 short points

Rules:
- Do NOT explain anything.
- Do NOT write introductions or conclusions.
- Do NOT write paragraphs.
- Keep the answer under 250 words.
"""
    response = model.generate_content(prompt)

    ai_plan = response.text

    # Weather API
    weather_url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={destination}&appid={WEATHER_API_KEY}&units=metric"
    )

    weather_response = requests.get(weather_url)

    weather_data = weather_response.json()

    if weather_response.status_code == 200:

        temperature = weather_data["main"]["temp"]
        condition = weather_data["weather"][0]["description"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]

    else:

        temperature = "N/A"
        condition = "Not Available"
        humidity = "N/A"
        wind_speed = "N/A"

    return jsonify({

        "destination": destination,
        "budget": budget,
        "days": days,
        "travelStyle": travel_style,
        "tripPlan": ai_plan,

        "temperature": temperature,
        "condition": condition,
        "humidity": humidity,
        "windSpeed": wind_speed

    })


if __name__ == "__main__":
    app.run(debug=True)