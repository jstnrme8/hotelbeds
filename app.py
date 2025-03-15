from flask import Flask, jsonify
from flask_cors import CORS  # ✅ Import CORS
import os
import requests
import time
import hashlib

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all routes

API_KEY = os.getenv("HOTELBEDS_API_KEY")
SECRET = os.getenv("HOTELBEDS_SECRET")

def generate_signature():
    timestamp = str(int(time.time()))  # Current UNIX timestamp
    raw_signature = API_KEY + SECRET + timestamp
    signature = hashlib.sha256(raw_signature.encode()).hexdigest()
    return signature

@app.route("/search-hotels", methods=["GET"])
def search_hotels():
    try:
        if not API_KEY or not SECRET:
            return jsonify({"error": "Missing API keys!"}), 500

        headers = {
            "Api-key": API_KEY,
            "X-Signature": generate_signature(),
            "Accept": "application/json",
        }
        
        response = requests.get("https://api.test.hotelbeds.com/hotel-api/3.0/hotels", headers=headers)
        
        if response.status_code != 200:
            return jsonify({"error": f"Hotelbeds API error: {response.status_code}", "details": response.text}), 500
        
        return response.json()
    
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
