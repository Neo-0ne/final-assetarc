import unittest
from app.estate_calculator import EstateInput, Asset, calculate_estate_duty

class TestEstateCalculator(unittest.TestCase):

    def test_unstructured_estate(self):
        """Test a simple case with all assets in the personal estate."""
        estate_input = EstateInput(assets=[
            Asset(name="Family Home", value=5000000),
            Asset(name="Share Portfolio", value=2000000),
        ])

        result = calculate_estate_duty(estate_input)

        gross_value = 7000000
        executor_fees = gross_value * 0.035 # 245,000
        net_estate = gross_value - executor_fees # 6,755,000
        dutiable_amount = net_estate - 3500000 # 3,255,000
        estate_duty = dutiable_amount * 0.20 # 651,000

        self.assertAlmostEqual(result['before_scenario']['gross_estate_value'], gross_value)
        self.assertAlmostEqual(result['before_scenario']['executor_fees'], executor_fees)
        self.assertAlmostEqual(result['before_scenario']['estate_duty'], estate_duty)

        # In the "after" scenario for this case, nothing is in trust, so results should be the same
        self.assertAlmostEqual(result['after_scenario']['total_costs'], result['before_scenario']['total_costs'])
        self.assertEqual(result['summary']['total_savings'], 0)

    def test_fully_structured_estate(self):
        """Test a case where all assets are correctly placed in a trust."""
        estate_input = EstateInput(assets=[
            Asset(name="Family Home", value=5000000, in_trust=True),
            Asset(name="Share Portfolio", value=2000000, in_trust=True),
        ])

        result = calculate_estate_duty(estate_input)

        # "After" scenario should have zero costs
        self.assertEqual(result['after_scenario']['gross_estate_value'], 0)
        self.assertEqual(result['after_scenario']['executor_fees'], 0)
        self.assertEqual(result['after_scenario']['estate_duty'], 0)
        self.assertEqual(result['after_scenario']['total_costs'], 0)

        # Savings should be equal to the "before" costs
        self.assertAlmostEqual(result['summary']['total_savings'], result['before_scenario']['total_costs'])
        self.assertGreater(result['summary']['total_savings'], 0)

    def test_partially_structured_estate(self):
        """Test a mixed case with some assets in the estate and some in a trust."""
        estate_input = EstateInput(assets=[
            Asset(name="Business Property", value=10000000, in_trust=True),
            Asset(name="Personal Car", value=500000),
        ])

        result = calculate_estate_duty(estate_input)

        # "After" scenario should only consider the car
        gross_value_after = 500000
        executor_fees_after = gross_value_after * 0.035 # 17,500
        net_estate_after = gross_value_after - executor_fees_after # 482,500
        # Dutiable amount is 0 because it's less than the 3.5M abatement
        estate_duty_after = 0

        self.assertAlmostEqual(result['after_scenario']['executor_fees'], executor_fees_after)
        self.assertEqual(result['after_scenario']['estate_duty'], estate_duty_after)
        self.assertGreater(result['summary']['total_savings'], 0)

    def test_high_value_estate_tier_2_tax(self):
        """Test an estate that exceeds the R30 million threshold."""
        estate_input = EstateInput(assets=[
            Asset(name="Commercial Portfolio", value=40000000),
        ])

        result = calculate_estate_duty(estate_input)

        gross_value = 40000000
        executor_fees = gross_value * 0.035 # 1,400,000
        net_estate = gross_value - executor_fees # 38,600,000
        dutiable_amount = net_estate - 3500000 # 35,100,000

        # Duty on first 30M @ 20% = 6,000,000
        # Duty on remaining 5.1M @ 25% = 1,275,000
        # Total Duty = 7,275,000
        expected_duty = (30000000 * 0.20) + ((dutiable_amount - 30000000) * 0.25)

        self.assertAlmostEqual(result['before_scenario']['estate_duty'], expected_duty)

if __name__ == '__main__':
    unittest.main()
