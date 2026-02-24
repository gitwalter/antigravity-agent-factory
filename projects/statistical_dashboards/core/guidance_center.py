import pandas as pd


class GuidanceCenter:
    """
    Centralized repository for help content, KPI definitions, and statistical education.
    Implements Requirement R1.
    """

    @staticmethod
    def get_kpi_dictionary():
        """Returns a list of core KPIs with definitions and formulas."""
        return [
            {
                "KPI": "UPH (Units Per Hour)",
                "Domain": "Warehouse",
                "Definition": "The number of items processed (picked, stowed, or packed) by an associate in one hour.",
                "Formula": "Total Units / Total Active Hours",
                "Target": "> 80 (Site dependent)",
            },
            {
                "KPI": "LSR (Late Shipment Rate)",
                "Domain": "Logistics",
                "Definition": "The percentage of orders shipped after their promised ship date.",
                "Formula": "(Late Orders / Total Orders) * 100",
                "Target": "< 4.0%",
            },
            {
                "KPI": "Dock-to-Stock (D2S)",
                "Domain": "Warehouse",
                "Definition": "The time taken from the moment a trailer arrives at the dock until the items are available for sale.",
                "Formula": "Stow Time - Dock Arrival Time",
                "Target": "< 2.0 Hours",
            },
            {
                "KPI": "Inventory Turnover",
                "Domain": "Finance",
                "Definition": "Shows how many times a company has sold and replaced inventory during a specific period.",
                "Formula": "Cost of Goods Sold / Average Inventory",
                "Target": "High (indicates efficient management)",
            },
        ]

    @staticmethod
    def get_statistical_primer():
        """Returns introductory explanations for AI/ML concepts used in the dashboard."""
        return {
            "Linear Regression": {
                "Title": "Finding Relationships",
                "Explanation": "Linear regression tries to draw a straight line through your data to predict one value based on another. For example, 'If I increase shelf height by 1 foot, how much does stow speed decrease?'",
                "Key Metric": "R-Squared (0 to 1): Close to 1 means the line fits the data very well. Below 0.3 means the relationship is weak.",
            },
            "K-Means Clustering": {
                "Title": "Grouping Like Items",
                "Explanation": "Clustering looks at your data and finds 'natural' groups based on similarities. It's like sorting a bowl of mixed fruit into piles of apples, oranges, and bananas without being told what they are.",
                "Use Case": "Identifying different types of customers or high-risk inventory zones.",
            },
            "Hypothesis Testing (T-Test)": {
                "Title": "Is the Difference Real?",
                "Explanation": "A T-Test checks if the difference between two groups (e.g., Team A vs Team B) is likely due to chance or if it's statistically significant.",
                "Key Metric": "P-Value: If it's less than 0.05, there's a 95% chance the difference is real and not just luck.",
            },
        }

    @staticmethod
    def get_dashboard_blueprints():
        """Returns structured layouts for different analysis types."""
        return {
            "Warehouse Efficiency": [
                "1. Metrics Row: UPH, D2S, ASN Accuracy",
                "2. Trend Chart: Hourly UPH throughout the shift",
                "3. Regression: Shelf Height vs Process Time",
                "4. Anomaly Table: Top 5 outliers in productivity",
            ],
            "Financial Health": [
                "1. Metrics Row: Cash on Hand, Burn Rate, Runway",
                "2. Line Chart: Revenue vs Expenses (6 months)",
                "3. Correlation Heatmap: Marketing Spend vs New Leads",
                "4. Forecast: Predictive 3-month cash flow",
            ],
        }
