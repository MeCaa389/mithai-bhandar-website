from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
import os

app = Flask(__name__)
CORS(app)

# Read from environment variables — set these in Render's dashboard,
# never hardcode keys directly in code that goes to GitHub.
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route("/api/inquiry", methods=["POST"])
def inquiry():
    data = request.get_json(force=True)

    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    message = data.get("message", "").strip()

    if not name or not phone:
        return jsonify({"error": "Name and phone are required"}), 400

    result = supabase.table("inquiries").insert({
        "name": name,
        "phone": phone,
        "message": message
    }).execute()

    return jsonify({"status": "ok", "message": "Inquiry received"}), 200


@app.route("/api/inquiries", methods=["GET"])
def list_inquiries():
    # In production, put a password/token check here before deploying —
    # right now anyone with the URL can see all inquiries.
    result = supabase.table("inquiries").select("*").order("created_at", desc=True).execute()
    return jsonify(result.data)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
