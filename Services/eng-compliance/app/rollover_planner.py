"""
This module contains the logic for the Section 42-47 Rollover Relief Planner.
It provides functions to check eligibility for corporate rollover relief and
to calculate the potential tax benefits.
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal

# --- Nested Models for Eligibility Checklist ---

class GroupRelationship(BaseModel):
    same_group: bool
    percentage: float = Field(..., ge=0, le=100)

class Consideration(BaseModel):
    shares_issued: bool
    cash_boot: float = Field(..., ge=0)
    debt_assumed: float = Field(..., ge=0)

class AssetProfile(BaseModel):
    type: Literal['capital', 'trading_stock', 'shares', 'immovable_property', 'ip']
    market_value: float = Field(..., ge=0)
    base_cost: float = Field(..., ge=0)

class ContinuityFlags(BaseModel):
    nature_retained: bool
    anti_avoidance_risk: bool

class TimingFlags(BaseModel):
    earmarked_disposal_months: Optional[int] = Field(None, ge=0)

class UnbundlingDetails(BaseModel):
    listed: bool
    control_threshold_met: bool

class LiquidationDetails(BaseModel):
    steps_to_deregister_within_36m: bool
    retain_assets_for_debt: bool

# --- Main Input Model ---

class RolloverPlannerInput(BaseModel):
    section: Literal['s42', 's45', 's46', 's47']
    taxpayer_type: Literal['individual', 'company', 'trust']

    # Eligibility Inputs
    transferor_residency: Literal['SA', 'non-SA']
    transferee_residency: Literal['SA', 'non-SA']
    group_relationship: GroupRelationship
    consideration: Consideration
    asset_profile: AssetProfile
    continuity_flags: ContinuityFlags
    timing_flags: TimingFlags
    unbundling_details: UnbundlingDetails
    liquidation_details: LiquidationDetails

    # Tax Calculation Inputs (can be derived from asset_profile)
    # proceeds and base_cost will be taken from asset_profile.market_value and asset_profile.base_cost
    recoupments: float = Field(0, ge=0)
    allowances_claimed: float = Field(0, ge=0)


# --- Eligibility Logic ---

def check_eligibility(inputs: RolloverPlannerInput) -> dict:
    """
    Checks if a transaction is eligible for rollover relief based on the selected section.
    Returns a dictionary with eligibility status, reasons, warnings, and a decision trace.
    """
    trace = []
    reasons = []
    warnings = []

    # --- Section 42: Asset-for-Share ---
    if inputs.section == 's42':
        # Rule: Transferee must be SA resident
        is_sa_resident_transferee = inputs.transferee_residency == 'SA'
        trace.append({"rule": "s42_resident_transferee", "pass": is_sa_resident_transferee})
        if not is_sa_resident_transferee:
            reasons.append("The company receiving the asset (transferee) must be a South African resident.")

        # Rule: Consideration must be mainly equity shares
        is_equity_consideration = inputs.consideration.shares_issued
        trace.append({"rule": "s42_equity_shares_issued", "pass": is_equity_consideration})
        if not is_equity_consideration:
            reasons.append("The consideration for the asset must be in the form of equity shares issued by the transferee company.")

        # Rule: Asset nature must be retained (e.g., capital to capital)
        trace.append({"rule": "s42_nature_retained", "pass": inputs.continuity_flags.nature_retained})
        if not inputs.continuity_flags.nature_retained:
            reasons.append("The nature of the asset must be retained by the transferee (e.g., a capital asset cannot become trading stock).")

        # Warning: 18-month disposal risk
        if inputs.timing_flags.earmarked_disposal_months is not None and inputs.timing_flags.earmarked_disposal_months < 18:
            warnings.append("Disposal of the asset by the transferee within 18 months may trigger a reversal of the tax relief.")

    # --- Section 45: Intra-group Transaction ---
    elif inputs.section == 's45':
        is_sa_resident_transferor = inputs.transferor_residency == 'SA'
        trace.append({"rule": "s45_resident_transferor", "pass": is_sa_resident_transferor})
        if not is_sa_resident_transferor:
            reasons.append("The transferor company must be a South African resident.")

        is_sa_resident_transferee = inputs.transferee_residency == 'SA'
        trace.append({"rule": "s45_resident_transferee", "pass": is_sa_resident_transferee})
        if not is_sa_resident_transferee:
            reasons.append("The transferee company must be a South African resident.")

        is_same_group = inputs.group_relationship.same_group and inputs.group_relationship.percentage >= 70
        trace.append({"rule": "s45_same_group", "pass": is_same_group})
        if not is_same_group:
            reasons.append("The transaction must be between companies in the same group (>= 70% shareholding).")

        warnings.append("De-grouping provisions can trigger a clawback of the tax relief if the group relationship ceases within a defined period.")

    # --- Section 46: Unbundling ---
    elif inputs.section == 's46':
        # For unbundling, transferor = "unbundling company", transferee = "unbundled company"
        is_sa_resident_unbundling = inputs.transferor_residency == 'SA'
        trace.append({"rule": "s46_resident_unbundling_co", "pass": is_sa_resident_unbundling})
        if not is_sa_resident_unbundling:
            reasons.append("The unbundling company must be a South African resident.")

        is_sa_resident_unbundled = inputs.transferee_residency == 'SA'
        trace.append({"rule": "s46_resident_unbundled_co", "pass": is_sa_resident_unbundled})
        if not is_sa_resident_unbundled:
            reasons.append("The unbundled company must be a South African resident.")

        control_met = inputs.unbundling_details.control_threshold_met
        trace.append({"rule": "s46_control_threshold", "pass": control_met})
        if not control_met:
            reasons.append("The required control thresholds for the unbundling transaction must be met.")

        warnings.append("The distribution of shares must be proportional to the shareholders' effective interest to qualify.")

    # --- Section 47: Liquidation ---
    elif inputs.section == 's47':
        # For liquidation, transferor = "liquidating company", transferee = "holding company"
        is_sa_resident_holding_co = inputs.transferee_residency == 'SA'
        trace.append({"rule": "s47_resident_holding_co", "pass": is_sa_resident_holding_co})
        if not is_sa_resident_holding_co:
            reasons.append("The holding company receiving the assets must be a South African resident.")

        is_same_group = inputs.group_relationship.same_group and inputs.group_relationship.percentage >= 70
        trace.append({"rule": "s47_same_group", "pass": is_same_group})
        if not is_same_group:
            reasons.append("The liquidation must be to a holding company within the same group (>= 70% shareholding).")

        dereg_steps_taken = inputs.liquidation_details.steps_to_deregister_within_36m
        trace.append({"rule": "s47_deregistration_steps", "pass": dereg_steps_taken})
        if not dereg_steps_taken:
            reasons.append("The liquidating company must take steps to liquidate, wind up, or deregister within the required timeframe (typically 36 months).")

    eligible = len(reasons) == 0
    return {"eligible": eligible, "failed_reasons": reasons, "warnings": warnings, "decision_trace": trace}


# --- Tax Calculation Logic ---

TAX_RATES = {
    'individual': {'inclusion_rate': 0.40, 'tax_rate': 0.45},
    'company': {'inclusion_rate': 0.80, 'tax_rate': 0.27},
    'trust': {'inclusion_rate': 0.80, 'tax_rate': 0.45},
}

def calculate_tax_impact(inputs: RolloverPlannerInput, eligibility: bool) -> dict:
    """Calculates the tax impact with and without rollover relief."""
    rates = TAX_RATES[inputs.taxpayer_type]

    proceeds = inputs.asset_profile.market_value
    base_cost = inputs.asset_profile.base_cost
    capital_gain = max(0, proceeds - base_cost)

    taxable_gain = capital_gain * rates['inclusion_rate']
    cgt_no_relief = taxable_gain * rates['tax_rate']

    cgt_with_relief = 0
    tax_on_boot = 0

    # "Boot" (cash or debt relief) can trigger a partial CGT liability
    boot_consideration = inputs.consideration.cash_boot + inputs.consideration.debt_assumed
    if boot_consideration > 0:
        boot_gain = min(boot_consideration, capital_gain)
        taxable_boot_gain = boot_gain * rates['inclusion_rate']
        tax_on_boot = taxable_boot_gain * rates['tax_rate']

    if eligibility:
        cgt_with_relief = tax_on_boot
        rolled_base_cost = base_cost
    else:
        # If not eligible, full CGT applies regardless
        cgt_with_relief = cgt_no_relief
        rolled_base_cost = proceeds # Acquirer gets a stepped-up base cost

    net_deferral_benefit = cgt_no_relief - cgt_with_relief

    return {
        "cgt_no_relief": round(cgt_no_relief, 2),
        "cgt_with_relief": round(cgt_with_relief, 2),
        "tax_on_boot": round(tax_on_boot, 2),
        "rolled_base_cost_to_acquirer": round(rolled_base_cost, 2),
        "net_deferral_benefit": round(net_deferral_benefit, 2),
        "notes": ["Tax calculation is indicative and excludes VAT, STT, and other potential taxes."]
    }


# --- Main Orchestrator ---

def run_rollover_planner(inputs: RolloverPlannerInput):
    """
    Orchestrates the rollover relief planning process.
    1. Checks eligibility based on the selected section.
    2. Calculates the tax impact with and without relief.
    """
    eligibility_result = check_eligibility(inputs)
    tax_result = calculate_tax_impact(inputs, eligibility_result['eligible'])

    return {
        "eligibility": eligibility_result,
        "tax_comparison": tax_result
    }
