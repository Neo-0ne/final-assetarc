import os
import bcrypt
import uuid
import functools
import boto3
import requests
from botocore.exceptions import ClientError
from datetime import datetime, timedelta, timezone
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from itsdangerous import URLSafeTimedSerializer, BadSignature

# --- App Initialization ---
load_dotenv()
app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}}) # Adjust origins as needed

# --- Configuration ---
JWT_SECRET = os.getenv('JWT_SECRET', 'a-super-secret-key-that-should-be-changed')
ACCESS_TOKEN_TTL_MIN = int(os.getenv('ACCESS_TOKEN_TTL_MIN', '15'))
REFRESH_TOKEN_TTL_DAYS = int(os.getenv('REFRESH_TOKEN_TTL_DAYS', '30'))
OTP_TTL_MIN = int(os.getenv('OTP_TTL_MIN', '10'))
COOKIE_SECURE = os.getenv('COOKIE_SECURE', 'False').lower() == 'true'
COOKIE_DOMAIN = None if os.getenv('COOKIE_DOMAIN', 'localhost') == 'localhost' else os.getenv('COOKIE_DOMAIN')
DB_URI = os.getenv('POSTGRES_URI') or os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///eng_identity.db')
SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'noreply@assetarc.com')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
ANALYTICS_SERVICE_URL = os.getenv('ENG_ANALYTICS_URL', 'http://localhost:5007')

# --- Services ---
signer = URLSafeTimedSerializer(JWT_SECRET)
engine = create_engine(DB_URI, future=True)
ses_client = boto3.client('ses', region_name=AWS_REGION)

# --- Database Setup ---
def init_db():
    with engine.begin() as conn:
        conn.execute(text('CREATE TABLE IF NOT EXISTS users(email TEXT PRIMARY KEY, role TEXT, is_active BOOLEAN DEFAULT 1, created_at DATETIME)'))
        conn.execute(text('CREATE TABLE IF NOT EXISTS otps(email TEXT, hash BLOB, exp DATETIME)'))
        conn.execute(text('CREATE TABLE IF NOT EXISTS refresh_tokens(jti TEXT PRIMARY KEY, email TEXT, exp DATETIME)'))
        conn.execute(text('CREATE TABLE IF NOT EXISTS client_tokens(token TEXT PRIMARY KEY, client_email TEXT, advisor_email TEXT, reason TEXT, created_at DATETIME, exp DATETIME)'))

@app.before_request
def setup_db():
    if not hasattr(app, 'db_initialized'):
        init_db()
        app.db_initialized = True

# --- Auth Decorators & Helpers ---
def _set_cookie(resp, name, val, max_age):
    resp.set_cookie(name, val, max_age=max_age, httponly=True, samesite='Lax', secure=COOKIE_SECURE, domain=COOKIE_DOMAIN)

def get_user_from_token():
    token = request.cookies.get('access_token')
    if not token:
        return None
    try:
        payload = signer.loads(token, max_age=60 * ACCESS_TOKEN_TTL_MIN * 2)
        if payload.get('type') != 'access':
            return None
        email = payload.get('sub')
        with engine.connect() as conn:
            user = conn.execute(text('SELECT email, role, is_active FROM users WHERE email=:e'), {'e': email}).first()
        return user
    except (BadSignature, TypeError, KeyError):
        return None

def require_auth(role=None):
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_user_from_token()
            if not user or not user.is_active:
                return jsonify({"ok": False, "error": "Authentication required"}), 401
            if role and user.role != role:
                return jsonify({"ok": False, "error": "Forbidden"}), 403
            request.current_user = user
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def _emit_event(event_type: str, payload: dict, user_id: str = None):
    """Helper to send an event to the analytics service."""
    try:
        event = {
            "event_type": event_type,
            "payload": payload,
            "service": "eng-identity",
            "user_id": user_id
        }
        requests.post(f"{ANALYTICS_SERVICE_URL}/events/ingest", json=event, timeout=2)
    except requests.exceptions.RequestException as e:
        # Log the error but don't fail the request
        app.logger.error(f"Failed to emit event {event_type}: {e}")

