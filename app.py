from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)

# -----------------------------
# MongoDB Atlas Configuration
# -----------------------------

MONGO_URI = os.getenv("MONGO_URI")

client = None
collection = None

if MONGO_URI:
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

        # Database name
        db = client["flask_assignment"]

        # Collection name
        collection = db["submissions"]

        # Test MongoDB connection
        client.admin.command("ping")

        print("MongoDB Atlas connected successfully.")

    except Exception as e:
        print("MongoDB connection failed:", e)


# -----------------------------
# Task 1: JSON API Route
# -----------------------------

@app.route("/api")
def api():

    try:
        with open("backend/data.json", "r") as file:
            data = json.load(file)

        return jsonify(data)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# -----------------------------
# Task 2: Frontend Form
# -----------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    error = None

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        # Basic validation
        if not name or not email or not message:
            error = "All fields are required."

            return render_template(
                "index.html",
                error=error,
                name=name,
                email=email,
                message=message
            )

        # Check MongoDB connection
        if collection is None:
            error = "MongoDB connection is not available."

            return render_template(
                "index.html",
                error=error,
                name=name,
                email=email,
                message=message
            )

        try:

            document = {
                "name": name,
                "email": email,
                "message": message
            }

            collection.insert_one(document)

            return redirect(url_for("success"))

        except Exception as e:

            error = f"Database error: {str(e)}"

            return render_template(
                "index.html",
                error=error,
                name=name,
                email=email,
                message=message
            )

    return render_template("index.html")




@app.route("/success")
def success():

    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)