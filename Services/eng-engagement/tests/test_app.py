import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from app import app

class BookingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app._emit_event')
    @patch('app._send_booking_confirmation_email')
    @patch('requests.post')
    @patch('requests.get')
    @patch('app.CAL_COM_API_KEY', 'test-api-key')
    def test_book_slot_success(self, mock_get, mock_post, mock_send_booking_confirmation_email, mock_emit_event):
        # Set a valid auth cookie
        self.app.set_cookie('access_token', 'valid_token')

        # Mock responses for identity service and billing service
        def mock_requests_get(url, **kwargs):
            if 'auth/user' in url:
                return MagicMock(status_code=200, json=lambda: {'ok': True, 'user': {}})
            elif 'pricing/lock' in url:
                return MagicMock(status_code=200)
            return MagicMock(status_code=404)
        mock_get.side_effect = mock_requests_get

        # Mock the response from the Cal.com API
        mock_cal_response = MagicMock()
        mock_cal_response.status_code = 200
        mock_cal_response.json.return_value = {'url': 'https://cal.com/booking/test-link'}
        mock_post.return_value = mock_cal_response

        mock_send_booking_confirmation_email.return_value = None # It's a fire-and-forget call

        booking_data = {
            'name': 'John Doe', 'email': 'john.doe@example.com',
            'event_type_id': 123, 'price_lock': 'lock_12345'
        }
        response = self.app.post('/engage/booking/slot', json=booking_data)

        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertTrue(json_data['ok'])
        mock_send_booking_confirmation_email.assert_called_once()

        # Assert that the event was emitted
        mock_emit_event.assert_called_once_with("booking.link.created", {
            "event_type_id": 123,
            "price_lock_used": True
        })

    def test_book_slot_unauthorized(self):
        # No auth cookie
        response = self.app.post('/engage/booking/slot', json={})
        self.assertEqual(response.status_code, 401)

    @patch('app.CAL_COM_API_KEY', None)
    def test_book_slot_no_api_key(self):
        # Set a valid auth cookie to get past the auth decorator
        self.app.set_cookie('access_token', 'valid_token')

        with patch('requests.get') as mock_get:
            # Mock the auth call so the decorator passes
            mock_get.return_value = MagicMock(status_code=200, json=lambda: {'ok': True, 'user': {}})

            response = self.app.post('/engage/booking/slot', json={
                'name': 'John Doe', 'email': 'john.doe@example.com',
                'event_type_id': 123, 'price_lock': 'lock_12345'
            })

            self.assertEqual(response.status_code, 500)
            json_data = response.get_json()
            self.assertEqual(json_data['error'], 'Booking system is not configured.')


if __name__ == '__main__':
    unittest.main()
