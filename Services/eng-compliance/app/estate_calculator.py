from pydantic import BaseModel, Field
from typing import List

# --- Constants based on research ---
EXECUTOR_FEE_PERCENTAGE = 0.035  # 3.5%
ESTATE_DUTY_ABATEMENT = 3500000.00  # R3.5 million
ESTATE_DUTY_RATE_TIER_1 = 0.20  # 20%
ESTATE_DUTY_RATE_TIER_2 = 0.25  # 25%
ESTATE_DUTY_TIER_1_THRESHOLD = 30000000.00  # R30 million

# --- Data Models for Input ---

class Asset(BaseModel):
    name: str
    value: float = Field(..., gt=0)
    in_trust: bool = Field(False, description="Is the asset held within a trust?")

class EstateInput(BaseModel):
    assets: List[Asset]

# --- Calculator Logic ---

def calculate_estate_duty(estate_input: EstateInput):
    """
    Calculates the potential executor fees and estate duty for a given list of assets.
    It provides a 'before' (unstructured) and 'after' (structured) scenario.
    """

    # --- "Before" Scenario (Unstructured) ---
    # All assets are considered part of the personal estate.
    gross_estate_value_before = sum(asset.value for asset in estate_input.assets)

    executor_fees_before = gross_estate_value_before * EXECUTOR_FEE_PERCENTAGE

    # Net estate is gross value less executor fees (and other liabilities, simplified here)
    net_estate_value_before = gross_estate_value_before - executor_fees_before

    # Dutiable estate is net estate less the abatement
    dutiable_estate_before = max(0, net_estate_value_before - ESTATE_DUTY_ABATEMENT)

    estate_duty_before = 0
    if dutiable_estate_before > 0:
        if dutiable_estate_before <= ESTATE_DUTY_TIER_1_THRESHOLD:
            estate_duty_before = dutiable_estate_before * ESTATE_DUTY_RATE_TIER_1
        else:
            duty_on_tier_1 = ESTATE_DUTY_TIER_1_THRESHOLD * ESTATE_DUTY_RATE_TIER_1
            duty_on_tier_2 = (dutiable_estate_before - ESTATE_DUTY_TIER_1_THRESHOLD) * ESTATE_DUTY_RATE_TIER_2
            estate_duty_before = duty_on_tier_1 + duty_on_tier_2

    total_costs_before = executor_fees_before + estate_duty_before
    net_inheritance_before = gross_estate_value_before - total_costs_before

    # --- "After" Scenario (Structured) ---
    # Only assets NOT in a trust are part of the personal estate.
    personal_assets_after = [asset for asset in estate_input.assets if not asset.in_trust]
    gross_estate_value_after = sum(asset.value for asset in personal_assets_after)

    executor_fees_after = gross_estate_value_after * EXECUTOR_FEE_PERCENTAGE

    net_estate_value_after = gross_estate_value_after - executor_fees_after

    dutiable_estate_after = max(0, net_estate_value_after - ESTATE_DUTY_ABATEMENT)

    estate_duty_after = 0
    if dutiable_estate_after > 0:
        if dutiable_estate_after <= ESTATE_DUTY_TIER_1_THRESHOLD:
            estate_duty_after = dutiable_estate_after * ESTATE_DUTY_RATE_TIER_1
        else:
            duty_on_tier_1 = ESTATE_DUTY_TIER_1_THRESHOLD * ESTATE_DUTY_RATE_TIER_1
            duty_on_tier_2 = (dutiable_estate_after - ESTATE_DUTY_TIER_1_THRESHOLD) * ESTATE_DUTY_RATE_TIER_2
            estate_duty_after = duty_on_tier_1 + duty_on_tier_2

    total_costs_after = executor_fees_after + estate_duty_after
    net_inheritance_after = gross_estate_value_before - total_costs_after # Compare to total assets

    savings = total_costs_before - total_costs_after

    return {
        "before_scenario": {
            "gross_estate_value": gross_estate_value_before,
            "executor_fees": executor_fees_before,
            "estate_duty": estate_duty_before,
            "total_costs": total_costs_before,
            "net_inheritance": net_inheritance_before
        },
        "after_scenario": {
            "gross_estate_value": gross_estate_value_after,
            "executor_fees": executor_fees_after,
            "estate_duty": estate_duty_after,
            "total_costs": total_costs_after,
            "net_inheritance": net_inheritance_after
        },
        "summary": {
            "total_savings": savings
        }
    }