# --- Core Endpoints ---
@app.route('/')
def index():
    return jsonify({"service": "eng-identity", "status": "running"})

@app.route('/auth/request-otp', methods=['POST'])
def request_otp():
    email = (request.json or {}).get('email', '').strip().lower()
    if not email: return jsonify({'ok': False, 'error': 'email required'}), 400

    code = str(uuid.uuid4().int)[-6:]
    hashed_code = bcrypt.hashpw(code.encode(), bcrypt.gensalt())
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=OTP_TTL_MIN)

    # Store user and OTP in database
    with engine.begin() as conn:
        user_exists = conn.execute(text('SELECT 1 FROM users WHERE email=:e'), {'e': email}).first()
        if not user_exists:
            conn.execute(text('INSERT INTO users(email, role, created_at) VALUES (:e, :r, :t)'), {'e': email, 'r': 'client', 't': datetime.now(timezone.utc)})
            _emit_event("user.created", {"source": "otp_request"}, user_id=email)

        conn.execute(text('DELETE FROM otps WHERE email=:e'), {'e': email})
        conn.execute(text('INSERT INTO otps(email, hash, exp) VALUES (:e, :h, :x)'), {'e': email, 'h': hashed_code, 'x': expires_at})

    # Send OTP via email
    email_subject = "Your AssetArc Login OTP"
    email_body = f"Your one-time password is: {code}\nIt will expire in {OTP_TTL_MIN} minutes."
    try:
        ses_client.send_email(
            Destination={'ToAddresses': [email]},
            Message={
                'Body': {'Text': {'Charset': "UTF-8", 'Data': email_body}},
                'Subject': {'Charset': "UTF-8", 'Data': email_subject},
            },
            Source=SENDER_EMAIL,
        )
        app.logger.info(f"Sent OTP to {email}")
        return jsonify({'ok': True, 'message': f'An OTP has been sent to {email}.'})
    except ClientError as e:
        app.logger.error(f"Failed to send OTP email to {email}: {e.response['Error']['Message']}")
        return jsonify({'ok': False, 'error': 'Failed to send OTP email.'}), 502

@app.route('/auth/verify-otp', methods=['POST'])
def verify_otp():
    email = (request.json or {}).get('email', '').strip().lower()
    code = (request.json or {}).get('code', '').strip()
    with engine.connect() as conn:
        otp_data = conn.execute(text('SELECT hash, exp FROM otps WHERE email=:e ORDER BY exp DESC LIMIT 1'), {'e': email}).fetchone()
    if not otp_data: return jsonify({'ok': False, 'error': 'No OTP found'}), 400
    hashed_code, exp_str = otp_data
    if datetime.fromisoformat(exp_str).replace(tzinfo=timezone.utc) < datetime.now(timezone.utc): return jsonify({'ok': False, 'error': 'OTP has expired'}), 400
    if not bcrypt.checkpw(code.encode(), hashed_code): return jsonify({'ok': False, 'error': 'Invalid OTP'}), 400

    now = datetime.now(timezone.utc)
    access_token = signer.dumps({'sub': email, 'type': 'access', 'iat': now.isoformat()})
    refresh_jti = uuid.uuid4().hex
    refresh_token = signer.dumps({'sub': email, 'type': 'refresh', 'jti': refresh_jti, 'iat': now.isoformat()})
    refresh_exp = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_TTL_DAYS)
    with engine.begin() as conn:
        conn.execute(text('INSERT INTO refresh_tokens(jti, email, exp) VALUES (:j, :e, :x)'), {'j': refresh_jti, 'e': email, 'x': refresh_exp})

    with engine.connect() as conn:
        user = conn.execute(text('SELECT email, role, is_active FROM users WHERE email=:e'), {'e': email}).first()

    if not user or not user.is_active: return jsonify({'ok': False, 'error': 'User account is inactive'}), 403

    _emit_event("user.login", {"method": "otp"}, user_id=email)

    resp = jsonify({'ok': True, 'user': {'email': user.email, 'role': user.role}})
    _set_cookie(resp, 'access_token', access_token, 60 * ACCESS_TOKEN_TTL_MIN)
    _set_cookie(resp, 'refresh_token', refresh_token, 60 * 60 * 24 * REFRESH_TOKEN_TTL_DAYS)
    return resp

