import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from datetime import datetime, timedelta, timezone

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from app import app

# Use a mock engine for all tests
mock_engine = MagicMock()

@patch('app.engine', mock_engine)
class AnalyticsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Patch init_db to prevent it from running before each request
        self.init_db_patcher = patch('app.init_db', return_value=None)
        self.init_db_patcher.start()

        self.mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = self.mock_conn
        mock_engine.begin.return_value.__enter__.return_value = self.mock_conn
        self.mock_conn.execute.reset_mock()

    def tearDown(self):
        self.init_db_patcher.stop()

    def test_get_kpi_success(self):
        def mock_execute(query, params):
            mock_result = MagicMock()
            if params['event'] == 'user.created':
                mock_result.scalar_one_or_none.return_value = 5
            elif params['event'] == 'user.login':
                mock_result.scalar_one_or_none.return_value = 12
            elif params['event'] == 'pack.generated':
                mock_result.scalar_one_or_none.return_value = 3
            else:
                mock_result.scalar_one_or_none.return_value = 0
            return mock_result

        self.mock_conn.execute.side_effect = mock_execute

        response = self.app.get('/analytics/kpi')

        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertTrue(json_data['ok'])

        kpis = json_data['kpis']
        self.assertEqual(kpis['users_created_today'], 5)
        self.assertEqual(kpis['logins_today'], 12)
        self.assertEqual(kpis['packs_generated_today'], 3)

        self.assertEqual(self.mock_conn.execute.call_count, 3)

    def test_get_kpi_no_events(self):
        self.mock_conn.execute.return_value.scalar_one_or_none.return_value = 0
        response = self.app.get('/analytics/kpi')
        self.assertEqual(response.status_code, 200)
        kpis = response.get_json()['kpis']
        self.assertEqual(kpis['users_created_today'], 0)

    def test_ingest_event_success(self):
        event_data = {
            "event_type": "test.event",
            "payload": {"foo": "bar"},
            "service": "test_service",
            "user_id": "test_user"
        }

        response = self.app.post('/events/ingest', json=event_data)

        self.assertEqual(response.status_code, 202)
        self.assertTrue(response.get_json()['ok'])

        self.mock_conn.execute.assert_called_once()
        # The parameters are the second positional argument of the call
        last_call_params = self.mock_conn.execute.call_args[0][1]
        self.assertEqual(last_call_params['event_type'], 'test.event')
        self.assertEqual(last_call_params['user_id'], 'test_user')

    @patch('app._get_kpi_data')
    def test_get_dashboard_success(self, mock_get_kpi):
        # Mock the helper function to return sample data
        mock_get_kpi.return_value = {
            "users_created_today": 10,
            "logins_today": 25,
            "packs_generated_today": 5
        }

        response = self.app.get('/analytics/dashboard')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

        # Check for key elements in the rendered HTML
        response_text = response.get_data(as_text=True)
        self.assertIn('<title>AssetArc Analytics Dashboard</title>', response_text)
        self.assertIn('<canvas id="kpiChart"></canvas>', response_text)

        # Check that the data is being passed to the template, ignoring whitespace issues
        self.assertIn('"users_created_today": 10', response_text)
        self.assertIn('"logins_today": 25', response_text)
        self.assertIn('"packs_generated_today": 5', response_text)

if __name__ == '__main__':
    unittest.main()
