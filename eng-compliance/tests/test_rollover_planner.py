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

class TestRolloverPlanner(TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.base_payload = {
            "module_id": "rollover_planner",
            "inputs": {
                "section": "s42",
                "taxpayer_type": "company",
                "transferor_residency": "SA",
                "transferee_residency": "SA",
                "group_relationship": {"same_group": True, "percentage": 80},
                "consideration": {"shares_issued": True, "cash_boot": 0, "debt_assumed": 0},
                "asset_profile": {"type": "capital", "market_value": 10000000, "base_cost": 5000000},
                "continuity_flags": {"nature_retained": True, "anti_avoidance_risk": False},
                "timing_flags": {"earmarked_disposal_months": None},
                "unbundling_details": {"listed": True, "control_threshold_met": True},
                "liquidation_details": {"steps_to_deregister_within_36m": True, "retain_assets_for_debt": True},
                "recoupments": 0,
                "allowances_claimed": 0
            }
        }

    def test_s42_happy_path(self):
        """Test a successful Section 42 asset-for-share transaction."""
        payload = self.base_payload.copy()
        payload['inputs']['section'] = 's42'

        response = self.app.post('/compliance/run', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertTrue(data['ok'])
        self.assertTrue(data['result']['details']['eligibility']['eligible'])
        self.assertGreater(data['result']['details']['tax_comparison']['cgt_no_relief'], 0)
        self.assertEqual(data['result']['details']['tax_comparison']['cgt_with_relief'], 0)
        self.assertGreater(data['result']['details']['tax_comparison']['net_deferral_benefit'], 0)

    def test_s45_fail_group_relationship(self):
        """Test a Section 45 transaction that fails due to insufficient group percentage."""
        payload = self.base_payload.copy()
        payload['inputs']['section'] = 's45'
        payload['inputs']['group_relationship']['percentage'] = 50 # Below 70% requirement

        response = self.app.post('/compliance/run', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertTrue(data['ok']) # The API call itself is ok
        self.assertFalse(data['result']['details']['eligibility']['eligible'])
        self.assertIn("must be between companies in the same group (>= 70% shareholding)", data['result']['details']['eligibility']['failed_reasons'][0])
        # Tax should be calculated as if there's no relief
        self.assertGreater(data['result']['details']['tax_comparison']['cgt_no_relief'], 0)
        self.assertEqual(data['result']['details']['tax_comparison']['cgt_with_relief'], data['result']['details']['tax_comparison']['cgt_no_relief'])


    def test_s47_happy_path(self):
        """Test a successful Section 47 liquidation transaction."""
        payload = self.base_payload.copy()
        payload['inputs']['section'] = 's47'

        response = self.app.post('/compliance/run', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertTrue(data['ok'])
        self.assertTrue(data['result']['details']['eligibility']['eligible'])
        self.assertGreater(data['result']['details']['tax_comparison']['net_deferral_benefit'], 0)

    def test_tax_calculation_individual(self):
        """Verify the tax calculation for an individual taxpayer."""
        payload = self.base_payload.copy()
        payload['inputs']['section'] = 's42'
        payload['inputs']['taxpayer_type'] = 'individual'
        payload['inputs']['asset_profile']['market_value'] = 1000000
        payload['inputs']['asset_profile']['base_cost'] = 500000

        response = self.app.post('/compliance/run', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertTrue(data['ok'])
        # Manual calc: Gain = 500k. Taxable Gain = 500k * 40% = 200k. CGT = 200k * 45% = 90k
        expected_cgt = 90000
        self.assertAlmostEqual(data['result']['details']['tax_comparison']['cgt_no_relief'], expected_cgt)
        self.assertAlmostEqual(data['result']['details']['tax_comparison']['net_deferral_benefit'], expected_cgt)

    def test_input_validation(self):
        """Test that invalid input returns a proper error."""
        payload = self.base_payload.copy()
        payload['inputs']['group_relationship']['percentage'] = -10 # Invalid value

        response = self.app.post('/compliance/run', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertFalse(data['ok'])
        self.assertEqual(data['result']['status'], 'error')
        self.assertIn('Input data is invalid', data['result']['summary'])
