import unittest
from unittest.mock import patch
import os
import sys
import json

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from app import app

class DraftingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_render_document_success(self):
        # Data for a successful render
        render_data = {
            "template_id": "booking_confirmation.v1",
            "data": {
                "name": "Jules",
                "booking_url": "https://cal.com/booking/test"
            }
        }

        response = self.app.post('/doc/render', json=render_data)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
        response_text = response.get_data(as_text=True)
        self.assertIn("Hello Jules", response_text)
        self.assertIn("https://cal.com/booking/test", response_text)

    def test_render_document_template_not_found(self):
        render_data = {
            "template_id": "non_existent_template.v1",
            "data": {}
        }

        response = self.app.post('/doc/render', json=render_data)

        self.assertEqual(response.status_code, 404)
        json_data = response.get_json()
        self.assertEqual(json_data['error'], "Template with id 'non_existent_template.v1' not found")

    def test_render_document_missing_data(self):
        response = self.app.post('/doc/render', json={"template_id": "booking_confirmation.v1"})

        self.assertEqual(response.status_code, 400)
        json_data = response.get_json()
        self.assertEqual(json_data['error'], "Missing template_id or data in request")

    @patch('os.path.exists')
    def test_render_document_file_not_found(self, mock_exists):
        # Mock os.path.exists to return False, simulating a missing file
        mock_exists.return_value = False

        render_data = {
            "template_id": "booking_confirmation.v1",
            "data": {}
        }

        response = self.app.post('/doc/render', json=render_data)

        self.assertEqual(response.status_code, 500)
        json_data = response.get_json()
        self.assertIn("Template file not found at path", json_data['error'])


if __name__ == '__main__':
    unittest.main()
