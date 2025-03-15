import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("HOTELBEDS_API_KEY")
SECRET = os.getenv("HOTELBEDS_SECRET")

@app.route("/search-hotels", methods=["GET"])
def search_hotels():
    try:
        if not API_KEY or not SECRET:
            return jsonify({"error": "Missing API keys!"}), 500

        # Example request to Hotelbeds API
        headers = {
            "Api-key": API_KEY,
            "X-Signature": SECRET,
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
