import json
import os

from flask import Flask, Response

PORT = int(os.environ.get("PORT", 8080))

app = Flask(__name__)


def _json(payload):
    # Use json.dumps (not jsonify) to keep the exact "key": "value"
    # spacing the CI smoke tests grep for.
    return Response(json.dumps(payload), mimetype="application/json")


@app.route("/healthz")
def healthz():
    return _json({"status": "ok"})


@app.route("/")
def index():
    # Optional failure injection for DORA change-failure simulation:
    # when FAIL_REQUESTS is truthy, app routes return 500 while
    # /healthz stays OK, so the pod stays Ready but requests fail.
    if os.environ.get("FAIL_REQUESTS", "").lower() in ("1", "true", "yes"):
        return _json({"error": "Simulated failure"}), 500
    return _json({"message": "Hello from Python webserver Juro Dora Test"})


if __name__ == "__main__":
    print(f"Listening on port {PORT}")
    app.run(host="0.0.0.0", port=PORT)
