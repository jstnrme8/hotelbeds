from flask import Flask, request, jsonify
from flask_cors import CORS  
import os
import requests
import time
import hashlib
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Change * to your frontend URL in production


API_KEY = os.getenv("HOTELBEDS_API_KEY")
SECRET = os.getenv("HOTELBEDS_SECRET")

def generate_signature():
    timestamp = str(int(time.time()))  # Current UNIX timestamp
    raw_signature = API_KEY + SECRET + timestamp
    signature = hashlib.sha256(raw_signature.encode()).hexdigest()
    return signature

@app.route("/search-hotels", methods=["GET", "POST"])  # ✅ Allow GET and POST
def search_hotels():
    try:
        if not API_KEY or not SECRET:
            return jsonify({"error": "Missing API keys!"}), 500

        headers = {
            "Api-key": API_KEY,
            "X-Signature": generate_signature(),
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        # Get search parameters from request
        data = request.get_json()
        destination = data.get("destination", "BCN")  
        check_in = data.get("check_in", "2025-04-01")
        check_out = data.get("check_out", "2025-04-05")
        adults = int(data.get("adults", 2))
        rooms = int(data.get("rooms", 1))


        # Create the Hotelbeds API request payload
        payload = {
            "stay": {"checkIn": check_in, "checkOut": check_out},
            "occupancies": [{"rooms": rooms, "adults": adults, "children": 0}],
            "destination": {"code": destination}
        }

        response = requests.post(
            "https://api.test.hotelbeds.com/hotel-api/3.0/hotels",
            headers=headers,
            json=payload  
        )

        if response.status_code != 200:
            return jsonify({"error": f"Hotelbeds API error: {response.status_code}", "details": response.text}), 500
        
        # Limit results to 10 hotels
        hotels_data = response.json().get("hotels", {}).get("hotels", [])
        limited_hotels = hotels_data[:10]  # Only return the first 10 hotels

        return jsonify({"hotels": limited_hotels})
    
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
