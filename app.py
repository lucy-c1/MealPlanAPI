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

# returns recipes that match name
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

# returns recipes that match a single category, only has name, image info
@app.route('/api/search-category', methods=['GET'])
def search_category():
    headers = {
        "Access-Control-Allow-Origin": "*"
    }
    
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    response = requests.get(f'https://www.themealdb.com/api/json/v1/1/filter.php?c={query}')
    data = response.json()

    return jsonify(data), 200, headers

# returns recipes that match a single category, has all info
@app.route('/api/search-category-details', methods=['GET'])
def search_category_details():
    headers = {
        "Access-Control-Allow-Origin": "*"
    }

    category = request.args.get('q', '')
    if not category:
        return jsonify({'error': 'No category provided'}), 400, headers

    # Step 1: Get meals (basic info) for the category
    filter_response = requests.get(f'https://www.themealdb.com/api/json/v1/1/filter.php?c={category}')
    filter_data = filter_response.json()
    meals = filter_data.get('meals', [])

    if not meals:
        return jsonify({'meals': []}), 200, headers

    detailed_meals = []

    # Step 2: Get full meal details for each id
    for meal in meals:
        meal_id = meal.get('idMeal')
        if meal_id:
            detail_res = requests.get(f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}')
            detail_data = detail_res.json()
            if detail_data.get('meals'):
                detailed_meals.append(detail_data['meals'][0])

    return jsonify({'meals': detailed_meals}), 200, headers


# returns recipes that match a single area
@app.route('/api/search-area', methods=['GET'])
def search_area():
    headers = {
        "Access-Control-Allow-Origin": "*"
    }
    
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    response = requests.get(f'https://www.themealdb.com/api/json/v1/1/filter.php?a={query}')
    data = response.json()

    return jsonify(data), 200, headers

# returns recipes that match a single area, has all info
@app.route('/api/search-area-details', methods=['GET'])
def search_area_details():
    headers = {
        "Access-Control-Allow-Origin": "*"
    }

    area = request.args.get('q', '')
    if not area:
        return jsonify({'error': 'No category provided'}), 400, headers

    # Step 1: Get meals (basic info) for the area
    filter_response = requests.get(f'https://www.themealdb.com/api/json/v1/1/filter.php?a={area}')
    filter_data = filter_response.json()
    meals = filter_data.get('meals', [])

    if not meals:
        return jsonify({'meals': []}), 200, headers

    detailed_meals = []

    # Step 2: Get full meal details for each id
    for meal in meals:
        meal_id = meal.get('idMeal')
        if meal_id:
            detail_res = requests.get(f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}')
            detail_data = detail_res.json()
            if detail_data.get('meals'):
                detailed_meals.append(detail_data['meals'][0])

    return jsonify({'meals': detailed_meals}), 200, headers

if __name__ == "__main__":
    app.run(debug=True)