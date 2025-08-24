import os
import sys
import json
from flask import Flask, jsonify, request, render_template
from pydantic import BaseModel, ValidationError
from sqlalchemy import create_engine, text
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

# --- Add common module to path ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'common')))
from secrets import get_secret

# --- Configuration ---
DB_URI = get_secret('postgres-uri') or get_secret('analytics-db-uri') or 'sqlite:///eng_analytics.db'

# --- Database Setup ---
engine = create_engine(DB_URI, future=True)

def init_db():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                payload TEXT,
                service TEXT,
                user_id TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """))

@app.before_request
def setup_db():
    if not hasattr(app, 'db_initialized'):
        init_db()
        app.db_initialized = True

# --- Models for Request Validation ---
class EventBody(BaseModel):
    event_type: str
    payload: dict
    service: str | None = None
    user_id: str | None = None

# --- Service Endpoints ---
@app.route('/')
def index():
    return jsonify({"service": "eng-analytics", "status": "running"})

@app.route('/events/ingest', methods=['POST'])
def ingest_event():
    try:
        body = EventBody(**request.get_json(force=True))
    except ValidationError as e:
        return jsonify({'ok': False, 'error': e.errors()}), 400

    # In a real implementation, this might go to a message queue first.
    # For now, we'll write directly to the database.
    try:
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO events (event_type, payload, service, user_id, created_at)
                VALUES (:event_type, :payload, :service, :user_id, :created_at)
            """), {
                "event_type": body.event_type,
                "payload": json.dumps(body.payload),
                "service": body.service,
                "user_id": body.user_id,
                "created_at": datetime.now(timezone.utc)
            })
        return jsonify({"ok": True, "message": "Event ingested successfully."}), 202
    except Exception as e:
        app.logger.error(f"Failed to ingest event: {e}")
        return jsonify({"ok": False, "error": "Failed to store event."}), 500


def _get_kpi_data():
    """Helper function to query the database for KPI data."""
    time_window = datetime.now(timezone.utc) - timedelta(hours=24)

    with engine.connect() as conn:
        signups = conn.execute(text(
            "SELECT COUNT(*) FROM events WHERE event_type = :event AND created_at >= :window"
        ), {"event": "user.created", "window": time_window}).scalar_one_or_none() or 0

        logins = conn.execute(text(
            "SELECT COUNT(*) FROM events WHERE event_type = :event AND created_at >= :window"
        ), {"event": "user.login", "window": time_window}).scalar_one_or_none() or 0

        packs = conn.execute(text(
            "SELECT COUNT(*) FROM events WHERE event_type = :event AND created_at >= :window"
        ), {"event": "pack.generated", "window": time_window}).scalar_one_or_none() or 0

    return {
        "users_created_today": signups,
        "logins_today": logins,
        "packs_generated_today": packs
    }

@app.route('/analytics/kpi', methods=['GET'])
def get_kpi():
    """
    Computes and returns key performance indicators from the events data as JSON.
    """
    try:
        kpi_data = _get_kpi_data()
        return jsonify({
            "ok": True,
            "kpis": kpi_data,
            "time_window_hours": 24
        })
    except Exception as e:
        app.logger.error(f"Failed to compute KPIs: {e}")
        return jsonify({"ok": False, "error": "Failed to compute KPIs."}), 500

@app.route('/analytics/dashboard', methods=['GET'])
def get_dashboard():
    """
    Renders an HTML dashboard visualizing the KPIs.
    """
    try:
        kpi_data = _get_kpi_data()
        return render_template('dashboard.html', kpi_data=kpi_data)
    except Exception as e:
        app.logger.error(f"Failed to render dashboard: {e}")
        return "Error loading dashboard.", 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5007)
