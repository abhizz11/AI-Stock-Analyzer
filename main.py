from fundamental_analyzer import FundamentalAnalyzer
from technical_analyzer import TechnicalAnalyzer
from context_analyzer import ContextAnalyzer
from reporting import ReportGenerator


def main():
    TICKER = input(
        "Enter the stock ticker you want to analyze (e.g., AAPL, GOOGL): ").upper()

    # --- PILLAR 1: FUNDAMENTALS ---
    f_analyzer = FundamentalAnalyzer(TICKER)
    fundamental_ratios = f_analyzer.get_key_ratios()
    dcf_results = f_analyzer.perform_dcf_analysis()

    # --- PILLAR 2: TECHNICALS ---
    t_analyzer = TechnicalAnalyzer(TICKER)
    latest_indicators = t_analyzer.calculate_indicators()
    t_analyzer.plot_charts()  # This will pause execution until plots are closed

    # --- PILLAR 3: CONTEXT ---
    c_analyzer = ContextAnalyzer()
    sector = f_analyzer.info.get('sector', 'N/A')
    industry = f_analyzer.info.get('industry', 'N/A')
    context_analysis = c_analyzer.analyze_macro_and_industry(
        TICKER, sector, industry)

    # --- PILLAR 4: REPORTING ---
    reporter = ReportGenerator()
    investment_memo = reporter.generate_investment_memo(
        TICKER,
        fundamental_ratios,
        dcf_results,
        latest_indicators,
        context_analysis
    )

    print("\n\n" + "="*50)
    print(f"      COMPREHENSIVE INVESTMENT MEMO FOR {TICKER}")
    print("="*50 + "\n")
    print(investment_memo)

    # Save the memo to a file
    with open(f"{TICKER}_investment_memo.txt", "w") as f:
        f.write(investment_memo)
    print(f"\nMemo saved to {TICKER}_investment_memo.txt")


if __name__ == '__main__':
    main()
