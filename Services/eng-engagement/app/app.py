import os
import sys
import sys
import boto3
import requests
import uuid
from flask import Flask, jsonify, request
from pydantic import BaseModel, ValidationError
from botocore.exceptions import ClientError
from auth_decorator import require_auth_from_identity

app = Flask(__name__)

# --- Add common module to path ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'common')))
from secrets import get_secret

# --- Configuration ---
DRAFTING_SERVICE_URL = get_secret('drafting-service-url') or 'http://localhost:5001'
BILLING_SERVICE_URL = get_secret('billing-service-url') or 'http://localhost:5003'
CAL_COM_BASE_URL = get_secret('cal-com-base-url') or 'https://api.cal.com/v2'
CAL_COM_API_KEY = get_secret('cal-com-api-key') # Required
AWS_REGION = get_secret('aws-region') or 'us-east-1'
SENDER_EMAIL = get_secret('sender-email') or 'noreply@assetarc.com'
ANALYTICS_SERVICE_URL = get_secret('eng-analytics-url') or 'http://localhost:5007'


# Initialize Boto3 client for SES
ses_client = boto3.client('ses', region_name=AWS_REGION)

# --- Models for Request Validation ---
class SequenceBody(BaseModel):
    sequence_id: str
    context: dict

class EmailBody(BaseModel):
    template_id: str
    to: str
    data: dict
    subject: str

class BookingBody(BaseModel):
    name: str
    email: str
    event_type_id: int
    price_lock: str | None = None
    when: str | None = None # This field is not used for link generation but kept for compatibility

# --- Service Endpoints ---
@app.route('/')
def index():
    return jsonify({"service": "eng-engagement", "status": "running"})

@app.route('/engage/sequence/start', methods=['POST'])
def start_sequence():
    try:
        body = SequenceBody(**request.get_json(force=True))
    except ValidationError as e:
        return jsonify({'ok': False, 'error': e.errors()}), 400

    # In a real application, this would trigger a workflow in a system
    # like AWS Step Functions, Celery, or a simple message queue.
    # For now, we'll just log the request to demonstrate it's been received.
    app.logger.info(f"Received request to start sequence '{body.sequence_id}' with context: {body.context}")

    return jsonify({
        "ok": True,
        "message": f"Sequence '{body.sequence_id}' has been initiated.",
        "sequence_instance_id": str(uuid.uuid4()) # Return a dummy instance ID
    }), 202

def _send_email_logic(body: EmailBody):
    """Core logic to render a template and send an email."""
    # 1. Call eng-drafting to render the email's HTML body
    drafting_payload = {"template_id": body.template_id, "data": body.data}
    drafting_response = requests.post(f"{DRAFTING_SERVICE_URL}/doc/render", json=drafting_payload, timeout=30)
    drafting_response.raise_for_status()

    email_html = drafting_response.text

    # 2. Send the email using AWS SES
    ses_response = ses_client.send_email(
        Destination={'ToAddresses': [body.to]},
        Message={
            'Body': {
                'Html': {'Charset': "UTF-8", 'Data': email_html},
                'Text': {'Charset': "UTF-8", 'Data': "This is a fallback text body for the email."}
            },
            'Subject': {'Charset': "UTF-8", 'Data': body.subject},
        },
        Source=SENDER_EMAIL,
    )

    return ses_response.get('MessageId')

@app.route('/engage/email/send', methods=['POST'])
def send_email():
    try:
        body = EmailBody(**request.get_json(force=True))
    except ValidationError as e:
        return jsonify({'ok': False, 'error': e.errors()}), 400

    try:
        message_id = _send_email_logic(body)
        app.logger.info(f"Email sent to {body.to}. Message ID: {message_id}")
        return jsonify({"ok": True, "message_id": message_id})

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Failed to call drafting service: {e}")
        return jsonify({"ok": False, "error": "Failed to render email template."}), 502
    except ClientError as e:
        app.logger.error(f"Failed to send email via SES: {e.response['Error']['Message']}")
        return jsonify({"ok": False, "error": "Failed to send email."}), 502
    except Exception as e:
        app.logger.error(f"An unexpected error occurred in send_email: {e}")
        return jsonify({"ok": False, "error": "An unexpected error occurred."}), 500

def _emit_event(event_type: str, payload: dict):
    """Helper to send an event to the analytics service."""
    try:
        user_id = request.current_user.get('email') if hasattr(request, 'current_user') else None
        event = {
            "event_type": event_type,
            "payload": payload,
            "service": "eng-engagement",
            "user_id": user_id
        }
        requests.post(f"{ANALYTICS_SERVICE_URL}/events/ingest", json=event, timeout=2)
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Failed to emit event {event_type}: {e}")

