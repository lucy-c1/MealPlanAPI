from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Allow frontend requests

@app.route("/api/hello")
def hello():
    return jsonify(message="Hello from Flask!")

# gets a single recipe from the mealdb API
@app.route("/get-recipe", methods=["GET", "OPTIONS"])
def get_recipe():
    # CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Max-Age": "3600",
    }

    # Handle preflight
    if request.method == "OPTIONS":
        return ("", 204, headers)

    # Make API request to TheMealDB
    response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php")

    # Return JSON with headers
    return jsonify(response.json()), 200, headers

if __name__ == "__main__":
    app.run(debug=True)