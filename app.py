
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
from anansi.core import generate_response

load_dotenv()
app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "Anansi AI Backend is live."

@app.route("/ask-anansi", methods=["POST"])
def ask_anansi():
    try:
        data = request.get_json()
        prompt = data.get("prompt")
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400
        response = generate_response(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
