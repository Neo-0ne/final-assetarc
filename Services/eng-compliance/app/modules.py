"""
This file contains the logic for various compliance modules.
Each function will take an 'inputs' dictionary and return a result dictionary.
"""
from pydantic import ValidationError
from .bbee import OwnershipStructure, calculate_ownership_scorecard
from .estate_calculator import EstateInput, calculate_estate_duty
from .insurance_wrapper_calculator import InsuranceWrapperInput, calculate_wrapper_benefit

def run_insurance_wrapper_check(inputs: dict) -> dict:
    """
    Parses investment data and runs the Insurance Wrapper Benefit calculator.
    """
    try:
        wrapper_input = InsuranceWrapperInput(**inputs)
        calculation = calculate_wrapper_benefit(wrapper_input)
        return {
            "status": "completed",
            "summary": f"Potential tax saving with wrapper: ZAR {calculation['results']['summary']['tax_saving_with_wrapper']:,.2f}",
            "details": calculation
        }
    except ValidationError as e:
        return {"status": "error", "summary": "Input data is invalid.", "details": e.errors()}
    except Exception as e:
        return {"status": "error", "summary": "An unexpected error occurred.", "details": str(e)}

def run_estate_duty_check(inputs: dict) -> dict:
    """
    Parses asset data and runs the Estate Duty calculator.
    """
    try:
        estate_input = EstateInput(**inputs)
        calculation = calculate_estate_duty(estate_input)
        return {
            "status": "completed",
            "summary": f"Potential savings with structuring: ZAR {calculation['summary']['total_savings']:,.2f}",
            "details": calculation
        }
    except ValidationError as e:
        return {"status": "error", "summary": "Input data is invalid.", "details": e.errors()}
    except Exception as e:
        return {"status": "error", "summary": "An unexpected error occurred.", "details": str(e)}

def run_succession_check(inputs: dict) -> dict:
    """
    Provides recommendations for succession planning based on user inputs.
    """
    recommendations = []
    has_partners = inputs.get('has_partners', False)
    has_buy_sell = inputs.get('has_buy_sell', False)

    if has_partners:
        if not has_buy_sell:
            recommendations.append({
                "id": "REC001",
                "title": "Create a Buy-Sell Agreement",
                "text": "You have business partners but no Buy-Sell Agreement. This is a significant risk. A Buy-Sell agreement ensures a smooth transition of ownership and prevents disputes if a partner exits."
            })
            recommendations.append({
                "id": "REC002",
                "title": "Consider Key Person Insurance",
                "text": "Key Person Insurance can provide the necessary funds for the remaining partners to buy out a departing partner's shares, preventing a liquidity crisis."
            })
        else:
            recommendations.append({
                "id": "REC003",
                "title": "Review Your Buy-Sell Agreement",
                "text": "It's great that you have a Buy-Sell Agreement. Ensure it is reviewed annually and that any associated insurance policies are up to date."
            })
    else:
        recommendations.append({
            "id": "REC004",
            "title": "Document Your Succession Plan",
            "text": "Even without partners, it's crucial to have a clear succession plan. This should be documented in your will and in your company's governance documents (e.g., MOI)."
        })

    return {
        "status": "completed",
        "summary": f"Found {len(recommendations)} succession planning recommendations.",
        "details": {"recommendations": recommendations}
    }


def run_bbee_scorecard_check(inputs: dict) -> dict:
    """
    Parses ownership data and runs the B-BBEE scorecard calculator.
    """
    try:
        # Validate the input data using the Pydantic model
        ownership_structure = OwnershipStructure(**inputs)

        # Run the calculation
        scorecard = calculate_ownership_scorecard(ownership_structure)

        return {
            "status": "completed",
            "summary": f"B-BBEE Ownership Score: {scorecard['total_ownership_points']} points.",
            "details": scorecard
        }

    except ValidationError as e:
        # Return a structured error if input validation fails
        return {
            "status": "error",
            "summary": "Input data is invalid.",
            "details": e.errors()
        }
    except Exception as e:
        # Catch any other unexpected errors during calculation
        return {
            "status": "error",
            "summary": "An unexpected error occurred during calculation.",
            "details": str(e)
        }

def run_s42_47_check(inputs: dict) -> dict:
    """
    Performs a simplified Solvency and Liquidity test as per the Companies Act.

    In a real-world application, this would be far more complex and would
    involve detailed financial statement analysis.

    Required inputs:
    - total_assets: Fair value of the company's total assets.
    - total_liabilities: Fair value of the company's total liabilities.
    - current_assets: Value of assets that can be converted to cash within 12 months.
    - current_liabilities: Value of liabilities due within the next 12 months.
    """

    # --- Input Validation ---
    required_fields = ['total_assets', 'total_liabilities', 'current_assets', 'current_liabilities']
    if not all(field in inputs for field in required_fields):
        return {
            "result": "fail",
            "reason": f"Missing required financial data. Required fields are: {', '.join(required_fields)}",
            "details": {}
        }

    try:
        total_assets = float(inputs['total_assets'])
        total_liabilities = float(inputs['total_liabilities'])
        current_assets = float(inputs['current_assets'])
        current_liabilities = float(inputs['current_liabilities'])
    except (ValueError, TypeError):
        return {
            "result": "fail",
            "reason": "Invalid financial data. All inputs must be numbers.",
            "details": {}
        }

    # --- Rule 1: Solvency Test (Assets > Liabilities) ---
    solvency_passed = total_assets > total_liabilities

    # --- Rule 2: Liquidity Test (Company can pay debts as they become due) ---
    # This is a simplified check. A real test would be more nuanced.
    # We'll use a simple current ratio check (Current Assets / Current Liabilities)
    # A ratio > 1 is generally considered healthy.
    liquidity_passed = False
    if current_liabilities > 0:
        current_ratio = current_assets / current_liabilities
        liquidity_passed = current_ratio > 1
    elif current_assets > 0:
        # No current liabilities, so liquidity is fine.
        liquidity_passed = True

    # --- Final Result ---
    if solvency_passed and liquidity_passed:
        return {
            "result": "pass",
            "reason": "The company appears to satisfy the Solvency and Liquidity test.",
            "details": {
                "solvency_test": "passed",
                "liquidity_test": "passed",
                "asset_surplus": total_assets - total_liabilities,
                "current_ratio": current_ratio if 'current_ratio' in locals() else 'N/A'
            }
        }
    else:
        failures = []
        if not solvency_passed:
            failures.append("Solvency test failed: Total assets do not fairly value exceed total liabilities.")
        if not liquidity_passed:
            failures.append("Liquidity test failed: The company may be unable to pay its debts as they become due in the ordinary course of business.")

        return {
            "result": "fail",
            "reason": "The company does not appear to satisfy the Solvency and Liquidity test.",
            "details": {
                "solvency_test": "passed" if solvency_passed else "failed",
                "liquidity_test": "passed" if liquidity_passed else "failed",
                "failures": failures
            }
        }
