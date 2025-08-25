import os
import sys
import requests
import uuid
import redis
import json
import hmac
import hashlib
import base64
from flask import Flask, jsonify, request, redirect
from functools import lru_cache
from datetime import datetime, timedelta, UTC
from auth_decorator import require_auth_from_identity

app = Flask(__name__)

# --- common module is now loaded via PYTHONPATH ---
from common.secrets import get_secret

# --- Configuration ---
YOCO_SECRET_KEY = get_secret('yoco_secret_key')
YOCO_WEBHOOK_SECRET = get_secret('yoco_webhook_secret')
REDIS_URL = get_secret('redis-url') or 'redis://localhost:6379/0'
ANALYTICS_SERVICE_URL = get_secret('eng-analytics-url') or 'http://localhost:5007'

from sqlalchemy import create_engine, text

# --- Database Setup ---
DB_URI = get_secret('sqlalchemy-database-uri') or 'sqlite:///eng_billing.db'
engine = create_engine(DB_URI, future=True)

def init_db():
    with engine.begin() as conn:
        # Table for advisor token balances
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS advisor_tokens (
                advisor_email TEXT PRIMARY KEY,
                token_balance INTEGER NOT NULL DEFAULT 0,
                updated_at DATETIME NOT NULL
            )
        """))
        # Table for financial transactions
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS transactions (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                yoco_checkout_id TEXT NOT NULL,
                amount_total INTEGER NOT NULL,
                currency TEXT NOT NULL,
                product_description TEXT,
                transaction_status TEXT NOT NULL,
                created_at DATETIME NOT NULL
            )
        """))

@app.before_request
def setup_db():
    if not hasattr(app, 'db_initialized'):
        init_db()
        app.db_initialized = True

# Initialize Redis client
try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
    app.logger.info("Successfully connected to Redis.")
except redis.exceptions.ConnectionError as e:
    app.logger.error(f"Could not connect to Redis: {e}")
    # In a real app, you might want to exit or have a fallback.
    # For now, we'll let it fail on requests that need it.
    redis_client = None

# --- FX Rate Logic (migrated from P03-fx) ---
@lru_cache(maxsize=128)
def get_rate(base, target, ttl_hash):
    del ttl_hash
    url = f'https://api.exchangerate.host/latest?base={base}&symbols={target}'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data.get('rates') or target.upper() not in data['rates']:
            raise ValueError('Rate not found in API response')
        return data['rates'][target.upper()]
    except Exception as e:
        app.logger.error(f"An error occurred while fetching FX rate: {e}")
        raise ValueError(f"Could not fetch FX rate: {e}")

def get_ttl_hash(seconds=600):
    return round(datetime.now(UTC).timestamp() / seconds)

def _emit_event(event_type: str, payload: dict):
    """Helper to send an event to the analytics service."""
    try:
        user_id = request.current_user.get('email') if hasattr(request, 'current_user') else None
        event = {
            "event_type": event_type,
            "payload": payload,
            "service": "eng-billing",
            "user_id": user_id
        }
        requests.post(f"{ANALYTICS_SERVICE_URL}/events/ingest", json=event, timeout=2)
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Failed to emit event {event_type}: {e}")

# --- Service Endpoints ---
@app.route('/')
def index():
    return jsonify({"service": "eng-billing", "status": "running"})

@app.route('/pricing/quote', methods=['POST'])
def get_quote():
    data = request.get_json() or {}
    base = data.get('base', 'USD').upper()
    target = data.get('target', 'ZAR').upper()
    amount = data.get('amount')
    if amount is None: return jsonify({"error": "Missing amount"}), 400
    try:
        rate = get_rate(base, target, ttl_hash=get_ttl_hash())
        return jsonify({"base": base, "target": target, "amount": amount, "rate": rate, "converted_amount": amount * rate})
    except ValueError as e:
        return jsonify({'ok': False, 'error': str(e)}), 502

