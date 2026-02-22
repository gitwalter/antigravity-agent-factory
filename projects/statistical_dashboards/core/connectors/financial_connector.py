import yfinance as yf
import pandas as pd


class FinancialConnector:
    def __init__(self):
        pass

    def get_ticker_data(self, ticker, period="1y", interval="1d"):
        """Fetches historical price data using yfinance."""
        try:
            yticker = yf.Ticker(ticker)
            df = yticker.history(period=period, interval=interval)
            if df.empty:
                return pd.DataFrame()

            # Reset index to make 'Date' a column
            df = df.reset_index()
            return df
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return pd.DataFrame()

    def get_ticker_info(self, ticker):
        """Fetches basic info about a company."""
        try:
            yticker = yf.Ticker(ticker)
            return yticker.info
        except Exception as e:
            print(f"Error fetching info for {ticker}: {e}")
            return {}
