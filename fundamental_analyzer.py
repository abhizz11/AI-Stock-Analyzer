# fundamental_analyzer.py

import yfinance as yf
import pandas as pd
import ollama
import re  # <<< NEW: Import the regular expression library
from verification_prints import print_fundamental_ratios, print_dcf_inputs


class FundamentalAnalyzer:
    def __init__(self, ticker_symbol, model_name='llama3:8b-instruct-q4_0'):
        print("Initializing Fundamental Analyzer...")
        self.ticker = yf.Ticker(ticker_symbol)
        self.info = self.ticker.info
        self.financials = self.ticker.financials
        self.balance_sheet = self.ticker.balance_sheet
        self.cash_flow = self.ticker.cashflow
        self.model = model_name
        print("Fundamental data loaded.")
        try:
            tnx_info = yf.Ticker('^TNX').history(period='5d', interval='1d')
            self.risk_free_rate = tnx_info['Close'].iloc[-1] / 100
        except Exception:
            print("Warning: Could not fetch 10-Year Treasury yield. Using default 3.5%.")
            self.risk_free_rate = 0.035

    def get_key_ratios(self):
        """
        <<< FIXED: This function is now fully implemented. >>>
        Calculates and PRINTS a comprehensive suite of financial ratios.
        """
        print("Calculating and Verifying Key Financial Ratios...")
        ratios = {}

        # --- Profitability, Liquidity, Solvency, Valuation Ratios ---
        ratios['Profit Margin'] = (self.info.get(
            'profitMargins', 0), "Measures how much profit is generated for every dollar of revenue. Higher is better.")
        ratios['Return on Equity (ROE)'] = (self.info.get(
            'returnOnEquity', 0), "Measures how effectively the company uses shareholder money to generate profit. Consistently high ROE is a great sign.")
        ratios['Current Ratio'] = (self.info.get(
            'currentRatio', 0), "Compares current assets to current liabilities. A ratio > 1 suggests good short-term financial health.")
        ratios['Debt to Equity Ratio'] = (self.info.get(
            'debtToEquity', 0), "Measures the company's debt relative to its shareholder equity. A high ratio can signal risk.")
        ratios['Price-to-Earnings (P/E) Ratio'] = (self.info.get('trailingPE', 0),
                                                   "Tells you how much investors are willing to pay for each dollar of earnings. Compare to industry average.")
        ratios['Price-to-Book (P/B) Ratio'] = (self.info.get('priceToBook', 0),
                                               "Compares the company's market price to its 'book value'. A low P/B can indicate a value stock.")
        ratios['Price/Earnings-to-Growth (PEG) Ratio'] = (self.info.get(
            'pegRatio', 0), "A P/E ratio adjusted for growth. A PEG around 1 is often considered fairly valued for a growth stock.")

        print_fundamental_ratios(ratios)
        return ratios

    def _get_industry_growth_rate(self):
        """
        <<< FIXED: This function now uses regular expressions for robust parsing. >>>
        Uses the LLM to estimate a 5-year forward CAGR for the company's industry.
        """
        industry = self.info.get('industry', 'general')
        print(
            f"\nQuerying LLM for 5-year growth rate estimate for the '{industry}' industry...")

        prompt = f"""
        Act as a senior equity research analyst specializing in industry forecasting. Based on current market trends and data as of mid-2025, what is a reasonable 5-year forward Compound Annual Growth Rate (CAGR) estimate for the '{industry}' industry?

        Provide ONLY the numerical percentage in your response, without the '%' sign. Your response should contain only one number. For example: 15.5
        """
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}]
            )
            response_text = response['message']['content'].strip()

            # Use regex to find the last number in the string (float or integer)
            # This is much more robust than float(response_text)
            matches = re.findall(r"[-+]?\d*\.\d+|\d+", response_text)

            if matches:
                growth_str = matches[-1]  # Take the last number found
                growth_rate = float(growth_str) / 100
                print(f"LLM estimated growth rate: {growth_rate:.2%}")
                return growth_rate
            else:
                raise ValueError("No number found in LLM response")

        except (ValueError, KeyError, IndexError) as e:
            print(
                f"Warning: Could not parse LLM growth rate response ('{response_text}'). Error: {e}")
            print("Falling back to historical FCF growth rate for the 5-year forecast.")
            return self.cash_flow.loc['Free Cash Flow'].pct_change().mean()

    def _calculate_wacc(self):
        # This function was correct and does not need changes
        # ... (full code for this function remains here)
        # --- Cost of Equity (using CAPM model) ---
        # Default to 1.0 if beta is not available
        beta = self.info.get('beta', 1.0)
        market_return = 0.08  # Assumed long-term market return
        equity_risk_premium = market_return - self.risk_free_rate
        cost_of_equity = self.risk_free_rate + beta * equity_risk_premium

        # --- Cost of Debt ---
        try:
            interest_expense = self.financials.loc['Interest Expense'].iloc[0]
            total_debt = self.info.get('totalDebt', 0)
            cost_of_debt_pre_tax = interest_expense / total_debt if total_debt > 0 else 0
            income_before_tax = self.financials.loc['Income Before Tax'].iloc[0]
            tax_expense = self.financials.loc['Income Tax Expense'].iloc[0]
            # Default to 21% if not calculable
            tax_rate = tax_expense / income_before_tax if income_before_tax > 0 else 0.21
            cost_of_debt_after_tax = cost_of_debt_pre_tax * (1 - tax_rate)
        except Exception:
            tax_rate = 0.21
            # Assume a 4% pre-tax cost of debt
            cost_of_debt_after_tax = 0.04 * (1 - tax_rate)
            print(
                "Warning: Could not calculate cost of debt from financials. Using default values.")

        # --- WACC Calculation ---
        market_cap = self.info.get('marketCap', 0)
        total_debt = self.info.get('totalDebt', 0)
        total_value = market_cap + total_debt
        weight_of_equity = market_cap / total_value if total_value > 0 else 1
        weight_of_debt = total_debt / total_value if total_value > 0 else 0
        wacc = (weight_of_equity * cost_of_equity) + \
            (weight_of_debt * cost_of_debt_after_tax)
        wacc_inputs = {"risk_free_rate": self.risk_free_rate, "beta": beta, "equity_risk_premium": equity_risk_premium,
                       "cost_of_equity": cost_of_equity, "cost_of_debt": cost_of_debt_after_tax, "wacc": wacc}
        return wacc, wacc_inputs

    def perform_dcf_analysis(self):
        # This function was correct and does not need changes
        # ... (full code for this function remains here)
        print("\nPerforming and Verifying Multi-Stage Dynamic DCF Analysis...")
        try:
            five_year_growth_rate = self._get_industry_growth_rate()
            perpetual_growth_rate = min(self.risk_free_rate, 0.025)
            wacc, wacc_inputs = self._calculate_wacc()
            discount_rate = wacc
            fcf = self.cash_flow.loc['Free Cash Flow']
            last_fcf = fcf.iloc[0]
            shares_outstanding = self.info['sharesOutstanding']
            net_debt = self.info.get('totalDebt', 0) - \
                self.info.get('totalCash', 0)
            dcf_inputs = {**wacc_inputs, 'five_year_growth_rate': five_year_growth_rate, 'perpetual_growth_rate': perpetual_growth_rate,
                          'industry': self.info.get('industry', 'N/A'), 'fcf_history': fcf.to_frame(), 'shares_outstanding': shares_outstanding, 'net_debt': net_debt}
            print_dcf_inputs(dcf_inputs)
            projected_fcf = [
                last_fcf * ((1 + five_year_growth_rate) ** i) for i in range(1, 6)]
            discounted_fcf = [fcf / ((1 + discount_rate) ** (i+1))
                              for i, fcf in enumerate(projected_fcf)]
            terminal_value = (
                projected_fcf[-1] * (1 + perpetual_growth_rate)) / (discount_rate - perpetual_growth_rate)
            discounted_terminal_value = terminal_value / \
                ((1 + discount_rate) ** 5)
            total_enterprise_value = sum(
                discounted_fcf) + discounted_terminal_value
            equity_value = total_enterprise_value - net_debt
            dcf_fair_value_per_share = equity_value / shares_outstanding
            current_price = self.info['currentPrice']
            return {"DCF Fair Value per Share": dcf_fair_value_per_share, "Current Market Price": current_price, "Upside/Downside (%)": ((dcf_fair_value_per_share / current_price) - 1) * 100}
        except Exception as e:
            return {"Error": f"Could not perform DCF. Data might be missing or invalid. Error: {e}"}
