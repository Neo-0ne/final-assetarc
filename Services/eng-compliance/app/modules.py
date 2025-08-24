"""
This file contains the logic for various compliance modules.
Each function will take an 'inputs' dictionary and return a result dictionary.
"""

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
