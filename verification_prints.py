# verification_prints.py

import pandas as pd


def print_header(title):
    # ... (no change here)
    print("\n" + "="*60)
    print(f"|    {title.upper():<50} |")
    print("="*60)


def print_fundamental_ratios(ratios):
    # ... (no change here)
    print_header("Verifiable Fundamental Ratios")
    for name, value in ratios.items():
        print(f"- {name:<30}: {value[0]:.4f}")
    print("\nACTION: Tally these ratios on Yahoo Finance (Statistics tab) or Google Finance.")

# <<< MODIFIED FUNCTION >>>


def print_dcf_inputs(dcf_inputs):
    """Prints the key inputs for the multi-stage DCF calculation."""
    print_header("Verifiable DCF Model Inputs & WACC Calculation")

    # --- WACC Components ---
    print("\n--- Weighted Average Cost of Capital (WACC) Inputs ---")
    print(
        f"- Risk-Free Rate (U.S. 10-Yr Treasury): {dcf_inputs['risk_free_rate']:.4%}")
    print(f"- Company Beta (Volatility vs. Market): {dcf_inputs['beta']:.4f}")
    print(
        f"- Cost of Equity (Calculated using CAPM): {dcf_inputs['cost_of_equity']:.4%}")
    print(f"- WACC (Calculated Discount Rate): {dcf_inputs['wacc']:.4%}")

    # --- Growth Rate Components (THE NEW PART) ---
    print("\n--- Multi-Stage Growth Rate Inputs ---")
    print(
        f"- Stage 1 Growth (Years 1-5): {dcf_inputs['five_year_growth_rate']:.2%}")
    print(
        f"  (Source: LLM-based analysis of the '{dcf_inputs['industry']}' industry)")
    print(
        f"- Stage 2 Growth (Perpetual): {dcf_inputs['perpetual_growth_rate']:.4%}")
    print(f"  (Source: Tied to U.S. 10-Year Treasury Yield for long-term stability)")

    # --- DCF Components ---
    print("\n--- Free Cash Flow & Other Data ---")
    with pd.option_context('display.float_format', '{:,.0f}'.format):
        print(dcf_inputs['fcf_history'])

    print(f"\n- Shares Outstanding: {dcf_inputs['shares_outstanding']:,}")
    print(f"- Net Debt (Total Debt - Cash): {dcf_inputs['net_debt']:,.0f}")


def print_technical_indicators(indicators):
    # ... (no change here)
    pass
