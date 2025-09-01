import unittest
from app.bbee import OwnershipStructure, calculate_ownership_scorecard, Shareholder

class TestBBEECalculator(unittest.TestCase):

    def test_simple_case_full_points(self):
        """
        Test a simple case where the entity should get full points for all indicators.
        """
        structure = OwnershipStructure(
            total_entity_value=1000000,
            total_acquisition_debt=0,
            years_since_equity_deal=10,
            shareholders=[
                Shareholder(
                    is_black=True,
                    is_black_woman=True,
                    voting_percentage=51.0,
                    economic_interest_percentage=51.0
                )
            ]
        )

        result = calculate_ownership_scorecard(structure)

        # Check individual points
        self.assertEqual(result['indicators']['voting_rights']['points'], 4.0)
        self.assertEqual(result['indicators']['voting_rights_black_women']['points'], 2.0)
        self.assertEqual(result['indicators']['economic_interest']['points'], 8.0)
        self.assertEqual(result['indicators']['economic_interest_black_women']['points'], 4.0)
        self.assertEqual(result['indicators']['net_value']['points'], 8.0)

        # Check total and discounting
        self.assertGreater(result['total_ownership_points'], 24.0) # Should be 26 in this ideal case
        self.assertFalse(result['discounting_principle_applied'])

    def test_net_value_sub_minimum_fail(self):
        """
        Test a case where the Net Value sub-minimum is not met, triggering the discounting principle.
        This happens when the acquisition debt is high relative to the equity value.
        """
        structure = OwnershipStructure(
            total_entity_value=1000000,
            total_acquisition_debt=480000, # 510k equity - 480k debt = 30k net value
            years_since_equity_deal=10, # Time factor is 1.0
            shareholders=[
                Shareholder(
                    is_black=True,
                    is_black_woman=False,
                    voting_percentage=51.0,
                    economic_interest_percentage=51.0
                )
            ]
        )

        result = calculate_ownership_scorecard(structure)

        # Net value points should be low
        # Deemed Net Value = (510k - 480k) / 1M = 0.03
        # Formula A = (0.03 / (0.25 * 1.0)) * 8 = 0.96 points
        # Formula B = (51 / 25) * 8 = 16.32
        # Final = min(0.96, 16.32) = 0.96
        self.assertAlmostEqual(result['indicators']['net_value']['points'], 0.96, places=2)

        # Discounting should be applied because 0.96 < 3.2
        self.assertTrue(result['discounting_principle_applied'])

    def test_time_based_graduation_factor(self):
        """
        Test the effect of the time-based graduation factor on Net Value.
        """
        # Year 1, factor is 10%
        structure_year_1 = OwnershipStructure(
            total_entity_value=1000000,
            total_acquisition_debt=0,
            years_since_equity_deal=1,
            shareholders=[Shareholder(is_black=True, is_black_woman=False, voting_percentage=25, economic_interest_percentage=25)]
        )
        result_year_1 = calculate_ownership_scorecard(structure_year_1)
        # Deemed Net Value = 0.25
        # Formula A = (0.25 / (0.25 * 0.1)) * 8 = 80 -> capped at 8
        # Formula B = (25 / 25) * 8 = 8
        # Result should be 8
        self.assertEqual(result_year_1['indicators']['net_value']['points'], 8.0)

        # A case where the time factor limits the points
        # Year 2, factor is 20%
        structure_year_2 = OwnershipStructure(
            total_entity_value=1000000,
            total_acquisition_debt=200000, # Net equity = 50k
            years_since_equity_deal=2,
            shareholders=[Shareholder(is_black=True, is_black_woman=False, voting_percentage=25, economic_interest_percentage=25)]
        )
        result_year_2 = calculate_ownership_scorecard(structure_year_2)
        # Deemed Net Value = (250k - 200k) / 1M = 0.05
        # Formula A = (0.05 / (0.25 * 0.2)) * 8 = 8
        # Formula B = (25 / 25) * 8 = 8
        # Result should be 8
        self.assertEqual(result_year_2['indicators']['net_value']['points'], 8.0)


if __name__ == '__main__':
    unittest.main()
