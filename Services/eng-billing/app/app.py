import os
import sys
import requests
import stripe
import uuid
import redis
import json
from flask import Flask, jsonify, request, redirect
from functools import lru_cache
from datetime import datetime, timedelta, UTC
from auth_decorator import require_auth_from_identity

app = Flask(__name__)

# --- Add common module to path ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'common')))
from secrets import get_secret

# --- Configuration ---
STRIPE_API_KEY = get_secret('stripe-api-key') or 'sk_test_YOUR_KEY'
STRIPE_WEBHOOK_SECRET = get_secret('stripe-webhook-secret') or 'whsec_YOUR_SECRET'
REDIS_URL = get_secret('redis-url') or 'redis://localhost:6379/0'
ANALYTICS_SERVICE_URL = get_secret('eng-analytics-url') or 'http://localhost:5007'
stripe.api_key = STRIPE_API_KEY

from sqlalchemy import create_engine, text

# --- Database Setup ---
DB_URI = get_secret('sqlalchemy-database-uri') or 'sqlite:///eng_billing.db'
engine = create_engine(DB_URI, future=True)

def init_db():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS advisor_tokens (
                advisor_email TEXT PRIMARY KEY,
                token_balance INTEGER NOT NULL DEFAULT 0,
                updated_at DATETIME NOT NULL
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
    line_items = data.get('items')
    if not line_items:
        return jsonify({"error": "Missing 'items' for checkout"}), 400

    try:
        # For simplicity, this example assumes the items are already formatted for Stripe.
        # A real implementation would have more robust validation and formatting.
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url=request.url_root + 'success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.url_root + 'cancel',
        )
        return jsonify({"payment_url": checkout_session.url})
    except Exception as e:
        app.logger.error(f"Stripe checkout session creation failed: {e}")
        return jsonify({'error': str(e)}), 403


@app.route('/webhooks/stripe', methods=['POST'])
def handle_stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    if not sig_header:
        return 'Missing Stripe-Signature header', 400

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig_header, secret=STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return 'Invalid signature', 400

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        app.logger.info(f"Payment successful for session: {session['id']}")
        # Here you would grant tokens or fulfill the order.
        # For example, extract user email from metadata and grant tokens:
        # user_email = session.get('metadata', {}).get('user_email')
        # if user_email:
        #     lock_db[user_email] = lock_db.get(user_email, 0) + 100 # Grant 100 tokens

    else:
        app.logger.info(f"Unhandled event type {event['type']}")

    return jsonify(status='success')



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

@app.route('/webhooks/<string:provider>', methods=['POST'])
def handle_other_webhooks(provider):
    if provider.lower() == 'stripe':
        return handle_stripe_webhook()
    return jsonify({"error": f"Provider '{provider}' not supported"}), 404


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
