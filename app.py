from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)  # Allow frontend requests

@app.route("/api/hello")
def hello():
    return jsonify(message="Hello from Flask!")

# gets a single recipe from the mealdb API
@app.route("/get-recipe", methods=["GET"])
def get_recipe():
    headers = {
        "Access-Control-Allow-Origin": "*"
    }

    try:
        response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php", timeout=5)
        response.raise_for_status()  # Handle 4xx and 5xx
        data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Request to TheMealDB failed", "details": str(e)}), 502, headers
    except ValueError:
        return jsonify({"error": "Invalid JSON returned from TheMealDB"}), 502, headers
    
    time.sleep(0.1)

    return jsonify(data), 200, headers

@app.route('/api/search', methods=['GET'])
def search_recipe():
    headers = {
        "Access-Control-Allow-Origin": "*"
    }
    
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    response = requests.get(f'https://www.themealdb.com/api/json/v1/1/search.php?s={query}')
    data = response.json()

    return jsonify(data), 200, headers

if __name__ == "__main__":
    app.run(debug=True)