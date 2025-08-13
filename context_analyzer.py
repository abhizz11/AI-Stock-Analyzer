import ollama


class ContextAnalyzer:
    def __init__(self, model_name='llama3:8b-instruct-q4_0'):
        self.model = model_name

    def analyze_macro_and_industry(self, ticker_symbol, company_sector, company_industry):
        print("Analyzing Macroeconomic and Industry Context with LLM...")
        prompt = f"""
        Act as a macroeconomic strategist. For a company like {ticker_symbol}, which is in the '{company_sector}' sector and '{company_industry}' industry, analyze the following:

        1.  **Current Macroeconomic Headwinds/Tailwinds:** Discuss the potential impact of current inflation rates, interest rate policies by the Fed, and overall GDP growth expectations on this company.
        2.  **Industry-Specific Trends:** What are the 1-3 most significant trends in the '{company_industry}' industry right now (e.g., AI adoption, supply chain issues, regulatory changes)?
        3.  **Competitive Landscape:** Who are the top 2-3 direct competitors? Briefly state their main competitive advantage against {ticker_symbol}.

        Provide a concise summary for each of the three points.
        """
        response = ollama.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']
