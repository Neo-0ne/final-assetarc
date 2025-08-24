import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from io import BytesIO

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from app import app

# Use mock objects for external services
mock_engine = MagicMock()
mock_storage_client = MagicMock()
mock_bucket = MagicMock()

@patch('app.engine', mock_engine)
@patch('app.bucket', mock_bucket)
@patch('app.storage_client', mock_storage_client)
class VaultTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = self.mock_conn
        mock_engine.begin.return_value.__enter__.return_value = self.mock_conn
        self.mock_conn.execute.reset_mock()
        mock_bucket.blob.reset_mock()

    @patch('requests.get')
    def test_upload_file_success(self, mock_auth_get):
        # Mock successful authentication
        mock_auth_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {'ok': True, 'user': {'email': 'test@example.com'}}
        )
        self.app.set_cookie('access_token', 'valid_token')

        # Mock file data
        file_data = {
            'file': (BytesIO(b'my file contents'), 'test.txt')
        }

        response = self.app.post('/vault/upload', data=file_data, content_type='multipart/form-data')

        self.assertEqual(response.status_code, 201)
        json_data = response.get_json()
        self.assertIn('file_id', json_data)

        # Check that the file was "uploaded" to GCS mock
        mock_bucket.blob.assert_called_once()
        # Check that metadata was inserted into the DB
        self.assertTrue(any("INSERT INTO files" in str(c[0][0]) for c in self.mock_conn.execute.call_args_list))

    def test_upload_file_unauthorized(self):
        response = self.app.post('/vault/upload', data={}, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 401)

    @patch('requests.get')
    def test_get_file_url_success(self, mock_auth_get):
        user_email = 'owner@example.com'
        file_id = 'test-file-id'

        # Mock successful authentication for the file owner
        mock_auth_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {'ok': True, 'user': {'email': user_email}}
        )
        self.app.set_cookie('access_token', 'valid_token')

        # Mock the file metadata in the database
        mock_file_info = MagicMock()
        mock_file_info.gcs_path = f"uploads/{user_email}/{file_id}/test.txt"
        mock_file_info.user_id = user_email
        self.mock_conn.execute.return_value.first.return_value = mock_file_info

        # Mock the GCS signed URL generation
        mock_bucket.blob.return_value.generate_signed_url.return_value = "https://fake.storage.url/test.txt"

        response = self.app.get(f'/vault/file/{file_id}')

        self.assertEqual(response.status_code, 200)
        self.assertIn('url', response.get_json())

    @patch('requests.get')
    def test_get_file_url_forbidden(self, mock_auth_get):
        owner_email = 'owner@example.com'
        requester_email = 'other_user@example.com'
        file_id = 'test-file-id'

        # Mock successful authentication for a DIFFERENT user
        mock_auth_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {'ok': True, 'user': {'email': requester_email}}
        )
        self.app.set_cookie('access_token', 'valid_token')

        # Mock the file metadata in the database (owned by someone else)
        mock_file_info = MagicMock()
        mock_file_info.user_id = owner_email
        self.mock_conn.execute.return_value.first.return_value = mock_file_info

        response = self.app.get(f'/vault/file/{file_id}')

        self.assertEqual(response.status_code, 403)

if __name__ == '__main__':
    unittest.main()
