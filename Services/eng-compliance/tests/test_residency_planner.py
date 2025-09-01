import os
import json
from unittest import TestCase

# Set all feature flags to true for a consistent testing environment
os.environ['BEE_CALCULATOR_ENABLED'] = 'true'
os.environ['ESTATE_CALCULATOR_ENABLED'] = 'true'
os.environ['SUCCESSION_PLANNER_ENABLED'] = 'true'
os.environ['INSURANCE_WRAPPER_CALCULATOR_ENABLED'] = 'true'
os.environ['RESIDENCY_PLANNER_ENABLED'] = 'true'
os.environ['ROLLOVER_PLANNER_ENABLED'] = 'true'

from app.app import app

class TestResidencyPlanner(TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.base_payload = {
            "module_id": "residency_planner",
            "inputs": {
                "days_in_current_year": 0,
                "days_each_of_prev_5_years": [0, 0, 0, 0, 0],
                "ordinary_residence_flags": {
                    "has_permanent_home": False,
                    "has_family_ties": False,
                    "has_economic_ties": False,
                    "intends_to_return": False
                },
                "days_continuously_absent": None
            }
        }

    def test_ordinarily_resident(self):
        """Test a user who is clearly ordinarily resident."""
        payload = self.base_payload.copy()
        payload['inputs']['ordinary_residence_flags'] = {
            "has_permanent_home": True,
            "has_family_ties": True,
            "has_economic_ties": True,
            "intends_to_return": True
        }

        response = self.app.post('/compliance/run', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertTrue(data['ok'])
        self.assertEqual(data['result']['details']['status'], 'Resident')
        self.assertIn('ordinarily resident', data['result']['details']['reasoning'])

    def test_physical_presence_pass(self):
        """Test a user who passes the physical presence test (user's example 2)."""
        payload = self.base_payload.copy()
        payload['inputs']['days_in_current_year'] = 120
        payload['inputs']['days_each_of_prev_5_years'] = [200, 180, 150, 200, 220] # sum = 950

        response = self.app.post('/compliance/run', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertTrue(data['ok'])
        self.assertEqual(data['result']['details']['status'], 'Resident')
        self.assertIn('physical presence test', data['result']['details']['reasoning'])

    def test_physical_presence_fail_total_days(self):
        """Test a user who fails the 915-day total (user's example 1)."""
        payload = self.base_payload.copy()
        payload['inputs']['days_in_current_year'] = 120
        payload['inputs']['days_each_of_prev_5_years'] = [150, 100, 95, 120, 130] # sum = 595

        response = self.app.post('/compliance/run', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertTrue(data['ok'])
        self.assertEqual(data['result']['details']['status'], 'Non-Resident')
        self.assertIn('Total days in past 5 years >= 915: Fail', data['result']['details']['reasoning'])

    def test_physical_presence_fail_one_year(self):
        """Test a user who fails because one of the preceding years is < 91 days."""
        payload = self.base_payload.copy()
        payload['inputs']['days_in_current_year'] = 100
        payload['inputs']['days_each_of_prev_5_years'] = [200, 200, 80, 200, 200] # sum = 880

        response = self.app.post('/compliance/run', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertTrue(data['ok'])
        self.assertEqual(data['result']['details']['status'], 'Non-Resident')
        self.assertIn('Days in each of past 5 years >= 91: Fail', data['result']['details']['reasoning'])

    def test_exit_rule_applies(self):
        """Test the 330-day exit rule for a user who was physically present."""
        payload = self.base_payload.copy()
        payload['inputs']['days_in_current_year'] = 120
        payload['inputs']['days_each_of_prev_5_years'] = [200, 180, 150, 200, 220] # Pass presence test
        payload['inputs']['days_continuously_absent'] = 331

        response = self.app.post('/compliance/run', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertTrue(data['ok'])
        self.assertEqual(data['result']['details']['status'], 'Non-Resident')
        self.assertIn('continuously outside of South Africa', data['result']['details']['reasoning'])

    def test_input_validation_error(self):
        """Test that invalid input returns a proper error."""
        payload = self.base_payload.copy()
        payload['inputs']['days_each_of_prev_5_years'] = [100, 100] # Invalid list length

        response = self.app.post('/compliance/run', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertFalse(data['ok'])
        self.assertEqual(data['result']['status'], 'error')
        self.assertIn('Input data is invalid', data['result']['summary'])
        # Check for Pydantic v2 error message for list length
        self.assertTrue(any('5 items' in e['msg'] for e in data['result']['details']))
