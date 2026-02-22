import requests
import pandas as pd


class EconomicConnector:
    def __init__(self):
        self.base_url = "https://api.worldbank.org/v2"

    def get_indicator_data(self, country_code, indicator, date_range="2000:2023"):
        """
        Fetches indicator data from World Bank.
        Example indicators:
        NY.GDP.MKTP.CD (GDP current USD)
        SP.POP.TOTL (Population total)
        FP.CPI.TOTL.ZG (Inflation, consumer prices annual %)
        """
        url = f"{self.base_url}/country/{country_code}/indicator/{indicator}"
        params = {"format": "json", "date": date_range, "per_page": 1000}

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if len(data) < 2 or not data[1]:
                return pd.DataFrame()

            # Flatten the JSON
            records = []
            for item in data[1]:
                records.append(
                    {
                        "date": item["date"],
                        "value": item["value"],
                        "indicator": item["indicator"]["value"],
                        "country": item["country"]["value"],
                    }
                )

            df = pd.DataFrame(records)
            df["date"] = df["date"].astype(int)
            df = df.sort_values("date")
            return df
        except Exception as e:
            print(f"Error fetching economic data: {e}")
            return pd.DataFrame()

    def list_common_indicators(self):
        return {
            "GDP (Current USD)": "NY.GDP.MKTP.CD",
            "Population": "SP.POP.TOTL",
            "Inflation (CPI %)": "FP.CPI.TOTL.ZG",
            "Unemployment (%)": "SL.UEM.TOTL.ZS",
            "CO2 Emissions": "EN.ATM.CO2E.KT",
        }
