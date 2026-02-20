import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

st.set_page_config(
    page_title="Statistical Analysis Dashboard", page_icon="📈", layout="wide"
)

# Directory where CSV files are stored
DATA_DIR = "data"


@st.cache_data
def load_data(domain):
    """Loads CSV data based on the selected domain using caching."""
    file_map = {
        "Sales": "sales_data.csv",
        "Warehouse": "warehouse_data.csv",
        "Accounting": "accounting_data.csv",
        "Manufacturing": "manufacturing_data.csv",
    }
    file_path = os.path.join(DATA_DIR, file_map[domain])
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # Attempt to convert date strings to datetime objects
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"])
        return df
    else:
        return None


def main():
    st.title("📈 Statistical Analysis & Visualization Dashboard")
    st.markdown(
        "Select a business domain from the sidebar to begin analyzing the dataset."
    )

    # --- SIDEBAR ---
    st.sidebar.header("Configuration")
    domain_options = ["Sales", "Warehouse", "Accounting", "Manufacturing"]
    selected_domain = st.sidebar.selectbox("Select Business Domain", domain_options)

    st.sidebar.markdown("---")
    st.sidebar.info(
        "This is a template dashboard for statistical analysis. Live financial and agentic data will be added in future iterations."
    )

    # --- DATA LOADING ---
    df = load_data(selected_domain)

    if df is None:
        st.error(
            f"Data file for **{selected_domain}** not found. Please ensure `data_generator.py` has been run."
        )
        return

    # --- Data Overview Section ---
    st.header(f"{selected_domain} Data Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", f"{len(df):,}")
    col2.metric("Total Features", f"{len(df.columns)}")
    col3.metric("Missing Values", f"{df.isna().sum().sum()}")

    with st.expander("View Raw Data", expanded=False):
        st.dataframe(df, use_container_width=True)

    with st.expander("Data Types & Missing Values", expanded=False):
        info_df = pd.DataFrame(
            {
                "Data Type": df.dtypes,
                "Missing Values": df.isna().sum(),
                "Uniques": df.nunique(),
            }
        )
        st.dataframe(info_df, use_container_width=True)

    # --- Statistical Summary Section ---
    st.markdown("---")
    st.header("📊 Statistical Analysis")

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    if numeric_cols:
        st.subheader("Descriptive Statistics")
        selected_stats_cols = st.multiselect(
            "Select columns for statistical summary",
            numeric_cols,
            default=numeric_cols[: min(3, len(numeric_cols))],
        )

        if selected_stats_cols:
            stats_df = df[selected_stats_cols].describe().T
            # Adding variance mathematically
            stats_df["variance"] = df[selected_stats_cols].var()
            # Reorganize columns for display
            cols = list(stats_df.columns)
            cols.insert(3, cols.pop(-1))  # Move variance next to std
            st.dataframe(
                stats_df[cols].style.format("{:.2f}"), use_container_width=True
            )
    else:
        st.info("No numerical columns found for statistical summary.")

    # --- Visualization Section ---
    st.markdown("---")
    st.header("📈 Data Visualization")

    viz_col1, viz_col2 = st.columns(2)

    # Left Column: Distribution (Histograms)
    with viz_col1:
        st.subheader("Distribution Analysis")
        if numeric_cols:
            hist_col = st.selectbox(
                "Select variable for distribution (Histogram)", numeric_cols, key="hist"
            )
            fig_hist = px.histogram(
                df,
                x=hist_col,
                nbins=30,
                marginal="box",
                color_discrete_sequence=["#3366cc"],
            )
            fig_hist.update_layout(bargap=0.1)
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info("Need numerical data for histograms.")

    # Right Column: Categorical (Bar Charts)
    with viz_col2:
        st.subheader("Categorical Breakdown")
        if categorical_cols:
            # try to avoid high cardinality columns like IDs for bar charts
            valid_cat_cols = [
                c
                for c in categorical_cols
                if df[c].nunique() < 50 and df[c].nunique() > 1
            ]
            if valid_cat_cols:
                bar_col = st.selectbox(
                    "Select variable for counts (Bar Chart)", valid_cat_cols, key="bar"
                )
                counts = df[bar_col].value_counts().reset_index()
                counts.columns = [bar_col, "Count"]
                fig_bar = px.bar(counts, x=bar_col, y="Count", color=bar_col)
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info(
                    "No suitable low-cardinality categorical columns found for breakdown."
                )
        else:
            st.info("Need categorical data for bar charts.")

    # Cross-analysis (Scatter Plot)
    if len(numeric_cols) >= 2:
        st.subheader("Bivariate Analysis (Scatter Plot)")
        scatter_col1, scatter_col2, scatter_col3 = st.columns(3)
        with scatter_col1:
            x_var = st.selectbox("X-Axis", numeric_cols, index=0)
        with scatter_col2:
            y_var = st.selectbox("Y-Axis", numeric_cols, index=1)
        with scatter_col3:
            color_var = st.selectbox("Color By (Optional)", ["None"] + categorical_cols)

        color_arg = color_var if color_var != "None" else None

        # sample data if highly dense
        plot_df = df.sample(min(2000, len(df))) if len(df) > 2000 else df

        fig_scatter = px.scatter(
            plot_df, x=x_var, y=y_var, color=color_arg, hover_data=plot_df.columns[:3]
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Time Series (if Date column exists)
    if "Date" in df.columns and len(numeric_cols) > 0:
        st.markdown("---")
        st.subheader("Time Series Analysis")

        ts_y = st.selectbox(
            "Select variable to trend over Date", numeric_cols, key="ts_y"
        )

        # Aggregate by date
        ts_agg = df.groupby("Date")[ts_y].sum().reset_index()
        fig_ts = px.line(ts_agg, x="Date", y=ts_y, markers=True)

        # Add a rolling mean
        ts_agg["Rolling 7d Mean"] = ts_agg[ts_y].rolling(window=7).mean()
        fig_ts.add_scatter(
            x=ts_agg["Date"],
            y=ts_agg["Rolling 7d Mean"],
            mode="lines",
            name="7d Trend",
            line=dict(dash="dash", color="orange"),
        )

        st.plotly_chart(fig_ts, use_container_width=True)


if __name__ == "__main__":
    main()
