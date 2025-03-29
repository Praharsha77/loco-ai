import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load API key from environment variable
API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"

def get_deepseek_response(message):
    if not API_KEY:
        return "Error: API Key is missing. Set the DEEPSEEK_API_KEY environment variable."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat-1.0",
        "messages": [{"role": "user", "content": message}],
        "temperature": 0.7,
        "max_tokens": 100
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()

        # Ensure the response contains the expected fields
        if "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"]
        return "Error: Invalid response from API."

    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    bot_response = get_deepseek_response(user_input)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
 