@app.route('/auth/refresh', methods=['POST'])
def refresh():
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        return jsonify({"ok": False, "error": "Missing refresh token"}), 401

    try:
        payload = signer.loads(refresh_token, max_age=60 * 60 * 24 * REFRESH_TOKEN_TTL_DAYS * 2)
        if payload.get('type') != 'refresh':
            return jsonify({"ok": False, "error": "Invalid token type"}), 401

        email = payload.get('sub')
        jti = payload.get('jti')

        with engine.connect() as conn:
            token_in_db = conn.execute(text('SELECT 1 FROM refresh_tokens WHERE jti=:jti'), {'jti': jti}).first()

        if not token_in_db:
            return jsonify({"ok": False, "error": "Token has been revoked"}), 401

        now = datetime.now(timezone.utc)
        access_token = signer.dumps({'sub': email, 'type': 'access', 'iat': now.isoformat()})
        resp = jsonify({'ok': True})
        _set_cookie(resp, 'access_token', access_token, 60 * ACCESS_TOKEN_TTL_MIN)
        return resp

    except (BadSignature, TypeError, KeyError):
        return jsonify({"ok": False, "error": "Invalid or expired refresh token"}), 401

@app.route('/auth/logout', methods=['POST'])
def logout():
    refresh_token = request.cookies.get('refresh_token')
    if refresh_token:
        try:
            payload = signer.loads(refresh_token, max_age=60 * 60 * 24 * REFRESH_TOKEN_TTL_DAYS * 2)
            jti = payload.get('jti')
            if jti:
                with engine.begin() as conn:
                    conn.execute(text('DELETE FROM refresh_tokens WHERE jti=:jti'), {'jti': jti})
        except (BadSignature, TypeError, KeyError):
            # If the token is bad, we can't look up the JTI, but we can still clear the cookies.
            pass

    resp = jsonify({'ok': True, 'message': 'Logged out successfully'})
    resp.set_cookie('access_token', '', expires=0, httponly=True, samesite='Lax')
    resp.set_cookie('refresh_token', '', expires=0, httponly=True, samesite='Lax')
    return resp

@app.route('/auth/user', methods=['GET'])
@require_auth()
def get_user():
    user = request.current_user
    return jsonify({'ok': True, 'user': {'email': user.email, 'role': user.role, 'is_active': user.is_active}})

# --- Admin Endpoints ---
@app.route('/admin/users/<string:user_email>', methods=['PATCH'])
@require_auth(role='admin')
def update_user(user_email):
    data = request.get_json()
    if not data: return jsonify({"error": "No data provided"}), 400

    new_role = data.get('role')
    is_active = data.get('is_active')

    with engine.begin() as conn:
        user = conn.execute(text("SELECT email FROM users WHERE email=:email"), {"email": user_email}).first()
        if not user: return jsonify({"error": "User not found"}), 404

        if new_role:
            conn.execute(text("UPDATE users SET role=:role WHERE email=:email"), {"role": new_role, "email": user_email})
        if is_active is not None:
            conn.execute(text("UPDATE users SET is_active=:is_active WHERE email=:email"), {"is_active": bool(is_active), "email": user_email})

    return jsonify({"ok": True, "message": f"User {user_email} updated successfully."})

