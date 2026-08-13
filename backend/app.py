from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import csv
import os

app = Flask(__name__)
CORS(app)  # allows the frontend (different origin) to call this API

LOG_FILE = "inquiries.csv"

@app.route("/api/inquiry", methods=["POST"])
def inquiry():
    data = request.get_json(force=True)

    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    message = data.get("message", "").strip()

    if not name or not phone:
        return jsonify({"error": "Name and phone are required"}), 400

    # --- Poor-man's database: append to a CSV file ---
    # Good enough for a single retailer's inquiry volume.
    # Swap this block for Google Sheets / Supabase / email later.
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "name", "phone", "message"])
        writer.writerow([datetime.now().isoformat(), name, phone, message])

    return jsonify({"status": "ok", "message": "Inquiry received"}), 200


@app.route("/api/inquiries", methods=["GET"])
def list_inquiries():
    # Simple endpoint for the shop owner to see all inquiries.
    # In production, put a password/token check here before deploying.
    if not os.path.isfile(LOG_FILE):
        return jsonify([])

    with open(LOG_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return jsonify(list(reader))


if __name__ == "__main__":
    app.run(port=5000, debug=True)
