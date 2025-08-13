# reporting.py

import ollama


class ReportGenerator:
    def __init__(self, model_name='llama3:8b-instruct-q4_0'):
        self.model = model_name

    def generate_investment_memo(self, ticker, fundamental_ratios, dcf_results, tech_indicators, context_analysis):
        print("Generating Final Investment Memo with LLM...")

        # <<< FIXED: Add a check to handle if fundamental_ratios is None >>>
        if fundamental_ratios:
            ratio_details = "\n".join(
                [f"- **{name}**: {value[0]:.2f} ({value[1]})" for name, value in fundamental_ratios.items()])
        else:
            ratio_details = "Fundamental ratio data was not available."

        dcf_summary = f"The DCF model estimates a fair value of ${dcf_results.get('DCF Fair Value per Share', 0):.2f}, suggesting a potential upside/downside of {dcf_results.get('Upside/Downside (%)', 0):.2f}% from the current price of ${dcf_results.get('Current Market Price', 0):.2f}."
        tech_summary = f"The current RSI is {tech_indicators.get('RSI', 0):.2f}. The price is trading relative to its 50-day SMA and 200-day SMA."

        # The rest of the prompt remains the same
        prompt = f"""
        **INVESTMENT MEMORANDUM**

        **SUBJECT: Comprehensive Analysis of {ticker}**

        **1. EXECUTIVE SUMMARY**
        Act as a world-class portfolio manager. Synthesize all the following information into a concise executive summary. State your final investment thesis: Is this a Buy, Hold, or Sell at the current price? Justify your reasoning with the most critical data points from the analysis.

        **2. DEEP FUNDAMENTAL ANALYSIS**
        * **Financial Ratios:**
            {ratio_details}
        * **Interpretation:** Based on these ratios, what is the overall picture of the company's profitability, financial health, and current valuation?

        **3. VALUATION ANALYSIS**
        * **Discounted Cash Flow (DCF) Result:** {dcf_summary}
        * **Interpretation:** How much weight should be given to this DCF result? What are its key assumptions (like growth and discount rates)?

        **4. TECHNICAL & QUANTITATIVE ANALYSIS**
        * **Current Indicator State:** {tech_summary}
        * **Interpretation:** What is the current market sentiment based on these technical signals? Is it indicating a potential entry point or a time for caution?

        **5. MACROECONOMIC & INDUSTRY CONTEXT**
        * **Analyst Summary:**
            {context_analysis}
        * **Interpretation:** How do the broader economic and industry factors support or contradict a potential investment in {ticker}?

        **6. FINAL SWOT ANALYSIS & RECOMMENDATION**
        - **Strengths:** (Based on everything above)
        - **Weaknesses:** (Based on everything above)
        - **Opportunities:** (Based on everything above)
        - **Threats:** (Based on everything above)

        Conclude with your final, data-backed recommendation.
        """

        response = ollama.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']
