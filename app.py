from flask import Flask, request, jsonify
import hashlib
import time
import requests
from flask_cors import CORS  # Allows frontend to call API
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

def get_signature():
    timestamp = str(int(time.time()))
    signature = hashlib.sha256((API_KEY + API_SECRET + timestamp).encode()).hexdigest()
    return signature, timestamp

@app.route("/search-hotels", methods=["GET"])
def search_hotels():
    signature, timestamp = get_signature()
    
    headers = {
        "Api-key": API_KEY,
        "X-Signature": signature,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    payload = {
        "stay": {"checkIn": "2025-04-01", "checkOut": "2025-04-05"},
        "occupancies": [{"rooms": 1, "adults": 2, "children": 0}],
        "destination": {"code": "BCN"}  # Example for Barcelona
    }

    url = "https://api.test.hotelbeds.com/hotel-api/1.0/hotels"
    response = requests.post(url, json=payload, headers=headers)
    
    data = response.json()

    # Debugging: Print response
    print("Hotelbeds Response:", data)

    # Extract only the hotels list and limit to 10
    hotels = data.get("hotels", {}).get("hotels", [])[:10]

    formatted_hotels = []
    for hotel in hotels:
        formatted_hotels.append({
            "name": hotel.get("name", "No Name"),
            "address": hotel.get("destinationName", "Unknown Address"),
            "price": hotel.get("minRate", "N/A"),
            "currency": hotel.get("currency", "N/A"),
            "latitude": hotel.get("latitude"),
            "longitude": hotel.get("longitude")
        })

    return jsonify({"hotels": formatted_hotels})



if __name__ == "__main__":
    app.run(debug=True)
