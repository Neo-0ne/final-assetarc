from pydantic import BaseModel, Field
from typing import List

# --- Data Models for Input ---

class Shareholder(BaseModel):
    is_black: bool = Field(..., description="Is the shareholder a Black person?")
    is_black_woman: bool = Field(..., description="Is the shareholder a Black woman?")
    voting_percentage: float = Field(..., ge=0, le=100)
    economic_interest_percentage: float = Field(..., ge=0, le=100)

class OwnershipStructure(BaseModel):
    shareholders: List[Shareholder]
    total_entity_value: float = Field(..., gt=0, description="Total fair market value of the entity.")
    total_acquisition_debt: float = Field(..., ge=0, description="Total acquisition debt held by all Black participants.")
    years_since_equity_deal: int = Field(..., ge=0, description="Number of years since the Black equity instruments were acquired.")

# --- Calculator Logic ---

def get_time_based_graduation_factor(years: int) -> float:
    """Returns the graduation factor based on the number of years."""
    if years <= 1: return 0.10
    if years == 2: return 0.20
    if years <= 4: return 0.40
    if years <= 6: return 0.60
    if years <= 8: return 0.80
    return 1.00

def calculate_ownership_scorecard(structure: OwnershipStructure):
    """
    Calculates the B-BBEE Ownership scorecard based on the provided structure.
    """

    # --- 1. Voting Rights Calculation ---
    total_black_voting = sum(s.voting_percentage for s in structure.shareholders if s.is_black)
    voting_rights_target = 25.0 # Simplified target, ignoring the "+1 vote" rule for the calculator
    voting_rights_points = min((total_black_voting / voting_rights_target) * 4, 4)

    total_black_women_voting = sum(s.voting_percentage for s in structure.shareholders if s.is_black_woman)
    voting_rights_women_target = 10.0
    voting_rights_women_points = min((total_black_women_voting / voting_rights_women_target) * 2, 2)

    # --- 2. Economic Interest Calculation ---
    total_black_economic_interest = sum(s.economic_interest_percentage for s in structure.shareholders if s.is_black)
    economic_interest_target = 25.0
    economic_interest_points = min((total_black_economic_interest / economic_interest_target) * 8, 8)

    total_black_women_economic_interest = sum(s.economic_interest_percentage for s in structure.shareholders if s.is_black_woman)
    economic_interest_women_target = 10.0 # Example target
    economic_interest_women_points = min((total_black_women_economic_interest / economic_interest_women_target) * 4, 4)

    # --- 3. Net Value Calculation ---
    black_equity_value = (total_black_economic_interest / 100) * structure.total_entity_value

    # Step 1: Deemed Net Value (A)
    deemed_net_value_numerator = black_equity_value - structure.total_acquisition_debt
    deemed_net_value = deemed_net_value_numerator / structure.total_entity_value if structure.total_entity_value > 0 else 0

    # Step 2: Two alternative formulas
    time_factor = get_time_based_graduation_factor(structure.years_since_equity_deal)

    # Formula A (Time-Based)
    formula_a_denominator = (0.25 * time_factor)
    points_a = (deemed_net_value / formula_a_denominator) * 8 if formula_a_denominator > 0 else 0

    # Formula B (Economic Interest Comparison)
    points_b = (total_black_economic_interest / 25.0) * 8

    # Final Net Value Points
    net_value_points = min(points_a, points_b)
    net_value_points = max(0, min(net_value_points, 8)) # Cap at 8 and ensure non-negative

    # --- 4. Sub-minimum Requirement and Discounting ---
    net_value_sub_minimum = 3.2 # 40% of 8 points
    discounting_applied = net_value_points < net_value_sub_minimum

    # --- 5. Total Score ---
    total_points = (
        voting_rights_points +
        voting_rights_women_points +
        economic_interest_points +
        economic_interest_women_points + # Assuming this is a separate indicator
        net_value_points
    )

    # Note: This is a simplified total. A full generic scorecard has 25 points for ownership.
    # We are only calculating the core indicators here based on user input.

    return {
        "indicators": {
            "voting_rights": {
                "points": round(voting_rights_points, 2),
                "target": f"{voting_rights_target}%",
                "actual": f"{total_black_voting}%"
            },
            "voting_rights_black_women": {
                "points": round(voting_rights_women_points, 2),
                "target": f"{voting_rights_women_target}%",
                "actual": f"{total_black_women_voting}%"
            },
            "economic_interest": {
                "points": round(economic_interest_points, 2),
                "target": f"{economic_interest_target}%",
                "actual": f"{total_black_economic_interest}%"
            },
            "economic_interest_black_women": {
                "points": round(economic_interest_women_points, 2),
                "target": f"{economic_interest_women_target}%",
                "actual": f"{total_black_women_economic_interest}%"
            },
            "net_value": {
                "points": round(net_value_points, 2),
                "target": "8 points (subject to sub-minimum)",
                "sub_minimum_met": not discounting_applied
            }
        },
        "total_ownership_points": round(total_points, 2),
        "discounting_principle_applied": discounting_applied
    }
