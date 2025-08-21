
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
import os
import hmac
import hashlib
import tempfile
import requests
import zipfile
import subprocess
from flask import request, jsonify, abort

GITHUB_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")

@app.route('/anansi/update', methods=['POST'])
def anansi_update():
    # Step 1: Verify signature
    signature = request.headers.get('X-Hub-Signature-256')
    if not is_valid_signature(request.data, signature):
        abort(403, 'Invalid webhook signature')

    payload = request.get_json()

    try:
        # Step 2: Get repo info
        repo = payload['repository']['clone_url']
        ref = payload['ref']
        branch = ref.split("/")[-1]
        zip_url = f"{repo.replace('.git', '')}/archive/refs/heads/{branch}.zip"

        # Step 3: Download zip
        zip_response = requests.get(zip_url)
        if zip_response.status_code != 200:
            return jsonify({"error": "Failed to download ZIP"}), 500

        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "update.zip")
            with open(zip_path, "wb") as f:
                f.write(zip_response.content)

            # Step 4: Extract ZIP
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)

            # Step 5: Run update.py inside extracted folder
            for root, dirs, files in os.walk(tmpdir):
                if "update.py" in files:
                    result = subprocess.run(["python", os.path.join(root, "update.py")], capture_output=True, text=True)
                    if result.returncode != 0:
                        return jsonify({
                            "error": "Update script failed",
                            "output": result.stdout,
                            "stderr": result.stderr
                        }), 500
                    return jsonify({"status": "Update successful", "output": result.stdout})

        return jsonify({"error": "No update.py found in zip"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def is_valid_signature(payload, signature):
    if not GITHUB_SECRET or not signature:
        return False
    sha_name, signature = signature.split('=')
    mac = hmac.new(GITHUB_SECRET.encode(), msg=payload, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature)
