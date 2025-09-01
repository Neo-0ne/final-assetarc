import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from app import app

class LifecycleTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app._emit_event')
    @patch('requests.get')
    @patch('requests.post')
    def test_generate_pack_success(self, mock_post, mock_get, mock_emit_event):
        # Mock auth check
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {'ok': True, 'user': {}})
        self.app.set_cookie('access_token', 'valid_token')

        # Mock drafting and vault responses
        mock_draft_response = MagicMock()
        mock_draft_response.status_code = 200
        mock_draft_response.content = b'fake document content'
        mock_draft_response.headers = {'Content-Disposition': 'attachment; filename=test.docx'}

        mock_vault_response = MagicMock()
        mock_vault_response.status_code = 200
        mock_vault_response.json.return_value = {'file_id': 'vault-file-123'}

        mock_post.side_effect = [
            mock_draft_response, # For first template
            mock_draft_response, # For second template
            mock_draft_response, # For third template
            mock_vault_response  # For vault upload
        ]

        # Data for the request
        pack_data = {
            "flow_id": "za_pty_ltd",
            "data": {
                "company_name": "Test Inc."
            }
        }

        response = self.app.post('/lifecycle/pack', json=pack_data)

        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertTrue(json_data['ok'])
        self.assertEqual(json_data['pack_file_id'], 'vault-file-123')

        # 3 calls to drafting + 1 to vault = 4 post calls
        self.assertEqual(mock_post.call_count, 4)
        # Check that the vault upload was called with cookies
        vault_call_kwargs = mock_post.call_args[1]
        self.assertIn('cookies', vault_call_kwargs)
        self.assertIn('access_token', vault_call_kwargs['cookies'])

        # Assert that the event was emitted
        mock_emit_event.assert_called_once_with("pack.generated", {
            "flow_id": "za_pty_ltd",
            "pack_file_id": "vault-file-123"
        })

    def test_generate_pack_unauthorized(self):
        response = self.app.post('/lifecycle/pack', json={})
        self.assertEqual(response.status_code, 401)

    def test_generate_pack_invalid_flow_id(self):
        # Mock auth check
        with patch('requests.get') as mock_get:
            mock_get.return_value = MagicMock(status_code=200, json=lambda: {'ok': True, 'user': {}})
            self.app.set_cookie('access_token', 'valid_token')

            pack_data = {"flow_id": "non_existent_flow", "data": {}}
            response = self.app.post('/lifecycle/pack', json=pack_data)

            self.assertEqual(response.status_code, 404)
            self.assertIn("not found", response.get_json()['error'])


if __name__ == '__main__':
    unittest.main()
