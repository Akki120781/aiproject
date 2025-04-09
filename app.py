"""from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# It's better to get the API key from environment variables for security
API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyAqJXj39JAabzqLXsPykvwe6q6u4KYWPb4")
if not API_KEY:
    raise ValueError("API key not found! Set GOOGLE_API_KEY as an environment variable.")

# Configure the generative AI model
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro-latest')

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    # Check if request has JSON data
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    prompt = data.get("prompt", "")
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    try:
        # Generate content with more specific instructions
        response = model.generate_content(
            f"Provide detailed software recommendations for: {prompt}. "
            "Format the response with clear sections for each recommendation including: "
            "1. Software Name, 2. Description, 3. Key Features, 4. Pricing information, "
            "5. Official website link. Organize the information in a structured way."
        )
        
        # Check if the response was successful
        if not response.text:
            return jsonify({"error": "No response from AI model"}), 500
            
        return jsonify({
            "recommendations": response.text,
            "status": "success"
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error generating recommendations: {str(e)}")
        return jsonify({
            "error": "Failed to generate recommendations",
            "details": str(e),
            "status": "error"
        }), 500

if __name__ == "__main__":
    # For production, you might want to turn off debug mode
    app.run(debug=True, host="0.0.0.0", port=5000)

    """
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = "AIzaSyCMNFRg6MLEVOzRycsZKqLlNivGpGwba5o"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {"parts": [{"text": f"Provide detailed software recommendations for: {prompt}. Include name, description, key features, pricing (if applicable), and official website links."}]}
        ]
    }

    try:
        response = requests.post(GEMINI_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()

        content = result.get("candidates", [{}])[0].get("content", {})
        text = " ".join([p.get("text", "") for p in content.get("parts", [])])

        return jsonify({
            "recommendations": text,
            "status": "success"
        })
    except requests.RequestException as e:
        return jsonify({
            "error": f"Request error: {str(e)}",
            "status": "error"
        }), 500
    except Exception as e:
        return jsonify({
            "error": f"Unexpected error: {str(e)}",
            "status": "error"
        }), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

API_KEY = "AIzaSyAqJXj39JAabzqLXsPykvwe6q6u4KYWPb4"
if not API_KEY:
    raise ValueError("API key not found! Set GOOGLE_API_KEY as an environment variable.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro-latest')

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    prompt = data.get("prompt", "")
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    try:
        response = model.generate_content(f"Provide detailed software recommendations for: {prompt}. Include name, description, key features, pricing (if applicable), and official website links.")
        return jsonify({
            "recommendations": response.text,
            "status": "success"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
