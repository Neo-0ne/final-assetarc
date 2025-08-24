import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import bcrypt
from datetime import datetime, timedelta, timezone

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from app import app, signer

# Use a mock engine for all tests
mock_engine = MagicMock()

@patch('app.engine', mock_engine)
class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = self.mock_conn
        mock_engine.begin.return_value.__enter__.return_value = self.mock_conn
        self.mock_conn.execute.reset_mock()

    @patch('app.ses_client')
    @patch('app._emit_event')
    def test_request_otp_success_new_user(self, mock_emit, mock_ses):
        self.mock_conn.execute.return_value.first.return_value = None
        response = self.app.post('/auth/request-otp', json={'email': 'test@example.com'})
        self.assertEqual(response.status_code, 200)
        mock_ses.send_email.assert_called_once()

        # Check that the user.created event was emitted
        mock_emit.assert_called_once_with("user.created", {"source": "otp_request"}, user_id='test@example.com')

    @patch('app._emit_event')
    def test_verify_otp_success(self, mock_emit):
        email = 'test@example.com'
        code = '123456'
        hashed_code = bcrypt.hashpw(code.encode(), bcrypt.gensalt())
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

        mock_user = MagicMock()
        mock_user.is_active = True
        mock_user.email = email
        mock_user.role = 'client'

        self.mock_conn.execute.side_effect = [
            MagicMock(fetchone=MagicMock(return_value=(hashed_code, expires_at.isoformat()))),
            MagicMock(), # For the INSERT refresh token
            MagicMock(first=MagicMock(return_value=mock_user))
        ]

        response = self.app.post('/auth/verify-otp', json={'email': email, 'code': code})

        self.assertEqual(response.status_code, 200)
        cookies = response.headers.getlist('Set-Cookie')
        self.assertTrue(any('access_token=' in c for c in cookies))
        self.assertTrue(any('refresh_token=' in c for c in cookies))

        # Check that the user.login event was emitted
        mock_emit.assert_called_once_with("user.login", {"method": "otp"}, user_id=email)

    def test_verify_otp_invalid_code(self):
        email = 'test@example.com'
        code = 'wrongcode'
        hashed_code = bcrypt.hashpw('correctcode'.encode(), bcrypt.gensalt())
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
        self.mock_conn.execute.return_value.fetchone.return_value = (hashed_code, expires_at.isoformat())
        response = self.app.post('/auth/verify-otp', json={'email': email, 'code': code})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['error'], 'Invalid OTP')

    def test_logout(self):
        refresh_token = signer.dumps({'sub': 'test@example.com', 'type': 'refresh', 'jti': 'some-jti'})
        self.app.set_cookie('refresh_token', refresh_token)
        response = self.app.post('/auth/logout')
        self.assertEqual(response.status_code, 200)

        executed_sql = str(self.mock_conn.execute.call_args[0][0])
        self.assertIn("DELETE FROM refresh_tokens", executed_sql)

        cookies = response.headers.getlist('Set-Cookie')
        self.assertTrue(any('access_token=;' in c and 'Expires' in c for c in cookies) or any('access_token="";' in c and 'Expires' in c for c in cookies))
        self.assertTrue(any('refresh_token=;' in c and 'Expires' in c for c in cookies) or any('refresh_token="";' in c and 'Expires' in c for c in cookies))

    def test_refresh_success(self):
        email = 'test@example.com'
        jti = 'some-valid-jti'
        refresh_token = signer.dumps({'sub': email, 'type': 'refresh', 'jti': jti})
        self.app.set_cookie('refresh_token', refresh_token)

        self.mock_conn.execute.return_value.first.return_value = (1,)
        response = self.app.post('/auth/refresh')

        self.assertEqual(response.status_code, 200)
        cookies = response.headers.getlist('Set-Cookie')
        self.assertTrue(any('access_token=' in c for c in cookies))
        self.assertFalse(any('refresh_token=' in c for c in cookies))

    def test_refresh_revoked_token(self):
        refresh_token = signer.dumps({'sub': 'test@example.com', 'type': 'refresh', 'jti': 'revoked-jti'})
        self.app.set_cookie('refresh_token', refresh_token)
        self.mock_conn.execute.return_value.first.return_value = None
        response = self.app.post('/auth/refresh')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()['error'], 'Token has been revoked')

    def test_require_auth_success(self):
        email = 'test@example.com'
        access_token = signer.dumps({'sub': email, 'type': 'access'})
        self.app.set_cookie('access_token', access_token)

        mock_user = MagicMock()
        mock_user.is_active = True
        mock_user.email = email
        mock_user.role = 'client'
        self.mock_conn.execute.return_value.first.return_value = mock_user

        response = self.app.get('/auth/user')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['user']['email'], email)

    def test_require_auth_failure_bad_token(self):
        self.app.set_cookie('access_token', 'invalid-token')
        response = self.app.get('/auth/user')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()['error'], 'Authentication required')

if __name__ == '__main__':
    unittest.main()