# --- Gateway Endpoint ---
@app.route('/gateway/routes', methods=['GET'])
def get_gateway_routes():
    """
    Provides a service discovery map for all backend engines.
    URLs are sourced from environment variables with sensible localhost defaults.
    """
    routes = {
        "eng-identity": os.getenv('ENG_IDENTITY_URL', 'http://localhost:5000'),
        "eng-drafting": os.getenv('ENG_DRAFTING_URL', 'http://localhost:5001'),
        "eng-vault": os.getenv('ENG_VAULT_URL', 'http://localhost:5002'),
        "eng-billing": os.getenv('ENG_BILLING_URL', 'http://localhost:5003'),
        "eng-compliance": os.getenv('ENG_COMPLIANCE_URL', 'http://localhost:5004'),
        "eng-lifecycle": os.getenv('ENG_LIFECYCLE_URL', 'http://localhost:5005'),
        "eng-engagement": os.getenv('ENG_ENGAGEMENT_URL', 'http://localhost:5006'),
        "eng-analytics": os.getenv('ENG_ANALYTICS_URL', 'http://localhost:5007'),
        # E8 eng-vault is listed again as it was in the original file, mapping to port 5002.
        # This might be an error in the original file, but we keep it for consistency.
        # A better approach would be to have a single source of truth for service names and ports.
        # For now, we will map eng-vault to 5002 as per the original file.
    }
    # The original file had a duplicate eng-vault mapping. The logic above handles it.
    # The spec mentions 8 engines, and we have 8 here.
    # E1: identity, E2: drafting, E3: billing, E4: compliance, E5: lifecycle, E6: engagement, E7: analytics, E8: vault
    # The list is complete.

    # Let's ensure eng-vault is correctly mapped as per the provided file structure.
    # It appears I have mapped all services correctly.
    # The original placeholder had eng-vault on 5002, which I have kept.

    # Final check of the list of engines from the refactor document:
    # E1: eng-identity
    # E2: eng-drafting
    # E3: eng-billing
    # E4: eng-compliance
    # E5: eng-lifecycle
    # E6: eng-engagement
    # E7: eng-analytics
    # E8: eng-vault
    # All 8 are present.

    return jsonify(routes), 200

# --- Pydantic models for System Email ---
from pydantic import BaseModel, ValidationError as PydanticValidationError

class SystemEmailBody(BaseModel):
    recipient: str
    subject: str
    body_text: str

