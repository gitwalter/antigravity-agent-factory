import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.metrics import r2_score, mean_squared_error
from scipy import stats


class AnalysisManager:
    """Handles advanced statistical modeling and predictions."""

    @staticmethod
    def run_linear_regression(df, x_col, y_col):
        """
        Performs a simple linear regression.
        Returns model details and coordinates for the regression line.
        """
        # Drop NaNs
        data = df[[x_col, y_col]].dropna()
        if data.empty:
            return None

        X = data[[x_col]].values
        y = data[y_col].values

        model = LinearRegression()
        model.fit(X, y)

        y_pred = model.predict(X)

        results = {
            "coefficient": model.coef_[0],
            "intercept": model.intercept_,
            "r2": r2_score(y, y_pred),
            "mse": mean_squared_error(y, y_pred),
            "x_range": X.flatten().tolist(),
            "y_pred": y_pred.tolist(),
        }

        return results

    @staticmethod
    def get_correlation_matrix(df):
        """Returns the correlation matrix for numeric columns."""
        numeric_df = df.select_dtypes(include=[np.number])
        return numeric_df.corr()

    @staticmethod
    def run_time_series_baseline(df, col, window=7):
        """
        Calculates simple moving averages and rolling volatility.
        """
        data = df[col].dropna()
        if data.empty:
            return None

        sma = data.rolling(window=window).mean()
        std = data.rolling(window=window).std()

        results = {
            "sma": sma,
            "rolling_std": std,
            "latest_sma": sma.iloc[-1] if not sma.empty else 0,
            "latest_std": std.iloc[-1] if not std.empty else 0,
        }
        return results

    @staticmethod
    def detect_outliers(df, col, method="iqr"):
        """
        Detects outliers using IQR or Z-score.
        """
        data = df[col].dropna()
        if data.empty:
            return []

        if method == "iqr":
            q1 = data.quantile(0.25)
            q3 = data.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers = data[(data < lower_bound) | (data > upper_bound)]
        else:
            z_scores = np.abs(stats.zscore(data))
            outliers = data[z_scores > 3]

        return outliers.index.tolist()

    @staticmethod
    def run_clustering(df, n_clusters=3):
        """
        Performs K-Means clustering on numeric columns.
        """
        numeric_df = df.select_dtypes(include=[np.number]).dropna()
        if len(numeric_df) < n_clusters:
            return None

        model = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = model.fit_predict(numeric_df)

        return clusters

    @staticmethod
    def run_hypothesis_test(group1, group2):
        """
        Performs a T-test between two groups.
        """
        t_stat, p_val = stats.ttest_ind(group1.dropna(), group2.dropna())
        return {"t_statistic": t_stat, "p_value": p_val, "significant": p_val < 0.05}

    @staticmethod
    def generate_ai_insight(module_type, results, context="General Analysis"):
        """
        Generates a text summary based on statistical results.
        Uses AIManager (Gemini) for real intelligent insights.
        """
        from core.ai_manager import AIManager

        ai = AIManager()

        # Prepare a descriptive string of the results for the LLM
        if isinstance(results, dict):
            # Clean up numpy types for JSON-like string
            serializable_results = {
                k: float(v) if isinstance(v, (np.float64, np.int64)) else v
                for k, v in results.items()
                if k not in ["x_range", "y_pred"]
            }
            data_summary = (
                f"Statistical results for {module_type}:\n{serializable_results}"
            )
        else:
            data_summary = f"Results for {module_type}: {results}"

        return ai.generate_insight(context, data_summary)

    @staticmethod
    def _generate_ai_insight_legacy(module_type, results):
        """
        Legacy mock logic (kept for reference or fallback).
        """
        if module_type == "regression":
            r2 = results.get("r2", 0)
            coef = results.get("coefficient", 0)
            strength = "strong" if r2 > 0.7 else "moderate" if r2 > 0.4 else "weak"
            direction = "positive" if coef > 0 else "negative"
            return (
                f"The model shows a **{strength} {direction} relationship** (R²={r2:.2f}). "
                f"For every unit increase in the independent variable, the target changes by approx. {coef:.2f}."
            )

        elif module_type == "time-series":
            latest_sma = results.get("latest_sma", 0)
            latest_std = results.get("latest_std", 0)
            return (
                f"The trend is currently stabilizing around a moving average of **{latest_sma:.2f}**. "
                f"The rolling volatility is **{latest_std:.2f}**, suggesting a {'high' if latest_std > 5 else 'stable'} market regime."
            )

        elif module_type == "hypothesis":
            p_val = results.get("p_value", 1.0)
            sig = (
                "is statistically significant"
                if p_val < 0.05
                else "is NOT statistically significant"
            )
            return (
                f"The difference between the groups **{sig}** (p-value: {p_val:.4f})."
            )

        return "Insight generation not configured for this module."
