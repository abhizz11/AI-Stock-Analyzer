# technical_analyzer.py

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from verification_prints import print_technical_indicators  # Import our new function


class TechnicalAnalyzer:
    def __init__(self, ticker_symbol):
        print("Initializing Technical Analyzer...")
        self.data = yf.Ticker(ticker_symbol).history(period="5y")
        print("Technical data loaded.")

    def calculate_indicators(self):
        """Calculates and PRINTS a suite of advanced technical indicators."""
        print("Calculating and Verifying Technical Indicators...")

        # ... (all calculation logic remains the same)
        self.data['SMA50'] = self.data['Close'].rolling(window=50).mean()
        self.data['SMA200'] = self.data['Close'].rolling(window=200).mean()
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        self.data['RSI'] = 100 - (100 / (1 + rs))
        self.data['BB_Middle'] = self.data['Close'].rolling(window=20).mean()
        self.data['BB_Std'] = self.data['Close'].rolling(window=20).std()
        self.data['BB_Upper'] = self.data['BB_Middle'] + \
            (self.data['BB_Std'] * 2)
        self.data['BB_Lower'] = self.data['BB_Middle'] - \
            (self.data['BB_Std'] * 2)

        latest_indicators = self.data.iloc[-1]

        # <<< NEW: Call the verification printer >>>
        print_technical_indicators(latest_indicators)

        return latest_indicators

    def plot_charts(self):
        # ... (this function does not need to change)
        print("Generating technical charts... Please close plots to continue.")
        plt.figure(figsize=(15, 10))
        plt.subplot(2, 1, 1)
        plt.plot(self.data.index, self.data['Close'], label='Close Price')
        plt.plot(self.data.index,
                 self.data['SMA50'], label='50-Day SMA', linestyle='--')
        plt.plot(self.data.index,
                 self.data['SMA200'], label='200-Day SMA', linestyle='--')
        plt.plot(self.data.index, self.data['BB_Upper'],
                 label='Upper Bollinger Band', color='gray', alpha=0.5)
        plt.plot(self.data.index, self.data['BB_Lower'],
                 label='Lower Bollinger Band', color='gray', alpha=0.5)
        plt.fill_between(
            self.data.index, self.data['BB_Upper'], self.data['BB_Lower'], color='gray', alpha=0.1)
        plt.title('Price, Moving Averages, and Bollinger Bands')
        plt.legend()
        plt.subplot(2, 1, 2)
        plt.plot(self.data.index, self.data['RSI'], label='RSI')
        plt.axhline(70, linestyle='--', color='red', label='Overbought (70)')
        plt.axhline(30, linestyle='--', color='green', label='Oversold (30)')
        plt.title('Relative Strength Index (RSI)')
        plt.legend()
        plt.tight_layout()
        plt.show()