# --- API Key Decorator (re-used from eng-lifecycle) ---
def require_api_key(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        # Ensure INTERNAL_SERVICE_API_KEY is loaded from .env
        if not api_key or api_key != os.getenv('INTERNAL_SERVICE_API_KEY'):
            return jsonify({'ok': False, 'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/v1/send-system-email', methods=['POST'])
@require_api_key
def send_system_email():
    try:
        body = SystemEmailBody(**request.get_json(force=True))
    except PydanticValidationError as e:
        return jsonify({'ok': False, 'error': e.errors()}), 400

    try:
        ses_client.send_email(
            Destination={'ToAddresses': [body.recipient]},
            Message={
                'Body': {'Text': {'Charset': "UTF-8", 'Data': body.body_text}},
                'Subject': {'Charset': "UTF-8", 'Data': body.subject},
            },
            Source=SENDER_EMAIL,
        )
        app.logger.info(f"Sent system email to {body.recipient} with subject: {body.subject}")
        return jsonify({'ok': True, 'message': 'Email sent successfully.'})
    except ClientError as e:
        app.logger.error(f"Failed to send system email to {body.recipient}: {e.response['Error']['Message']}")
        return jsonify({'ok': False, 'error': 'Failed to send system email.'}), 502

# --- Pydantic models for Client Token Request ---
class ClientTokenRequestBody(BaseModel):
    client_name: str
    client_email: str
    reason: str

@app.route('/api/v1/advisor/request-client-token', methods=['POST'])
@require_auth(role='advisor')
def request_client_token():
    try:
        body = ClientTokenRequestBody(**request.get_json(force=True))
    except PydanticValidationError as e:
        return jsonify({'ok': False, 'error': e.errors()}), 400

    advisor_email = request.current_user.email
    client_email = body.client_email.strip().lower()

    # Generate a unique, short-lived token for the client
    client_token = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    # Let's make the client token valid for 7 days
    expires_at = now + timedelta(days=7)

    try:
        with engine.begin() as conn:
            # Create a user for the client if they don't exist
            user_exists = conn.execute(text('SELECT 1 FROM users WHERE email=:e'), {'e': client_email}).first()
            if not user_exists:
                conn.execute(text('INSERT INTO users(email, role, created_at) VALUES (:e, :r, :t)'), {'e': client_email, 'r': 'client', 't': now})
                _emit_event("user.created", {"source": "advisor_invitation", "advisor": advisor_email}, user_id=client_email)

            # Store the client token
            conn.execute(
                text('INSERT INTO client_tokens (token, client_email, advisor_email, reason, created_at, exp) VALUES (:t, :ce, :ae, :r, :c, :e)'),
                {
                    't': client_token,
                    'ce': client_email,
                    'ae': advisor_email,
                    'r': body.reason,
                    'c': now,
                    'e': expires_at
                }
            )

        # Send the token to the client via email
        email_subject = f"You have been invited to AssetArc by {advisor_email}"
        email_body = f"Hello {body.client_name},\\n\\nAn advisor has invited you to begin your structuring journey with AssetArc.\\n\\nPlease use the following token to access the platform: {client_token}\\n\\nThis token will expire in 7 days."

        ses_client.send_email(
            Destination={'ToAddresses': [client_email]},
            Message={
                'Body': {'Text': {'Charset': "UTF-8", 'Data': email_body}},
                'Subject': {'Charset': "UTF-8", 'Data': email_subject},
            },
            Source=SENDER_EMAIL,
        )

        _emit_event("client.token.requested", {"advisor": advisor_email}, user_id=client_email)

        return jsonify({'ok': True, 'message': f'An invitation token has been sent to {client_email}.'})

    except ClientError as e:
        app.logger.error(f"Failed to send client token email to {client_email}: {e.response['Error']['Message']}")
        return jsonify({'ok': False, 'error': 'Failed to send invitation email.'}), 502
    except Exception as e:
        app.logger.error(f"An unexpected error occurred during client token request: {e}")
        return jsonify({'ok': False, 'error': 'An unexpected error occurred.'}), 500

@app.route('/api/v1/advisor/dashboard', methods=['GET'])
@require_auth(role='advisor')
def get_advisor_dashboard():
    advisor_email = request.current_user.email

    # --- Data Aggregation from other services ---
    clients = []
    stats = {
        "active_clients": 0,
        "pending_reviews": 0,
        "tokens_remaining": 0
    }

    headers = {'x-api-key': os.getenv('INTERNAL_SERVICE_API_KEY')}

    try:
        # 1. Get client list from eng-lifecycle
        lifecycle_url = os.getenv('ENG_LIFECYCLE_URL', 'http://localhost:5005')
        lifecycle_resp = requests.get(
            f"{lifecycle_url}/api/v1/clients?advisor_email={advisor_email}",
            headers=headers,
            timeout=10
        )
        if lifecycle_resp.status_code == 200:
            clients = lifecycle_resp.json().get('clients', [])
            stats['active_clients'] = len(clients)
            stats['pending_reviews'] = sum(1 for c in clients if c.get('status') == 'Pending Review')

        # 2. Get token balance from eng-billing
        billing_url = os.getenv('ENG_BILLING_URL', 'http://localhost:5003')
        billing_resp = requests.get(
            f"{billing_url}/api/v1/tokens/balance?advisor_email={advisor_email}",
            headers=headers,
            timeout=10
        )
        if billing_resp.status_code == 200:
            stats['tokens_remaining'] = billing_resp.json().get('balance', 0)

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Failed to fetch advisor dashboard data: {e}")
        # Return what we have, or an error if nothing is available
        if not clients:
            return jsonify({"ok": False, "error": "Could not retrieve advisor data from backend services."}), 503

    dashboard_data = {
        "stats": stats,
        "clients": clients
    }

    return jsonify({"ok": True, "dashboard_data": dashboard_data})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
