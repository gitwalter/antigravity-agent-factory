import pandas as pd
import numpy as np


class BusinessManager:
    """
    Logic for domain-specific business analytics.
    Covers Warehousing (Amazon-scale), Logistics, CRM, and Sales.
    """

    @staticmethod
    def calculate_inventory_turnover(total_sales, avg_inventory):
        """Standard turnover ratio: Sales / Avg Inventory."""
        if avg_inventory == 0:
            return 0
        return total_sales / avg_inventory

    @staticmethod
    def calculate_bin_density(inventory_df, total_bins):
        """
        Calculates Bin Density (% of bins utilized).
        In Random Stow, high density is good until it hits the 'Pick Threshold'.
        """
        if total_bins <= 0:
            return 0
        utilized_bins = inventory_df["bin_id"].nunique()
        return (utilized_bins / total_bins) * 100

    @staticmethod
    def calculate_asn_accuracy(asn_items_df):
        """
        Calculates ASN Fill Rate (Received vs Expected).
        """
        if (
            "expected_quantity" not in asn_items_df.columns
            or "received_quantity" not in asn_items_df.columns
        ):
            return None

        expected = asn_items_df["expected_quantity"].sum()
        received = asn_items_df["received_quantity"].sum()

        return {
            "fill_rate_pct": (received / expected) * 100 if expected > 0 else 0,
            "variance_units": received - expected,
            "overages_count": (
                asn_items_df["received_quantity"] > asn_items_df["expected_quantity"]
            ).sum(),
        }

    @staticmethod
    def calculate_dock_to_stock(df, dock_time_col, stow_time_col):
        """
        Calculates Dock-to-Stock cycle time in hours.
        Amazon Target: < 2 hours.
        """
        if dock_time_col not in df.columns or stow_time_col not in df.columns:
            return None

        # Ensure datetime
        df[dock_time_col] = pd.to_datetime(df[dock_time_col])
        df[stow_time_col] = pd.to_datetime(df[stow_time_col])

        ref_diff = (df[stow_time_col] - df[dock_time_col]).dt.total_seconds() / 3600
        return {
            "avg_d2s_hours": ref_diff.mean(),
            "max_d2s_hours": ref_diff.max(),
            "target_met_pct": (ref_diff <= 2.0).mean() * 100,
        }

    @staticmethod
    def calculate_uph(df, start_col, end_col, units_col):
        """
        Calculates Units Per Hour (UPH / PPH).
        """
        if any(c not in df.columns for c in [start_col, end_col, units_col]):
            return None

        df[start_col] = pd.to_datetime(df[start_col])
        df[end_col] = pd.to_datetime(df[end_col])

        duration_hrs = (df[end_col] - df[start_col]).dt.total_seconds() / 3600
        duration_hrs = duration_hrs.replace(0, np.nan)  # Avoid div by zero

        uph = df[units_col] / duration_hrs
        return {
            "avg_uph": uph.mean(),
            "total_units": df[units_col].sum(),
            "high_performers_pct": (uph > uph.mean()).mean() * 100,
        }

    @staticmethod
    def calculate_lsr(df, promised_time_col, actual_ship_time_col):
        """
        Late Shipment Rate (LSR).
        Amazon Target: < 4%.
        """
        if (
            promised_time_col not in df.columns
            or actual_ship_time_col not in df.columns
        ):
            return None

        df[promised_time_col] = pd.to_datetime(df[promised_time_col])
        df[actual_ship_time_col] = pd.to_datetime(df[actual_ship_time_col])

        late = (df[actual_ship_time_col] > df[promised_time_col]).sum()
        total = len(df)
        return {
            "lsr_pct": (late / total) * 100 if total > 0 else 0,
            "late_orders": late,
            "on_time_orders": total - late,
        }

    @staticmethod
    def predict_needed_labor(expected_units, avg_uph):
        """
        Simple prognosis: How many associates are needed for the expected volume?
        """
        if avg_uph <= 0:
            return 0
        total_hours_needed = expected_units / avg_uph
        # Assuming an 8-hour shift
        associates_needed = np.ceil(total_hours_needed / 8)
        return {
            "total_hours_needed": total_hours_needed,
            "associates_needed": int(associates_needed),
            "headcount_gap": 0,  # Placeholder for actual vs needed
        }

    @staticmethod
    def get_crm_conversion_funnel(leads, opportunities, won_deals):
        """Returns conversion rates between stages."""
        leads_count = len(leads) if isinstance(leads, pd.Series) else leads
        opps_count = (
            len(opportunities)
            if isinstance(opportunities, pd.Series)
            else opportunities
        )
        won_count = len(won_deals) if isinstance(won_deals, pd.Series) else won_deals

        return {
            "leads_to_opps": (opps_count / leads_count) if leads_count > 0 else 0,
            "opps_to_won": (won_count / opps_count) if opps_count > 0 else 0,
            "total_conversion": (won_count / leads_count) if leads_count > 0 else 0,
        }
