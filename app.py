import json
import logging
import os
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data.json"


app = Flask(__name__)

# Configure basic debug-friendly logging.
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def get_mongo_collection():
    """
    Create and return the MongoDB collection object.
    Uses an environment variable when available, otherwise falls back
    to a placeholder connection string that should be replaced.
    """
    mongo_uri = os.getenv(
        "MONGODB_URI",
        "mongodb+srv://<username>:<password>@<cluster-url>/"
        "?retryWrites=true&w=majority&appName=Cluster0",
    )
    client = MongoClient(mongo_uri)
    db = client["testdb"]
    return db["users"]


@app.route("/api", methods=["GET"])
def api():
    """Read local JSON data and return it as an API response."""
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        logger.debug("Loaded %s records from %s", len(data), DATA_FILE)
        return jsonify(data)
    except FileNotFoundError:
        logger.exception("data.json file was not found.")
        return jsonify({"error": "data.json file not found"}), 404
    except json.JSONDecodeError:
        logger.exception("data.json contains invalid JSON.")
        return jsonify({"error": "Invalid JSON format in data.json"}), 500
    except Exception as exc:
        logger.exception("Unexpected error while reading API data: %s", exc)
        return jsonify({"error": "Unable to load data"}), 500


@app.route("/", methods=["GET", "POST"])
def form():
    """Render the form and handle submissions to MongoDB Atlas."""
    error_message = None
    name = ""
    email = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        logger.debug("Received form submission for name=%s email=%s", name, email)

        if not name or not email:
            error_message = "Both name and email are required."
            logger.warning("Validation failed: missing required fields.")
            return render_template(
                "form.html",
                error_message=error_message,
                name=name,
                email=email,
            )

        try:
            users_collection = get_mongo_collection()
            result = users_collection.insert_one({"name": name, "email": email})
            logger.debug("Inserted document into MongoDB with id=%s", result.inserted_id)
            return redirect(url_for("success"))
        except PyMongoError as exc:
            error_message = f"Database error: {exc}"
            logger.exception("MongoDB insertion failed: %s", exc)
        except Exception as exc:
            error_message = f"Unexpected error: {exc}"
            logger.exception("Unexpected insertion error: %s", exc)

    return render_template(
        "form.html",
        error_message=error_message,
        name=name,
        email=email,
    )


@app.route("/success", methods=["GET"])
def success():
    """Display a success message after a successful submission."""
    return render_template("success.html")


if __name__ == "__main__":
    logger.debug("Starting Flask application...")
    app.run(debug=True)
