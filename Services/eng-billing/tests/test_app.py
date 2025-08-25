import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import json
import fakeredis
from datetime import datetime, UTC, timedelta
import hmac
import hashlib
import base64
from sqlalchemy import create_engine, text

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from app import app
from common.secrets import get_secret

class PriceLockTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.fake_redis_client = fakeredis.FakeStrictRedis(decode_responses=True)
        self.redis_patcher = patch('app.redis_client', self.fake_redis_client)
        self.redis_patcher.start()
        self.fake_redis_client.flushall()

    def tearDown(self):
        self.redis_patcher.stop()

    @patch('app._emit_event')
    @patch('requests.get')
    def test_create_price_lock_success(self, mock_get, mock_emit_event):
        # Set a valid auth cookie
        self.app.set_cookie('access_token', 'valid_token')

        # Mock responses for identity service and FX service
        def mock_requests_get(url, **kwargs):
            if 'auth/user' in url:
                mock_resp = MagicMock()
                mock_resp.status_code = 200
                mock_resp.json.return_value = {'ok': True, 'user': {'email': 'authed_user@example.com'}}
                return mock_resp
            elif 'api.exchangerate.host' in url:
                mock_resp = MagicMock()
                mock_resp.status_code = 200
                mock_resp.json.return_value = {'rates': {'ZAR': 18.50}}
                return mock_resp
            return MagicMock(status_code=404)
        mock_get.side_effect = mock_requests_get

        lock_data = {'amount': 100, 'base': 'USD', 'target': 'ZAR', 'product_id': 'prod_abc'}
        response = self.app.post('/pricing/lock/create', json=lock_data)

        self.assertEqual(response.status_code, 201)
        json_data = response.get_json()
        self.assertEqual(json_data['user_id'], 'authed_user@example.com')
        lock_id = json_data['lock_id']
        stored_data = json.loads(self.fake_redis_client.get(f"price_lock:{lock_id}"))
        self.assertEqual(stored_data['user_id'], 'authed_user@example.com')
        mock_emit_event.assert_called_once()
        self.assertEqual(mock_emit_event.call_args[0][0], "price.lock.created")

    def test_create_price_lock_unauthorized(self):
        response = self.app.post('/pricing/lock/create', json={'amount': 100})
        self.assertEqual(response.status_code, 401)

    @patch('requests.get')
    def test_create_price_lock_missing_amount(self, mock_get):
        self.app.set_cookie('access_token', 'valid_token')
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {'ok': True, 'user': {}})
        response = self.app.post('/pricing/lock/create', json={'product_id': 'prod_abc'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['error'], 'Missing amount')

    def test_get_price_lock_success(self):
        lock_id = 'test_lock_123'
        lock_data = {"lock_id": lock_id, "amount": 50, "rate": 1.2, "expires_at": (datetime.now(UTC)).isoformat(), "user_id": "user_xyz", "product_id": "prod_xyz"}
        self.fake_redis_client.set(f"price_lock:{lock_id}", json.dumps(lock_data))
        response = self.app.get(f'/pricing/lock/{lock_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['lock_id'], lock_id)

    def test_get_price_lock_not_found(self):
        response = self.app.get('/pricing/lock/non_existent_lock')
        self.assertEqual(response.status_code, 404)

class YocoIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.db_patcher = patch('app.engine', create_engine('sqlite:///:memory:'))
        self.engine = self.db_patcher.start()
        from app import init_db
        with app.app_context():
            init_db()

    def tearDown(self):
        self.db_patcher.stop()

    @patch('requests.post')
    def test_create_checkout_session_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "ch_12345", "redirectUrl": "https://pay.yoco.com/checkout_12345"}
        mock_post.return_value = mock_response
        response = self.app.post('/checkout/session', json={'amount': 15000, 'currency': 'ZAR', 'user_id': 'test@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['payment_url'], "https://pay.yoco.com/checkout_12345")
        mock_post.assert_called_once()

    def test_create_checkout_session_missing_data(self):
        response = self.app.post('/checkout/session', json={'amount': 15000}) # Missing user_id
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing \'user_id\'', response.get_json()['error'])

    def test_yoco_webhook_invalid_signature(self):
        headers = {'webhook-id': 'wh_test_123', 'webhook-timestamp': str(int(datetime.now(UTC).timestamp())), 'webhook-signature': 'v1,invalid_signature'}
        response = self.app.post('/webhooks/yoco', headers=headers, json={'type': 'payment.succeeded'})
        self.assertEqual(response.status_code, 403)

    def test_yoco_webhook_old_timestamp(self):
        old_timestamp = int((datetime.now(UTC) - timedelta(minutes=5)).timestamp())
        headers = {'webhook-id': 'wh_test_123', 'webhook-timestamp': str(old_timestamp), 'webhook-signature': 'v1,some_signature'}
        response = self.app.post('/webhooks/yoco', headers=headers, json={'type': 'payment.succeeded'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Timestamp too old', response.get_data(as_text=True))

    def test_yoco_webhook_success_and_token_grant(self):
        webhook_id = 'wh_test_success'
        timestamp = str(int(datetime.now(UTC).timestamp()))
        payload_dict = {"type": "payment.succeeded", "payload": {"id": "pay_test_12345", "amount": 25000, "currency": "ZAR", "metadata": {"checkoutId": "ch_test_abcde", "user_id": "new_user@example.com"}}}
        request_body = json.dumps(payload_dict)
        signed_content = f"{webhook_id}.{timestamp}.{request_body}"
        secret = get_secret('yoco_webhook_secret')
        secret_bytes = base64.b64decode(secret.split('_')[1])
        hmac_signature = hmac.new(secret_bytes, signed_content.encode('utf-8'), hashlib.sha256).digest()
        expected_signature = base64.b64encode(hmac_signature).decode()
        headers = {'webhook-id': webhook_id, 'webhook-timestamp': timestamp, 'webhook-signature': f"v1,{expected_signature}"}

        response = self.app.post('/webhooks/yoco', headers=headers, data=request_body, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        with self.engine.connect() as conn:
            trans = conn.execute(text("SELECT * FROM transactions WHERE id = 'pay_test_12345'")).first()
            self.assertIsNotNone(trans)
            self.assertEqual(trans.user_id, 'new_user@example.com')
            tokens = conn.execute(text("SELECT token_balance FROM advisor_tokens WHERE advisor_email = 'new_user@example.com'")).scalar_one()
            self.assertEqual(tokens, 100)

        response2 = self.app.post('/webhooks/yoco', headers=headers, data=request_body, content_type='application/json')
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.get_json()['reason'], 'already_processed')

        with self.engine.connect() as conn:
            tokens2 = conn.execute(text("SELECT token_balance FROM advisor_tokens WHERE advisor_email = 'new_user@example.com'")).scalar_one()
            self.assertEqual(tokens2, 100)

    def test_get_metrics_success(self):
        # 1. Seed the database with sample transactions
        with self.engine.connect() as conn:
            # The .begin() method is not needed for individual inserts if using a connection
            # but we need to commit if the engine is not in autocommit mode.
            # For simplicity in testing, we can often rely on the test framework's transaction management,
            # but explicit is better than implicit.
            conn.execute(text("""
                INSERT INTO transactions (id, user_id, yoco_checkout_id, amount_total, currency, product_description, transaction_status, created_at)
                VALUES
                    ('pay_1', 'user1', 'co_1', 10000, 'ZAR', 'p1', 'completed', '2023-01-01 10:00:00'),
                    ('pay_2', 'user2', 'co_2', 15000, 'ZAR', 'p2', 'completed', '2023-01-01 11:00:00'),
                    ('pay_3', 'user1', 'co_3', 5000, 'ZAR', 'p3', 'failed', '2023-01-01 12:00:00')
            """))
            conn.commit()

        # 2. Make request with valid API key
        api_key = get_secret('internal-service-api-key')
        headers = {'x-api-key': api_key}
        response = self.app.get('/api/v1/metrics', headers=headers)

        # 3. Assert the response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['ok'])
        metrics = data['metrics']
        # 10000 + 15000 = 25000 cents -> 250.00
        self.assertEqual(metrics['total_revenue'], 250.0)
        self.assertEqual(metrics['total_transactions'], 2)

    def test_get_metrics_unauthorized(self):
        response = self.app.get('/api/v1/metrics') # No API key
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
