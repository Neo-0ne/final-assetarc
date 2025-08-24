import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import json
import fakeredis
from datetime import datetime, UTC

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from app import app

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

        # Check that the user_id from the token was used
        self.assertEqual(json_data['user_id'], 'authed_user@example.com')

        # Check data in redis
        lock_id = json_data['lock_id']
        stored_data = json.loads(self.fake_redis_client.get(f"price_lock:{lock_id}"))
        self.assertEqual(stored_data['user_id'], 'authed_user@example.com')

        # Assert that the event was emitted
        mock_emit_event.assert_called_once()
        self.assertEqual(mock_emit_event.call_args[0][0], "price.lock.created")

    def test_create_price_lock_unauthorized(self):
        # No auth cookie set
        response = self.app.post('/pricing/lock/create', json={'amount': 100})
        self.assertEqual(response.status_code, 401)

    @patch('requests.get')
    def test_create_price_lock_missing_amount(self, mock_get):
        # Set a valid auth cookie
        self.app.set_cookie('access_token', 'valid_token')
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {'ok': True, 'user': {}})

        # Request is missing the 'amount' field
        response = self.app.post('/pricing/lock/create', json={'product_id': 'prod_abc'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['error'], 'Missing amount')

    def test_get_price_lock_success(self):
        lock_id = 'test_lock_123'
        lock_data = {
            "lock_id": lock_id, "amount": 50, "rate": 1.2,
            "expires_at": (datetime.now(UTC)).isoformat(),
            "user_id": "user_xyz", "product_id": "prod_xyz"
        }
        self.fake_redis_client.set(f"price_lock:{lock_id}", json.dumps(lock_data))

        response = self.app.get(f'/pricing/lock/{lock_id}')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['lock_id'], lock_id)

    def test_get_price_lock_not_found(self):
        response = self.app.get('/pricing/lock/non_existent_lock')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
