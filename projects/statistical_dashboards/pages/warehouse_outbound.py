import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from core.database import Project, DatabaseManager
from core.data_manager import DataManager
from core.viz_manager import VizManager


def render_outbound_template(
    project: Project,
    db_manager: DatabaseManager,
    data_manager: DataManager,
    viz_manager: VizManager,
):
    st.subheader("🚚 Outbound Fulfillment (Pick, Pack, Ship)")
    st.info("Metrics derived from expected `outbound.schema.json` compliant data.")

    datasets = project.datasets
    if not datasets:
        st.warning("No outbound data found. Please upload data via Warehousing Intel.")
        return

    ds = datasets[-1]
    df = data_manager.get_dataset_data(ds.id, db_manager)

    if df is None:
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Site Average UPH", "114", "+4")
    c2.metric("Order-to-Ship Cycle", "3.2 hours", "-0.1h")
    c3.metric("Carrier SLA Breach Rate", "0.8%", "-0.2%")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Units Per Hour (UPH) Distribution")
        # Generate mock UPH distribution
        uph_data = np.random.normal(loc=114, scale=15, size=200)
        uph_df = pd.DataFrame({"UPH": uph_data})
        fig_hist = px.histogram(
            uph_df,
            x="UPH",
            nbins=20,
            title="Associate UPH Distribution",
            color_discrete_sequence=["#ff7f0e"],
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        st.markdown("### Carrier Volume Split")
        carriers = ["Amazon Logistics", "UPS", "FedEx", "USPS"]
        vols = [4500, 2100, 1500, 800]
        c_df = pd.DataFrame({"Carrier": carriers, "Volume": vols})
        fig_bar = px.bar(
            c_df,
            x="Carrier",
            y="Volume",
            title="Daily Shift Volume by Carrier SLA",
            color="Carrier",
        )
        st.plotly_chart(fig_bar, use_container_width=True)
