from core.database import DatabaseManager
from core.connectors.financial_connector import FinancialConnector
from core.connectors.economic_connector import EconomicConnector
from core.data_manager import DataManager
import pandas as pd


def test_logic_flow():
    print("--- 🔬 Starting Statistical Logic Test ---")

    # 1. Test Database
    print("\n1. Testing DatabaseManager...")
    db = DatabaseManager("projects/statistical_dashboards/data/test_dash.db")
    print("✅ Database initialized.")

    # 2. Test Financial Connector
    print("\n2. Testing FinancialConnector (AAPL)...")
    fin = FinancialConnector()
    df_fin = fin.get_ticker_data("AAPL", period="1mo")
    if not df_fin.empty:
        print(f"✅ Received {len(df_fin)} rows of financial data.")
        print(df_fin.head(2))
    else:
        print("❌ Financial data fetch failed.")

    # 3. Test Economic Connector
    print("\n3. Testing EconomicConnector (USA GDP)...")
    eco = EconomicConnector()
    df_eco = eco.get_indicator_data("USA", "NY.GDP.MKTP.CD", "2020:2022")
    if not df_eco.empty:
        print(f"✅ Received {len(df_eco)} rows of economic data.")
        print(df_eco)
    else:
        print("❌ Economic data fetch failed.")

    # 4. Test Data Processing
    print("\n4. Testing DataManager (Synthetic EDA)...")
    data = DataManager("projects/statistical_dashboards/data/test_store")
    synthetic_df = pd.DataFrame(
        {"day": range(10), "score": [i * 1.5 for i in range(10)]}
    )
    cleaned = data.clean_data(synthetic_df)
    print(f"✅ Data cleaned. Rows: {len(cleaned)}")

    print("\n--- 🏁 Logic Test Complete ---")


if __name__ == "__main__":
    test_logic_flow()
