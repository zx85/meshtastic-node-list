from flask import (
    Flask,
    request,
    make_response,
    jsonify,
    render_template,
    send_from_directory,
    abort,
    session,
)
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import os
import time
import functools
import logging
import json
import re
from includes.db import init_db, get_db_connection
from includes.poller import start_poller
from includes.feed import parse_feed

# Configure application

app = Flask(__name__, static_folder="static")
app.secret_key = os.environ.get("SECRET_KEY", "fallback-secret-key")

# Session cookie settings for reverse proxy/HTTPS at nginx
app.config["SESSION_COOKIE_SECURE"] = False  # HTTPS is terminated at nginx
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
node_db_file = os.environ.get("node_db_file", "/app/node_data/nodes.db")
meshtastic_device = os.environ.get("MESHTASTIC_DEVICE", "/dev/ttyUSB0")

# Initialize Database and Background Poller
init_db()
start_poller(meshtastic_device)

# Version
with open("version.txt") as vf:
    APP_VERSION = vf.read().strip()


@app.before_request
def log_request():
    logger.info(f"Request: {request.method} {request.path}")


@app.route("/")
def serve_index():
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM nodes ORDER BY last_heard DESC").fetchall()

    last_modified = "N/A"
    if rows:
        # Determine the latest update time from the node list
        max_lh = max((r["last_heard"] for r in rows if r["last_heard"]), default=0)
        if max_lh:
            dt = datetime.fromtimestamp(max_lh, tz=ZoneInfo("Europe/London"))
            last_modified = f'{dt.strftime("%Y-%m-%d %H:%M:%S")} UK time'

    headers, data = parse_feed(rows)
    return render_template(
        "index.html.j2",
        headers=headers,
        data=data,
        version=APP_VERSION,
        last_modified=last_modified,
        enumerate=enumerate,
    )


if __name__ == "__main__":
    try:
        from waitress import serve

        logger.info("Starting production server on HTTP...")
        serve(app, host="0.0.0.0", port=5000)
    except ImportError:
        logger.info("Starting development server on HTTP...")
        app.run(host="0.0.0.0", port=5000)
