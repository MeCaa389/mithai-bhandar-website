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
ADMIN_KEY = os.environ.get("ADMIN_KEY")  # set this in Render env vars too

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route("/api/inquiry", methods=["POST"])
def inquiry():
    data = request.get_json(force=True)

    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    message = data.get("message", "").strip()

    if not name or not phone:
        return jsonify({"error": "Name and phone are required"}), 400

    try:
        result = supabase.table("inquiries").insert({
            "name": name,
            "phone": phone,
            "message": message
        }).execute()
    except Exception as e:
        print("Supabase insert failed:", e)
        return jsonify({"error": "Could not save inquiry", "details": str(e)}), 500

    return jsonify({"status": "ok", "message": "Inquiry received"}), 200


@app.route("/api/inquiries", methods=["GET"])
def list_inquiries():
    # Requires a secret key in the request header — set ADMIN_KEY in
    # Render's environment variables, then view inquiries by visiting:
    # https://your-backend.onrender.com/api/inquiries?key=YOUR_ADMIN_KEY
    provided_key = request.args.get("key")
    if not ADMIN_KEY or provided_key != ADMIN_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    result = supabase.table("inquiries").select("*").order("created_at", desc=True).execute()
    return jsonify(result.data)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
