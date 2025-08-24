import os
import sys
import requests
import zipfile
import io
from datetime import datetime, timezone
from flask import Flask, jsonify, request
from pydantic import BaseModel, ValidationError
from auth_decorator import require_auth_from_identity

# Import the lifecycle modules
from modules import design_corporate_structure, STRUCTURE_TEMPLATE_MAP

app = Flask(__name__)

# --- Add common module to path ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'common')))
from secrets import get_secret

# --- Engine Service URLs ---
DRAFTING_SERVICE_URL = get_secret('drafting-service-url') or 'http://localhost:5001'
VAULT_SERVICE_URL = get_secret('vault-service-url') or 'http://localhost:5002'
ANALYTICS_SERVICE_URL = get_secret('eng-analytics-url') or 'http://localhost:5007'


from sqlalchemy import create_engine, text

# --- Database Setup ---
DB_URI = get_secret('sqlalchemy-database-uri') or 'sqlite:///eng_lifecycle.db'
engine = create_engine(DB_URI, future=True)

def init_db():
    with engine.begin() as conn:
        conn.execute(text('CREATE TABLE IF NOT EXISTS subscribers (email TEXT PRIMARY KEY, subscribed_at DATETIME)'))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS lifecycles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_email TEXT NOT NULL,
                advisor_email TEXT,
                flow_id TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL
            )
        """))

@app.before_request
def setup_db():
    if not hasattr(app, 'db_initialized'):
        init_db()
        app.db_initialized = True

# --- Models for Request Validation ---
class DesignBody(BaseModel):
    goals: list[str]
    jurisdiction: str

class PackBody(BaseModel):
    flow_id: str
    data: dict

# --- Service Endpoints ---
@app.route('/')
def index():
    return jsonify({"service": "eng-lifecycle", "status": "running"})

def _emit_event(event_type: str, payload: dict):
    """Helper to send an event to the analytics service."""
    try:
        user_id = request.current_user.get('email') if hasattr(request, 'current_user') else None
        event = {
            "event_type": event_type,
            "payload": payload,
            "service": "eng-lifecycle",
            "user_id": user_id
        }
        requests.post(f"{ANALYTICS_SERVICE_URL}/events/ingest", json=event, timeout=2)
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Failed to emit event {event_type}: {e}")

@app.route('/lifecycle/design', methods=['POST'])
def design_structure_endpoint():
    try:
        body = DesignBody(**request.get_json(force=True))
    except ValidationError as e:
        return jsonify({'ok': False, 'error': e.errors()}), 400

    try:
        result = design_corporate_structure(body.goals, body.jurisdiction)
        return jsonify({"ok": True, **result})
    except Exception as e:
        app.logger.error(f"An error occurred during structure design: {e}")
        return jsonify({"ok": False, "error": "An unexpected error occurred during design"}), 500


@app.route('/lifecycle/pack', methods=['POST'])
@require_auth_from_identity()
def generate_pack():
    try:
        body = PackBody(**request.get_json(force=True))
    except ValidationError as e:
        return jsonify({'ok': False, 'error': e.errors()}), 400

    context_data = body.data
    flow_id = body.flow_id

    # Look up the required templates from the imported map
    structure_info = STRUCTURE_TEMPLATE_MAP.get(flow_id)
    if not structure_info:
        return jsonify({"ok": False, "error": f"Flow ID '{flow_id}' not found."}), 404
    template_ids = structure_info['required_templates']

    try:
        # Pass the user's auth cookie to downstream services
        auth_cookie = request.cookies.get('access_token')
        downstream_cookies = {'access_token': auth_cookie} if auth_cookie else {}

        # Create an in-memory zip file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            # Iterate through templates and render each one
            for template_id in template_ids:
                # 1. Call eng-drafting to render the document
                drafting_payload = {"template_id": template_id, "data": context_data}
                # Drafting service is public, no auth needed for it.
                drafting_response = requests.post(f"{DRAFTING_SERVICE_URL}/doc/render", json=drafting_payload, timeout=30)
                drafting_response.raise_for_status()

                # Get filename from Content-Disposition header, or guess one
                content_disp = drafting_response.headers.get('Content-Disposition')
                filename = content_disp.split('filename=')[1] if content_disp else f"{template_id}.docx"

                # 2. Add the rendered file to the zip archive
                zip_file.writestr(filename, drafting_response.content)

        zip_buffer.seek(0)

        # 3. Upload the final zip file to eng-vault
        zip_filename = f"{flow_id}_pack.zip"
        files = {'file': (zip_filename, zip_buffer, 'application/zip')}
        vault_response = requests.post(
            f"{VAULT_SERVICE_URL}/vault/upload",
            files=files,
            cookies=downstream_cookies,
            timeout=30
        )
        vault_response.raise_for_status()

        pack_file_id = vault_response.json().get('file_id')

        # 4. Emit event and return the file_id of the zip package
        _emit_event("pack.generated", {
            "flow_id": flow_id,
            "pack_file_id": pack_file_id
        })

        return jsonify({"ok": True, "pack_file_id": pack_file_id})

    except requests.exceptions.RequestException as e:
        app.logger.error(f"A service call failed during pack generation: {e}")
        return jsonify({"ok": False, "error": "A required downstream service is unavailable."}), 503
    except Exception as e:
        app.logger.error(f"An error occurred during pack generation: {e}")
        return jsonify({"ok": False, "error": "An unexpected error occurred during pack generation"}), 500


# --- Models for Contact Form ---
class ContactBody(BaseModel):
    name: str
    email: str
    message: str

# --- API Key Decorator ---
from functools import wraps

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        internal_api_key = get_secret('internal-service-api-key')
        if not internal_api_key or not api_key or api_key != internal_api_key:
            return jsonify({'ok': False, 'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/v1/contact', methods=['POST'])
@require_api_key
def handle_contact_form():
    try:
        body = ContactBody(**request.get_json(force=True))
    except ValidationError as e:
        return jsonify({'ok': False, 'error': e.errors()}), 400

    # 1. Emit an event for analytics
    _emit_event("contact.form.submitted", {
        "name": body.name,
        "email": body.email,
    })

    # 2. Delegate email sending to eng-identity
    try:
        identity_service_url = get_secret('eng-identity-url') or 'http://localhost:5000'
        admin_email = get_secret('admin-email') or 'admin@assetarc.com'

        email_payload = {
            "recipient": admin_email,
            "subject": f"New Contact Form Submission from {body.name}",
            "body_text": f"Name: {body.name}\\nEmail: {body.email}\\n\\nMessage:\\n{body.message}"
        }

        # This endpoint will be protected by the same internal API key
        headers = {'x-api-key': get_secret('internal-service-api-key')}

        response = requests.post(
            f"{identity_service_url}/api/v1/send-system-email",
            json=email_payload,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()

        return jsonify({"ok": True, "message": "Message sent successfully."})

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Failed to send contact email via eng-identity: {e}")
        return jsonify({"ok": False, "error": "Failed to send message due to an internal error."}), 503
    except Exception as e:
        app.logger.error(f"An unexpected error occurred in contact form handling: {e}")
        return jsonify({"ok": False, "error": "An unexpected error occurred."}), 500

# --- Models for Newsletter Subscription ---
class SubscribeBody(BaseModel):
    email: str

@app.route('/api/v1/subscribe', methods=['POST'])
@require_api_key
def handle_subscription():
    try:
        body = SubscribeBody(**request.get_json(force=True))
    except ValidationError as e:
        return jsonify({'ok': False, 'error': e.errors()}), 400

    try:
        with engine.begin() as conn:
            # Use INSERT OR IGNORE to prevent errors on duplicate subscriptions
            conn.execute(
                text('INSERT OR IGNORE INTO subscribers (email, subscribed_at) VALUES (:email, :now)'),
                {'email': body.email, 'now': datetime.now(timezone.utc)}
            )

        _emit_event("newsletter.subscribed", {"email": body.email})

        return jsonify({"ok": True, "message": "Successfully subscribed."})

    except Exception as e:
        app.logger.error(f"An unexpected error occurred during subscription: {e}")
        return jsonify({"ok": False, "error": "An unexpected error occurred."}), 500

@app.route('/api/v1/clients', methods=['GET'])
@require_api_key
def get_clients_by_advisor():
    advisor_email = request.args.get('advisor_email')
    if not advisor_email:
        return jsonify({'ok': False, 'error': 'advisor_email parameter is required'}), 400

    # In a real implementation, this would query the lifecycles table.
    # For now, return placeholder data.
    placeholder_clients = [
        {
            "email": "client1@example.com",
            "status": "Pending Review",
            "last_activity": "2023-10-26T10:00:00Z",
            "vault_url": "/vault/client/client1@example.com"
        },
        {
            "email": "client2@example.com",
            "status": "Active",
            "last_activity": "2023-10-25T14:30:00Z",
            "vault_url": "/vault/client/client2@example.com"
        }
    ]

    return jsonify({"ok": True, "clients": placeholder_clients})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