@app.route('/checkout/session', methods=['POST'])
def create_checkout_session():
    data = request.get_json() or {}
    amount = data.get('amount') # amount in cents
    currency = data.get('currency', 'ZAR')
    user_id = data.get('user_id') # The user making the purchase

    if not amount:
        return jsonify({"error": "Missing 'amount' for checkout"}), 400
    if not user_id:
        return jsonify({"error": "Missing 'user_id' for checkout"}), 400

    headers = {
        "Authorization": f"Bearer {YOCO_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "amount": amount,
        "currency": currency,
        "metadata": {
            "user_id": user_id
        },
        # Per docs, these URLs are for redirect, not for fulfillment logic
        "successUrl": request.url_root + 'success',
        "cancelUrl": request.url_root + 'cancel'
    }

    try:
        response = requests.post('https://payments.yoco.com/api/checkouts', headers=headers, json=payload, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes
        yoco_checkout_data = response.json()

        # The URL to redirect the user to
        redirect_url = yoco_checkout_data.get('redirectUrl')

        if not redirect_url:
            app.logger.error("Yoco checkout response did not contain a redirectUrl")
            return jsonify({"error": "Failed to create checkout session"}), 500

        return jsonify({"payment_url": redirect_url})
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Yoco checkout session creation failed: {e}")
        return jsonify({'error': str(e)}), 502 # 502 Bad Gateway, as we failed to talk to an upstream service


@app.route('/webhooks/yoco', methods=['POST'])
def handle_yoco_webhook():
    # 1. Get headers and raw body
    headers = request.headers
    request_body_bytes = request.get_data()
    request_body = request_body_bytes.decode('utf-8')

    # 2. Check timestamp for replay attacks
    timestamp_str = headers.get('webhook-timestamp')
    if not timestamp_str:
        app.logger.warning("Yoco webhook missing timestamp.")
        return 'Missing webhook-timestamp header', 400
    try:
        event_timestamp = datetime.fromtimestamp(int(timestamp_str), tz=UTC)
        if datetime.now(UTC) - event_timestamp > timedelta(minutes=3):
            app.logger.warning("Received Yoco webhook with old timestamp. Ignoring.")
            return 'Timestamp too old', 400
    except (ValueError, TypeError):
        return 'Invalid timestamp format', 400

    # 3. Construct the signed content
    webhook_id = headers.get('webhook-id')
    if not webhook_id:
        app.logger.warning("Yoco webhook missing id.")
        return 'Missing webhook-id header', 400

    signed_content = f"{webhook_id}.{timestamp_str}.{request_body}"

    # 4. Determine the expected signature
    secret_bytes = base64.b64decode(YOCO_WEBHOOK_SECRET.split('_')[1])
    hmac_signature = hmac.new(secret_bytes, signed_content.encode('utf-8'), hashlib.sha256).digest()
    expected_signature = base64.b64encode(hmac_signature).decode()

    # 5. Compare signatures
    signature_header = headers.get('webhook-signature')
    if not signature_header:
        app.logger.warning("Yoco webhook missing signature.")
        return 'Missing webhook-signature header', 400

    try:
        actual_signature = signature_header.split(',')[1]
    except IndexError:
        return 'Invalid signature format', 400

    if not hmac.compare_digest(actual_signature, expected_signature):
        app.logger.error("Yoco webhook signature verification failed.")
        return 'Invalid signature', 403

    # --- Signature is valid, process the event ---
    app.logger.info(f"Yoco webhook {webhook_id} signature verified successfully.")

    event_data = json.loads(request_body)

    # Logic to record transaction and grant tokens.
    if event_data.get('type') == 'payment.succeeded':
        payment_data = event_data.get('payload', {})
        payment_id = payment_data.get('id')
        metadata = payment_data.get('metadata', {})
        user_id = metadata.get('user_id')
        checkout_id = metadata.get('checkoutId')

        if not all([payment_id, user_id, checkout_id]):
            app.logger.error(f"Yoco webhook {webhook_id} missing essential data (payment_id, user_id, or checkoutId).")
            return jsonify(status='error', reason='missing_data'), 400

        try:
            with engine.begin() as conn:
                # Idempotency check using payment ID
                result = conn.execute(
                    text("SELECT id FROM transactions WHERE id = :id"),
                    {'id': payment_id}
                ).scalar_one_or_none()

                if result:
                    app.logger.info(f"Transaction for payment {payment_id} already processed.")
                    return jsonify(status='success', reason='already_processed')

                # 1. Record the transaction
                conn.execute(text("""
                    INSERT INTO transactions (id, user_id, yoco_checkout_id, amount_total, currency, product_description, transaction_status, created_at)
                    VALUES (:id, :user_id, :yoco_checkout_id, :amount_total, :currency, :product_description, :transaction_status, :created_at)
                """), {
                    "id": payment_id,
                    "user_id": user_id,
                    "yoco_checkout_id": checkout_id,
                    "amount_total": payment_data.get('amount'),
                    "currency": payment_data.get('currency'),
                    "product_description": "Token Purchase", # Placeholder
                    "transaction_status": "completed",
                    "created_at": datetime.now(UTC)
                })
                app.logger.info(f"Recorded transaction for payment {payment_id}")

                # 2. Grant tokens
                # Using an "upsert" pattern for SQLite
                conn.execute(text("""
                    INSERT INTO advisor_tokens (advisor_email, token_balance, updated_at)
                    VALUES (:email, 100, :now)
                    ON CONFLICT(advisor_email) DO UPDATE SET
                    token_balance = token_balance + 100,
                    updated_at = :now
                """), {'email': user_id, 'now': datetime.now(UTC)})
                app.logger.info(f"Granted 100 tokens to {user_id}")

        except Exception as e:
            app.logger.error(f"Error processing payment {payment_id}: {e}")
            return jsonify(status='error', error=str(e)), 500
    else:
        app.logger.info(f"Unhandled Yoco event type {event_data.get('type')}")

    return jsonify(status='success'), 200



# Dummy success/cancel pages for Stripe redirect
@app.route('/success')
def success():
    return "<h1>Payment Successful!</h1>"

@app.route('/cancel')
def cancel():
    return "<h1>Payment Canceled.</h1>"


# --- Price Lock Endpoints ---
@app.route('/pricing/lock/create', methods=['POST'])
@require_auth_from_identity()
def create_price_lock():
    """
    Creates a price lock for a specific product or amount, including FX rates.
    The lock is stored in Redis with a 24-hour TTL. The user_id is derived
    from the authentication token.
    """
    if not redis_client:
        return jsonify({"error": "Database connection is not available."}), 503

    data = request.get_json() or {}
    base = data.get('base', 'USD').upper()
    target = data.get('target', 'ZAR').upper()
    amount = data.get('amount')
    user_id = request.current_user.get('email') # Get user from decorator
    product_id = data.get('product_id')

    if amount is None:
        return jsonify({"error": "Missing amount"}), 400

    try:
        rate = get_rate(base, target, ttl_hash=get_ttl_hash())
        lock_id = str(uuid.uuid4())
        # Expiry is handled by Redis TTL, but we store it for informational purposes.
        expires_at = datetime.now(UTC) + timedelta(hours=24)

        lock_data = {
            "lock_id": lock_id,
            "base": base,
            "target": target,
            "amount": amount,
            "rate": rate,
            "expires_at": expires_at.isoformat(),
            "user_id": user_id,
            "product_id": product_id
        }

        # Store in Redis with a 24-hour expiry (86400 seconds)
        redis_client.set(f"price_lock:{lock_id}", json.dumps(lock_data), ex=86400)

        _emit_event("price.lock.created", {
            "lock_id": lock_id,
            "product_id": product_id,
            "amount": amount,
            "currency": base
        })

        return jsonify(lock_data), 201
    except ValueError as e:
        return jsonify({'ok': False, 'error': str(e)}), 502
    except redis.exceptions.RedisError as e:
        app.logger.error(f"Redis error on price lock creation: {e}")
        return jsonify({"error": "Failed to store price lock."}), 503


@app.route('/pricing/lock/<string:lock_id>', methods=['GET'])
def get_price_lock(lock_id):
    """
    Retrieves a price lock from Redis.
    """
    if not redis_client:
        return jsonify({"error": "Database connection is not available."}), 503

    try:
        lock_data_json = redis_client.get(f"price_lock:{lock_id}")
        if not lock_data_json:
            return jsonify({"error": "Price lock not found or has expired"}), 404

        lock_data = json.loads(lock_data_json)
        return jsonify(lock_data)
    except redis.exceptions.RedisError as e:
        app.logger.error(f"Redis error on price lock retrieval: {e}")
        return jsonify({"error": "Failed to retrieve price lock."}), 503


# --- Deprecated endpoints from old services ---
# These are placeholders to show where the old logic would map.


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

@app.route('/api/v1/tokens/balance', methods=['GET'])
@require_api_key
def get_token_balance():
    advisor_email = request.args.get('advisor_email')
    if not advisor_email:
        return jsonify({'ok': False, 'error': 'advisor_email parameter is required'}), 400

    # In a real implementation, this would query the advisor_tokens table.
    # For now, return a placeholder balance.
    # We would also need an endpoint to grant/deduct tokens.

    # Let's add a dummy record for testing purposes.
    with engine.begin() as conn:
        conn.execute(
            text("INSERT OR IGNORE INTO advisor_tokens (advisor_email, token_balance, updated_at) VALUES (:email, 100, :now)"),
            {'email': advisor_email, 'now': datetime.now(UTC)}
        )
        result = conn.execute(
            text("SELECT token_balance FROM advisor_tokens WHERE advisor_email = :email"),
            {'email': advisor_email}
        ).scalar_one_or_none()

    balance = result if result is not None else 0

    return jsonify({"ok": True, "balance": balance})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