def _send_booking_error_email(recipient_email: str, error_reason: str):
    """Helper function to send a booking error email."""
    try:
        email_subject = "Action Required: Issue with Your Booking Attempt"
        email_data = {
            "error_reason": error_reason,
            "next_step": "Please try to secure a new price lock and attempt the booking again.",
            "support_contact": "support@assetarc.com"
        }
        email_body = EmailBody(
            template_id="booking_error.v1",
            to=recipient_email,
            data=email_data,
            subject=email_subject
        )
        _send_email_logic(email_body)
        app.logger.info(f"Sent booking error email to {recipient_email}")
    except Exception as e:
        # Log the error, but don't let it fail the parent request
        app.logger.error(f"Failed to send booking error email: {e}")

@app.route('/engage/booking/slot', methods=['POST'])
@require_auth_from_identity()
def book_slot():
    """
    Validates a price lock and returns a unique Cal.com booking link.
    Requires authentication.
    """
    if not CAL_COM_API_KEY:
        app.logger.error("CAL_COM_API_KEY is not set.")
        return jsonify({"ok": False, "error": "Booking system is not configured."}), 500

    try:
        body = BookingBody(**request.get_json(force=True))
    except ValidationError as e:
        return jsonify({'ok': False, 'error': e.errors()}), 400

    # 1. If a price_lock is provided, validate it with the billing service
    if body.price_lock:
        try:
            billing_response = requests.get(f"{BILLING_SERVICE_URL}/pricing/lock/{body.price_lock}", timeout=10)
            if billing_response.status_code != 200:
                error_message = "Your price lock is invalid or has expired."
                _send_booking_error_email(body.email, error_message)
                return jsonify({"ok": False, "error": error_message}), 400

        except requests.exceptions.RequestException as e:
            app.logger.error(f"Failed to call billing service: {e}")
            return jsonify({"ok": False, "error": "Failed to validate price lock."}), 502

    # 2. Create a unique booking link using Cal.com API
    try:
        headers = {
            'Authorization': f'Bearer {CAL_COM_API_KEY}',
            'Content-Type': 'application/json'
        }
        # The Cal.com API for private links doesn't seem to take a payload,
        # but we can pass info via query params on the resulting URL.
        cal_response = requests.post(
            f"{CAL_COM_BASE_URL}/event-types/{body.event_type_id}/private-links",
            headers=headers,
            timeout=15
        )
        cal_response.raise_for_status()

        cal_data = cal_response.json()
        booking_url = cal_data.get("url")

        if not booking_url:
            app.logger.error("Cal.com response did not include a booking URL.")
            return jsonify({"ok": False, "error": "Failed to create booking link."}), 502

        # 3. Add user info and price_lock as query parameters
        from urllib.parse import urlencode, urlparse, urlunparse, parse_qs

        # Pre-fill user info
        params = {
            'name': body.name,
            'email': body.email,
        }
        # Pass price_lock for tracking on the booking page or in webhooks
        if body.price_lock:
            params['price_lock_id'] = body.price_lock

        # Append params to the booking URL
        url_parts = list(urlparse(booking_url))
        query = dict(parse_qs(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query)
        final_url = urlunparse(url_parts)

        # 4. Send confirmation email and emit event
        _send_booking_confirmation_email(
            recipient_email=body.email,
            name=body.name,
            booking_url=final_url
        )

        _emit_event("booking.link.created", {
            "event_type_id": body.event_type_id,
            "price_lock_used": bool(body.price_lock)
        })

        return jsonify({"ok": True, "booking_url": final_url})

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Failed to call Cal.com service: {e}")
        return jsonify({"ok": False, "error": "Failed to create booking link."}), 502
    except Exception as e:
        app.logger.error(f"An unexpected error occurred in book_slot: {e}")
        return jsonify({"ok": False, "error": "An unexpected error occurred."}), 500

def _send_booking_confirmation_email(recipient_email: str, name: str, booking_url: str):
    """Helper function to send a booking confirmation email."""
    try:
        email_subject = "Your Booking Confirmation"
        email_data = {
            "name": name,
            "booking_url": booking_url,
        }
        email_body = EmailBody(
            template_id="booking_confirmation.v1",
            to=recipient_email,
            data=email_data,
            subject=email_subject
        )
        _send_email_logic(email_body)
        app.logger.info(f"Queued booking confirmation email to {recipient_email}")
    except Exception as e:
        # Log the error, but don't let it fail the parent request
        app.logger.error(f"Failed to send booking confirmation email: {e}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5006)
