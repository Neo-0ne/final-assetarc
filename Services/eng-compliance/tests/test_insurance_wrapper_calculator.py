import os
import json
from unittest import TestCase
from unittest.mock import patch

# It's crucial to set the feature flag *before* importing the app
os.environ['INSURANCE_WRAPPER_CALCULATOR_ENABLED'] = 'true'

from app.app import app

class TestInsuranceWrapperCalculator(TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_insurance_wrapper_calculator_individual(self):
        """
        Test the insurance wrapper calculator for an 'individual' investor type.
        """
        payload = {
            "module_id": "insurance_wrapper_calculator",
            "inputs": {
                "investment_amount": 1000000,
                "investment_period_years": 10,
                "annual_growth_rate": 0.08,
                "investor_type": "individual"
            }
        }

        response = self.app.post('/compliance/run',
                                 data=json.dumps(payload),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertTrue(data['ok'])
        self.assertEqual(data['module_id'], 'insurance_wrapper_calculator')

        results = data['result']['details']['results']
        summary = results['summary']

        # --- Manual Calculation for Verification ---
        # FV = 1,000,000 * (1.08)^10 = 2,158,924.997
        # Total Growth = 1,158,925.00
        total_growth = 1158925.00
        self.assertAlmostEqual(results['total_growth'], total_growth, places=0)

        # Unwrapped Tax (Individual)
        # Interest Component = 1,158,925 * 0.4 = 463,570
        # Capital Gains Component = 1,158,925 * 0.4 = 463,570
        # Dividend Component = 1,158,925 * 0.2 = 231,785
        # Tax on Interest = 463,570 * 0.45 = 208,606.5
        # Tax on CGT = 463,570 * 0.18 = 83,442.6
        # Tax on Dividends = 231,785 * 0.20 = 46,357
        # Total Unwrapped Tax = 208,606.5 + 83,442.6 + 46,357 = 338,406.1
        unwrapped_tax = 338406.1
        self.assertAlmostEqual(results['unwrapped_investment']['total_tax'], unwrapped_tax, places=0)

        # Wrapped Tax (Individual)
        # Total Growth * CGT Rate = 1,158,925 * 0.18 = 208,606.5
        wrapped_tax = 208606.5
        self.assertAlmostEqual(results['wrapped_investment']['total_tax'], wrapped_tax, places=0)

        # Summary
        # Tax Saving = 338,406.1 - 208,606.5 = 129,799.6
        tax_saving = 129799.6
        self.assertAlmostEqual(summary['tax_saving_with_wrapper'], tax_saving, places=0)

    def test_input_validation(self):
        """
        Test that invalid input returns a 400 error with details.
        """
        payload = {
            "module_id": "insurance_wrapper_calculator",
            "inputs": {
                "investment_amount": -100, # Invalid
                "investment_period_years": 10,
                "annual_growth_rate": 0.08,
                "investor_type": "invalid_type" # Invalid
            }
        }

        response = self.app.post('/compliance/run',
                                 data=json.dumps(payload),
                                 content_type='application/json')

        # The main endpoint catches the validation error and returns a 200 OK with error details
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertFalse(data['ok'])
        self.assertIn("Input data is invalid", data['result']['summary'])
        # Check for specific error messages from Pydantic v2
        errors = data['result']['details']
        error_messages = [e['msg'] for e in errors]
        self.assertIn('Input should be greater than 0', error_messages)
        self.assertTrue(any("String should match pattern" in msg for msg in error_messages))
