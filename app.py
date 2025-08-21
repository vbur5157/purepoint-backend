from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "PurePoint AI Backend is running!"

@app.route("/ask-anansi", methods=["POST"])
def ask_anansi():
    try:
        data = request.get_json()
        prompt = data.get("prompt")
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are Anansi, a helpful, sarcastic, and professional assistant for PurePoint."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return jsonify({"response": response.choices[0].message.content.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
import zipfile
import requests

@app.route("/webhook", methods=["POST"])
def github_webhook():
    try:
        # Step 1: Download latest update zip from GitHub repo
        zip_url = "https://github.com/<your-username>/<repo-name>/raw/main/anansi-update.zip"
        response = requests.get(zip_url)
        zip_path = "anansi-update.zip"
        with open(zip_path, "wb") as f:
            f.write(response.content)

        # Step 2: Extract the ZIP
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("anansi_modules")

        # Step 3: (Optional) Execute update.py from bundle
        exec(open("anansi_modules/update.py").read(), globals())

        return jsonify({"status": "Update applied successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
