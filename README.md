# AI-Stock-Analyzer
This project is a comprehensive stock analysis tool that combines traditional quantitative analysis with modern Large Language Model (LLM) based qualitative insights. It automatically fetches financial data, calculates key metrics, analyzes the broader context, and generates a detailed investment memorandum for any given stock ticker..

The script's workflow is divided into four distinct modules, each representing a pillar of modern investment analysis.

Pillar 1: Fundamental Analysis (fundamental_analyzer.py)
Calculates key financial ratios (like P/E, P/B, Debt-to-Equity).
Performs a multi-stage Discounted Cash Flow (DCF) valuation to estimate the intrinsic value per share.

Pillar 2: Technical Analysis (technical_analyzer.py)
Fetches historical price data.
Calculates major technical indicators like the Relative Strength Index (RSI), Simple Moving Averages (SMA50, SMA200), and Bollinger Bands.
Generates plots to visualize price action and indicator levels.

Pillar 3: Contextual Analysis (context_analyzer.py)
Uses a local LLM (via Ollama) to analyze the qualitative aspects of the investment.
Provides insights on macroeconomic headwinds/tailwinds (inflation, interest rates), industry-specific trends, and the competitive landscape.

Pillar 4: AI-Powered Reporting (reporting.py)
The final pillar synthesizes all the quantitative and qualitative data from the first three pillars.
It prompts an LLM to act as a portfolio manager, creating a structured, comprehensive investment memo that includes an executive summary, a SWOT analysis, and a final "Buy/Hold/Sell" recommendation.


Features:
Automated Data Gathering: Pulls data from yfinance.
Quantitative & Qualitative: Merges hard numbers (ratios, DCF) with soft analysis (macro trends, competition).
LLM Integration: Leverages a local LLM (llama3:8b) for nuanced analysis and report generation, ensuring privacy and no API costs.
Interactive Charts: Displays key technical charts for visual analysis.
Verifiable Inputs: Prints the key inputs used in the DCF model for transparency and verification.
Comprehensive Output: Generates a ready-to-read investment memo and saves it as a .txt file.

Prerequisites and Setup.
1. Clone the Repository
git clone https://github.com/abhizz11/AI-Stock-Analyzer.git
cd AI-Stock-Analyzer

2. Setup a virtual environment and install dependencies.
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install yfinance pandas matplotlib ollama

3. Install and setup Ollama
Download Ollama from official website: https://ollama.com/
Once ollama is running, pull: 
ollama run llama3:8b-instruct-q4_0


How to Use:
1. Run the Main Script
python main.py

2. Enter a ticker like 'NVDA'

3. View Technical Charts. The charts must be closed for the analysis to continue.

4. Get the Final report. {TICKER}_investment_memo.txt in the same directory. 


Project Structure:
.
├── main.py                  # Main entry point to run the analysis workflow.
├── fundamental_analyzer.py  # Handles ratio calculations and DCF analysis.
├── technical_analyzer.py    # Handles technical indicator calculations and plotting.
├── context_analyzer.py      # Uses LLM to analyze macro and industry context.
├── reporting.py             # Uses LLM to synthesize all data into a final memo.
└── verification_prints.py   # Helper functions to print verifiable model inputs.


!!!Disclaimer!!!
This tool is for educational and informational purposes only. It is not financial advice. 
The analyses and recommendations generated are based on publicly available data and automated models, 
which may contain errors or inaccuracies. Always conduct your own thorough research and consult with a qualified financial advisor before making any investment decisions.
