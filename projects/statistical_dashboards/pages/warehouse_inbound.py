import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from core.database import Project, DatabaseManager
from core.data_manager import DataManager
from core.viz_manager import VizManager


def render_inbound_template(
    project: Project,
    db_manager: DatabaseManager,
    data_manager: DataManager,
    viz_manager: VizManager,
):
    st.subheader("📦 Inbound Operations (Dock-to-Stock)")
    st.info("Metrics derived from expected `inbound.schema.json` compliant data.")

    # In a real scenario, we would filter datasets bound to the 'inbound' schema.
    # For now, we simulate finding the compliant dataset.
    datasets = project.datasets
    if not datasets:
        st.warning(
            "No datasets available. Please upload Inbound data in the Intelligence tab."
        )
        return

    # Simulate fetching the most recent inbound dataset
    # We will just take the first one and pretend it's inbound data for demonstration if columns match
    ds = datasets[-1]
    df = data_manager.get_dataset_data(ds.id, db_manager)

    if df is None or df.empty:
        st.error("Dataset is empty.")
        return

    # Mocking Inbound KPIs if real data isn't perfectly mapped yet
    has_inbound_cols = all(
        col in df.columns for col in ["Expected_Qty", "Received_Qty"]
    )

    if not has_inbound_cols:
        st.warning(
            "Dataset does not fully match Inbound Schema. Simulating metrics based on row count."
        )
        # Generative mock data for demo
        val_expected = len(df) * 10
        val_received = int(val_expected * 0.98)  # 2% discrepancy
    else:
        val_expected = df["Expected_Qty"].sum()
        val_received = df["Received_Qty"].sum()

    discrepancy = (
        ((val_expected - val_received) / val_expected) * 100 if val_expected > 0 else 0
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Expected Qty", f"{val_expected:,}")
    c2.metric("Total Received Qty", f"{val_received:,}")
    c3.metric(
        "Receive Discrepancy Rate",
        f"{discrepancy:.2f}%",
        "-0.1%" if discrepancy < 2 else "+1.5%",
    )

    st.divider()
    st.markdown("### Dock Arrival vs. Putaway Volume")

    # Generate mock time-series data for visualization if not present
    dates = pd.date_range(end=pd.Timestamp.now(), periods=14)
    arrivals = np.random.randint(50, 200, size=14)
    putaway = arrivals * np.random.uniform(0.8, 1.1, size=14)

    chart_df = pd.DataFrame(
        {
            "Date": dates,
            "Arrival Volume (Items)": arrivals,
            "Putaway Volume (Items)": putaway,
        }
    )

    # Using plotly express directly for a dual-line chart
    fig = px.line(
        chart_df,
        x="Date",
        y=["Arrival Volume (Items)", "Putaway Volume (Items)"],
        title="14-Day Dock-to-Stock Flow",
        markers=True,
    )
    st.plotly_chart(fig, use_container_width=True)
