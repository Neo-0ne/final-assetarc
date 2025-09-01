import math
from pydantic import BaseModel, Field

class InsuranceWrapperInput(BaseModel):
    investment_amount: float = Field(..., gt=0, description="The principal investment amount.")
    investment_period_years: int = Field(..., gt=0, description="The investment period in years.")
    annual_growth_rate: float = Field(..., gt=0, lt=1, description="The expected annual growth rate (e.g., 0.08 for 8%).")
    investor_type: str = Field(..., pattern="^(individual|company|trust)$", description="The type of investor.")

TAX_RATES = {
    'individual': {
        'cgt_rate': 0.18,  # 40% inclusion * 45% marginal
        'interest_rate': 0.45,
        'dividend_rate': 0.20,
    },
    'company': {
        'cgt_rate': 0.224, # 80% inclusion * 28% corporate rate
        'interest_rate': 0.28,
        'dividend_rate': 0.0, # Dividends are exempt for companies
    },
    'trust': {
        'cgt_rate': 0.36, # 80% inclusion * 45% trust rate
        'interest_rate': 0.45,
        'dividend_rate': 0.20,
    }
}

# Assumed portfolio composition for unwrapped investment
PORTFOLIO_COMPOSITION = {
    'interest': 0.40,
    'equity_growth': 0.40,
    'dividends': 0.20,
}

def calculate_wrapper_benefit(inputs: InsuranceWrapperInput):
    """
    Calculates the potential tax benefit of using an insurance wrapper for an investment.

    Args:
        inputs (InsuranceWrapperInput): Pydantic model containing the validated input data.

    Returns:
        dict: A dictionary containing the detailed calculation results.
    """
    # --- 1. Calculate Total Growth ---
    future_value = inputs.investment_amount * math.pow((1 + inputs.annual_growth_rate), inputs.investment_period_years)
    total_growth = future_value - inputs.investment_amount

    # --- 2. Calculate Tax for "Unwrapped" (Direct) Investment ---
    rates = TAX_RATES[inputs.investor_type]

    # Distribute total growth according to portfolio composition
    interest_component = total_growth * PORTFOLIO_COMPOSITION['interest']
    capital_gains_component = total_growth * PORTFOLIO_COMPOSITION['equity_growth']
    dividend_component = total_growth * PORTFOLIO_COMPOSITION['dividends']

    # Calculate tax on each component
    tax_on_interest = interest_component * rates['interest_rate']
    tax_on_capital_gains = capital_gains_component * rates['cgt_rate']
    tax_on_dividends = dividend_component * rates['dividend_rate']

    total_unwrapped_tax = tax_on_interest + tax_on_capital_gains + tax_on_dividends
    net_return_unwrapped = total_growth - total_unwrapped_tax

    # --- 3. Calculate Tax for "Wrapped" (Insurance) Investment ---
    # In a wrapper, all growth is taxed as a capital gain upon withdrawal.
    total_wrapped_tax = total_growth * rates['cgt_rate']
    net_return_wrapped = total_growth - total_wrapped_tax

    # --- 4. Calculate Benefit ---
    tax_saving = total_unwrapped_tax - total_wrapped_tax

    return {
        "inputs": inputs.model_dump(),
        "results": {
            "total_growth": round(total_growth, 2),
            "unwrapped_investment": {
                "total_tax": round(total_unwrapped_tax, 2),
                "net_return": round(net_return_unwrapped, 2),
                "tax_details": {
                    "tax_on_interest": round(tax_on_interest, 2),
                    "tax_on_capital_gains": round(tax_on_capital_gains, 2),
                    "tax_on_dividends": round(tax_on_dividends, 2),
                }
            },
            "wrapped_investment": {
                "total_tax": round(total_wrapped_tax, 2),
                "net_return": round(net_return_wrapped, 2),
            },
            "summary": {
                "tax_saving_with_wrapper": round(tax_saving, 2),
                "final_net_benefit": round(net_return_wrapped - net_return_unwrapped, 2)
            }
        }
    }
