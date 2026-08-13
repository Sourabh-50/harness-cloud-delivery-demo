import os
from flask import Flask, jsonify

app = Flask(__name__)

# Application Version metadata
APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")
GIT_COMMIT = os.environ.get("GIT_COMMIT", "unknown")


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Harness Cloud Delivery Demo",
        "platform": "Harness Cloud CI/CD",
        "status": "active"
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "checks": {
            "uptime": "ok",
            "database": "n/a"
        }
    }), 200


@app.route("/version", methods=["GET"])
def version():
    return jsonify({
        "version": APP_VERSION,
        "commit": GIT_COMMIT
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
