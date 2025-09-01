"""
This module contains the logic for the South African Tax Residency Planner.
It implements the Ordinary Residence Test and the Physical Presence Test
as defined in the Income Tax Act.
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional

class OrdinaryResidenceFlags(BaseModel):
    """Flags representing ties to South Africa for the Ordinary Residence Test."""
    has_permanent_home: bool = Field(..., description="Does the person have a permanent home available in SA?")
    has_family_ties: bool = Field(..., description="Are the person's immediate family (spouse, children) in SA?")
    has_economic_ties: bool = Field(..., description="Are the person's main economic interests (business, assets) in SA?")
    intends_to_return: bool = Field(..., description="Does the person intend to return to SA as their real home?")

class ResidencyPlannerInput(BaseModel):
    """Input model for the residency planner calculator."""
    days_in_current_year: int = Field(..., ge=0, le=366, description="Number of days physically present in SA in the current tax year.")
    days_each_of_prev_5_years: List[int] = Field(..., min_items=5, max_items=5, description="A list of days present in each of the 5 preceding tax years.")
    ordinary_residence_flags: OrdinaryResidenceFlags
    days_continuously_absent: Optional[int] = Field(None, ge=0, description="For the exit rule, the number of continuous days spent outside SA.")

    @validator('days_each_of_prev_5_years')
    def check_days_in_year(cls, v):
        for days in v:
            if not (0 <= days <= 366):
                raise ValueError('Days in any given year must be between 0 and 366.')
        return v

def determine_residency_status(inputs: ResidencyPlannerInput):
    """
    Determines tax residency status based on the provided inputs.
    Follows the logic flow: Ordinary Residence -> Physical Presence -> Exit Rule.
    """
    # --- Step 1: Ordinary Residence Test ---
    # This is a subjective test. For this tool, we'll use a rule-based heuristic.
    # If the user has strong ties (e.g., 3 or more flags), we consider them ordinarily resident.
    flags = inputs.ordinary_residence_flags
    true_flags_count = sum([
        flags.has_permanent_home,
        flags.has_family_ties,
        flags.has_economic_ties,
        flags.intends_to_return
    ])

    if true_flags_count >= 3:
        return {
            "status": "Resident",
            "reasoning": "You are considered ordinarily resident in South Africa due to your significant personal and economic ties.",
            "advice": "As a resident, you are subject to SA tax on your worldwide income. You may be able to claim foreign tax credits for tax paid in other countries. A Double Tax Agreement (DTA) may apply."
        }

    # --- Step 2: Physical Presence Test ---
    physically_resident = False
    test_conditions = {
        "current_year_test": inputs.days_in_current_year >= 91,
        "preceding_years_test": all(d >= 91 for d in inputs.days_each_of_prev_5_years),
        "total_days_test": sum(inputs.days_each_of_prev_5_years) >= 915
    }

    if all(test_conditions.values()):
        physically_resident = True

    # --- Step 3: Exit Rule (330-day rule) ---
    if physically_resident and inputs.days_continuously_absent is not None:
        if inputs.days_continuously_absent >= 330:
            return {
                "status": "Non-Resident",
                "reasoning": "Although you met the physical presence test, you have since been continuously outside of South Africa for at least 330 days, which ceases your tax residency from the date of departure.",
                "advice": "As a non-resident, you are generally only taxed on income sourced from South Africa."
            }

    # --- Final Determination ---
    if physically_resident:
        return {
            "status": "Resident",
            "reasoning": "You meet the requirements of the physical presence test (the day-counting test).",
            "advice": "As a resident, you are subject to SA tax on your worldwide income. You may be able to claim foreign tax credits. A Double Tax Agreement (DTA) may also apply. If you remain outside SA for a continuous period of 330 days, you will cease to be a resident."
        }

    # If neither test is met
    reasoning_details = [f"Days in current year >= 91: {'Pass' if test_conditions['current_year_test'] else 'Fail'}",
                         f"Days in each of past 5 years >= 91: {'Pass' if test_conditions['preceding_years_test'] else 'Fail'}",
                         f"Total days in past 5 years >= 915: {'Pass' if test_conditions['total_days_test'] else 'Fail'}"]

    return {
        "status": "Non-Resident",
        "reasoning": f"You do not meet the requirements for ordinary residence or the physical presence test. Failures: {', '.join([r for r in reasoning_details if 'Fail' in r])}",
        "advice": "As a non-resident, you are generally only taxed on income sourced from South Africa."
    }
