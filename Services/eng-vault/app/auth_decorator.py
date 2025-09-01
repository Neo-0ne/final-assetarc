import os
import sys
import functools
from flask import request, jsonify
import requests

# --- common module is now loaded via PYTHONPATH ---
from common.secrets import get_secret

IDENTITY_SERVICE_URL = get_secret('eng-identity-url') or 'http://localhost:5000'

def require_auth_from_identity(role=None):
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.cookies.get('access_token')
            if not token:
                return jsonify({"ok": False, "error": "Authentication token required"}), 401

            try:
                # Call the identity service to validate the token
                headers = {'Cookie': f'access_token={token}'}
                user_response = requests.get(f"{IDENTITY_SERVICE_URL}/auth/user", headers=headers, timeout=5)

                if user_response.status_code != 200:
                    return jsonify({"ok": False, "error": "Invalid or expired token"}), 401

                user_data = user_response.json().get('user', {})

                if role and user_data.get('role') != role:
                    return jsonify({"ok": False, "error": "Forbidden"}), 403

                # Attach user to the request for use in the endpoint
                request.current_user = user_data

            except requests.exceptions.RequestException:
                return jsonify({"ok": False, "error": "Could not connect to identity service"}), 503

            return f(*args, **kwargs)
        return decorated_function
    return decorator
