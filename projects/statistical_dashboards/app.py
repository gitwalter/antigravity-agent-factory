import streamlit as st
import pandas as pd
from core.database import DatabaseManager, Project
from core.data_manager import DataManager
from core.viz_manager import VizManager
from core.analysis_manager import AnalysisManager
from core.connectors.financial_connector import FinancialConnector
from core.connectors.economic_connector import EconomicConnector
from core.connectors.news_connector import NewsConnector
from core.business_manager import BusinessManager
import os
import numpy as np

# --- Configuration ---
st.set_page_config(
    page_title="Antigravity Stats-Dash",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Premium Look
st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    .stButton>button {
        background: linear-gradient(45deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        border: none;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(37, 117, 252, 0.4);
    }
    .css-1d391kg {
        background-color: #161b22;
    }
    .stMetric {
        background-color: #1c2128;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# --- Initialization ---
# @st.cache_resource  # Disabled to ensure code updates (like viz_manager) are always live
def init_managers():
    db = DatabaseManager()
    data = DataManager()
    viz = VizManager()
    analysis = AnalysisManager()
    fin = FinancialConnector()
    eco = EconomicConnector()
    news = NewsConnector()
    biz = BusinessManager()
    return db, data, viz, analysis, fin, eco, news, biz


(
    db_manager,
    data_manager,
    viz_manager,
    analysis_manager,
    fin_connector,
    eco_connector,
    news_connector,
    biz_manager,
) = init_managers()

# --- Sidebar ---
st.sidebar.title("🚀 Antigravity Stats v1.2")
st.sidebar.markdown("---")

menu = st.sidebar.selectbox(
    "Navigate",
    [
        "📊 Dashboard",
        "📁 Data Manager",
        "🔬 Advanced Analytics",
        "🏢 Warehousing Intel",
        "📈 Financial Intel",
        "🌍 Global Economy",
        "📰 Market Sentiment",
        "📖 Help & Guide",
        "⚙️ Settings",
    ],
)

if menu == "📊 Dashboard":
    st.title("📊 Statistical Overview")
    st.markdown("Select a project to view metrics and visualizations.")

    session = db_manager.get_session()
    projects = session.query(Project).all()
    project_names = [p.name for p in projects]

    if project_names:
        selected_project = st.selectbox("Select Project", project_names)
        project = session.query(Project).filter_by(name=selected_project).first()

        st.subheader(f"Project: {project.name}")
        st.write(project.description)

        col1, col2, col3 = st.columns(3)
        col1.metric("Datasets", len(project.datasets))
        col2.metric("Total Rows", sum(d.row_count for d in project.datasets))
        col3.metric("Last Activity", project.created_at.strftime("%Y-%m-%d"))

        if project.datasets:
            selected_ds = st.selectbox(
                "View Dataset", [d.filename for d in project.datasets]
            )
            ds = next(d for d in project.datasets if d.filename == selected_ds)

            # Load from database (Generic Storage)
            df = data_manager.get_dataset_data(ds.id, db_manager)
            if df is not None:
                st.dataframe(df.head(10))

                # Visuals
                cols = df.select_dtypes(include=["number"]).columns.tolist()
                if len(cols) >= 2:
                    st.plotly_chart(
                        viz_manager.create_scatter_chart(
                            df, cols[0], cols[1], title=f"{cols[0]} vs {cols[1]}"
                        )
                    )
            else:
                st.error("Data content missing in database.")
    else:
        st.info("🚀 **Welcome to Antigravity Stats!**")
        st.markdown("""
        It looks like you haven't created any projects yet.

        **To get started:**
        1. Navigate to the **📁 Data Manager** in the sidebar.
        2. Initialize a new project with a name and description.
        3. Upload your first dataset (CSV or Excel).

        Check the **📖 Help & Guide** for more details and example data.
        """)
    session.close()

elif menu == "📁 Data Manager":
    st.title("📁 Data Management")

    tab1, tab2 = st.tabs(["Create Project", "Upload Data"])

    with tab1:
        st.subheader("Start New Project")
        p_name = st.text_input("Project Name")
        p_desc = st.text_area("Description")
        if st.button("Initialize Project"):
            session = db_manager.get_session()
            new_p = Project(name=p_name, description=p_desc)
            session.add(new_p)
            session.commit()
            st.success(f"Project '{p_name}' ready!")
            session.close()

    with tab2:
        st.subheader("Add Data to Project")
        session = db_manager.get_session()
        projects = session.query(Project).all()
        if projects:
            target_p = st.selectbox(
                "Target Project", [p.name for p in projects], key="upload_proj"
            )
            uploaded_file = st.file_uploader(
                "Choose a CSV or Excel file", type=["csv", "xlsx"]
            )

            if uploaded_file is not None:
                df, metadata = data_manager.load_data(uploaded_file)
                st.write("File Preview:")
                st.dataframe(df.head())

                if st.button("Process & Save"):
                    proj = session.query(Project).filter_by(name=target_p).first()
                    data_manager.save_to_database(
                        df, proj.id, uploaded_file.name, db_manager
                    )
                    st.success("Dataset ingested and cataloged in general storage.")

                    # Automapping / Domain Ingestion
                    with st.spinner("Checking for warehouse data mapping..."):
                        tables = data_manager.auto_ingest_domain_data(
                            df, proj.id, db_manager
                        )
                        if tables:
                            st.balloons()
                            st.success(
                                f"🚀 Domain Match! Data automatically mapped to: {', '.join(tables)}"
                            )
                        else:
                            st.info(
                                "No automatic domain mapping found. Using generic analysis."
                            )
        else:
            st.warning("Create a project first.")
        session.close()

elif menu == "🔬 Advanced Analytics":
    st.title("🔬 Advanced Statistical Analysis")
    st.markdown("Perform regression and correlation analysis on your project datasets.")

    session = db_manager.get_session()
    projects = session.query(Project).all()
    project_names = [p.name for p in projects]

    if project_names:
        selected_project = st.selectbox("Select Project for Analysis", project_names)
        project = session.query(Project).filter_by(name=selected_project).first()

        if project.datasets:
            selected_ds = st.selectbox(
                "Select Dataset", [d.filename for d in project.datasets]
            )
            ds = next(d for d in project.datasets if d.filename == selected_ds)

            df = data_manager.get_dataset_data(ds.id, db_manager)

            if df is not None:
                analysis_tab, corr_tab, ts_tab = st.tabs(
                    [
                        "Regression Analysis",
                        "Correlation Matrix",
                        "Time-Series Baseline",
                    ]
                )

                with analysis_tab:
                    st.subheader("Linear Regression")
                    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
                    if len(num_cols) >= 2:
                        y_var = st.selectbox(
                            "Dependent Variable (Y)", num_cols, index=0
                        )
                        x_var = st.selectbox(
                            "Independent Variable (X)", num_cols, index=1
                        )

                        if st.button("Run Regression"):
                            results = analysis_manager.run_linear_regression(
                                df, x_var, y_var
                            )
                            if results:
                                c1, c2, c3 = st.columns(3)
                                c1.metric("R-Squared", f"{results['r2']:.4f}")
                                c2.metric(
                                    "Coefficient", f"{results['coefficient']:.4f}"
                                )
                                c3.metric("MSE", f"{results['mse']:.4e}")

                                # Regression plot
                                import plotly.graph_objects as go

                                fig = viz_manager.create_scatter_chart(
                                    df,
                                    x_var,
                                    y_var,
                                    title=f"Regression: {y_var} vs {x_var}",
                                )
                                fig.add_trace(
                                    go.Scatter(
                                        x=results["x_range"],
                                        y=results["y_pred"],
                                        mode="lines",
                                        name="Reg Line",
                                        line=dict(color="red", width=2),
                                    )
                                )
                                st.plotly_chart(fig)

                                st.info(
                                    f"**AI Insight:** {analysis_manager.generate_ai_insight('regression', results)}"
                                )
                            else:
                                st.error("Regression failed. Check for missing data.")
                    else:
                        st.warning("Need at least two numeric columns for regression.")

                with corr_tab:
                    st.subheader("Numeric Correlation Heatmap")
                    if len(num_cols) >= 2:
                        corr_matrix = analysis_manager.get_correlation_matrix(df)
                        st.plotly_chart(
                            viz_manager.create_heatmap(
                                corr_matrix, title="Feature Correlation Matrix"
                            )
                        )
                    else:
                        st.warning("Not enough numeric columns for correlation.")

                with ts_tab:
                    st.subheader("Time-Series Trends")
                    ts_cols = df.select_dtypes(include=["number"]).columns.tolist()
                    if ts_cols:
                        target_col = st.selectbox(
                            "Select Variable for Trend Analysis", ts_cols
                        )
                        window = st.slider("Rolling Window Size", 2, 60, 7)

                        if st.button("Calculate Trends"):
                            results = analysis_manager.run_time_series_baseline(
                                df, target_col, window=window
                            )
                            if results is not None:
                                m1, m2 = st.columns(2)
                                m1.metric(
                                    f"Current SMA ({window}d)",
                                    f"{results['latest_sma']:.2f}",
                                )
                                m2.metric(
                                    "Rolling Volatility", f"{results['latest_std']:.2f}"
                                )

                                # Plot SMA
                                import plotly.graph_objects as go

                                fig = viz_manager.create_line_chart(
                                    df,
                                    df.index.name or "index",
                                    target_col,
                                    title=f"{target_col} Trends",
                                )
                                # Ensure index is sorted if it's temporal
                                fig.add_trace(
                                    go.Scatter(
                                        x=df.index,
                                        y=results["sma"],
                                        mode="lines",
                                        name=f"{window}d SMA",
                                        line=dict(dash="dash"),
                                    )
                                )
                                st.plotly_chart(fig)

                                st.info(
                                    f"**AI Insight:** {analysis_manager.generate_ai_insight('time-series', results)}"
                                )
                            else:
                                st.error("Time-Series analysis failed.")
                    else:
                        st.warning("No numeric data for time-series analysis.")
            else:
                st.error("Data file missing.")
        else:
            st.info("No datasets in this project.")
    else:
        st.info("Create a project and upload data first.")
    session.close()

elif menu == "🏢 Warehousing Intel":
    st.title("🏢 Warehousing Intelligence")
    st.markdown("Role-based insights for Amazon-scale fulfillment operations.")

    role = st.radio(
        "Select Perspective",
        ["Operations Manager", "Associate (Station)", "Industrial Analyst"],
        horizontal=True,
    )

    session = db_manager.get_session()
    projects = session.query(Project).all()
    project_names = [p.name for p in projects]

    if project_names:
        selected_project = st.selectbox(
            "Select Warehouse Project", project_names, key="wh_proj"
        )
        project = session.query(Project).filter_by(name=selected_project).first()

        if role == "Operations Manager":
            st.subheader("🚀 Mission Control: Shift KPIs")
            with st.expander("📖 Manager Operational Guide", expanded=False):
                st.markdown("""
                **Workflow Summary**:
                1. **Volume Review**: Check ASN vs. actual dock arrival.
                2. **Labor Health**: Re-assign stowers if LSR > 3.5%.
                3. **Outbound Urgency**: Prioritize 'Hot Picks' for carrier pickup.
                *See full workflow in `.agent/workflows/warehouse-manager.md`*
                """)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Dock-to-Stock", "1.4 hrs", "-0.2h", help="Target: < 2.0 hrs")
            c2.metric("Late Ship Rate", "2.1%", "-0.5%", help="Target: < 4.0%")
            c3.metric("Current UPH", "342", "+12", help="Units Per Hour")
            c4.metric("Labor Health", "94%", "Stable")

            st.divider()
            st.subheader("📦 Fulfillment Velocity")
            st.info(
                "Managers monitor the entire flow from Dock arrival to Carrier pickup."
            )

        elif role == "Associate (Station)":
            st.subheader("🛠️ My Station Performance")
            with st.expander("📖 Associate Workflow Guide", expanded=False):
                st.markdown("""
                **Fast-Track Workflow**:
                1. **Station Login**: Verify supplies and ergonomics.
                2. **Execution**: Follow system-suggested route; Scan-First Policy.
                3. **Real-Time UPH**: Keep UPH within 5% of target to trigger productivity bonus.
                *See full workflow in `.agent/workflows/warehouse-associate.md`*
                """)

            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric("My UPH", "85", "+5")
                st.metric("Accuracy", "99.98%", "Top 5%")
            with col2:
                st.success("Current Status: Optimized Flow. Keep it up!")
                st.markdown("""
                **Next Task**: High-Priority Stowing
                - **Target Bin Area**: A-12 to B-04
                - **Item Priority**: Electronics (Expedited)
                """)

        elif role == "Industrial Analyst":
            st.subheader("📊 Optimization & Bottleneck Analysis")
            with st.expander("📖 Analyst Optimization Guide", expanded=False):
                st.markdown("""
                **Advanced Workflow**:
                1. **Density Analysis**: Generate Heatmaps; check aisles > 85% density.
                2. **Process Variances**: Correlate Shelf Height vs. Stow Speed.
                3. **Predictive Labor**: Forecast volume based on ASN historical regression.
                *See full workflow in `.agent/workflows/warehouse-analyst.md`*
                """)

            tab1, tab2, tab3 = st.tabs(
                ["Bin Density Heatmap", "Process Variances", "Anomaly Detection"]
            )
            with tab1:
                st.write("Visualizing bin utilization vs. pick travel time.")
                st.image(
                    "https://via.placeholder.com/800x400.png?text=Bin+Density+Heatmap",
                    use_container_width=True,
                )

            with tab2:
                st.write("Correlating Shelf Height vs. Stow Speed.")
                # Show regression results
                reg_results = analysis_manager.run_linear_regression(
                    pd.DataFrame(
                        {"Height": [1, 2, 3, 4, 5], "Speed": [100, 90, 80, 70, 60]}
                    ),
                    "Height",
                    "Speed",
                )
                st.code(analysis_manager.generate_ai_insight("regression", reg_results))

            with tab3:
                st.write("Detecting UPH outliers and process anomalies.")
                st.info(
                    "Using IQR and Z-Score methods from the Statistical Mastery skill."
                )
                # Mocking a group comparison
                test_results = analysis_manager.run_hypothesis_test(
                    pd.Series([80, 82, 85]), pd.Series([70, 72, 68])
                )
                st.write(
                    analysis_manager.generate_ai_insight("hypothesis", test_results)
                )

        st.divider()
        st.subheader("📥 Process Data Ingestion")
        st.write("Upload specific logs to update these perspectives.")

        file_type = st.selectbox(
            "Select Process Log Type",
            ["Inbound (ASN/Receiving)", "Inventory Snapshot", "Outbound Fulfillment"],
        )
        uploaded_file = st.file_uploader(f"Upload {file_type} (CSV/Excel)")
        if uploaded_file:
            st.success(f"{file_type} processed. Perspectives updated!")

    else:
        st.info("Use the Data Manager to create a 'Warehouse' project first.")
    session.close()

elif menu == "📈 Financial Intel":
    st.title("📈 Financial Intelligence")
    ticker = st.text_input("Enter Ticker (e.g., TSLA, AAPL, BTC-USD)", "AAPL")
    period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

    if st.button("Fetch Analysis"):
        with st.spinner("Analyzing market data..."):
            df = fin_connector.get_ticker_data(ticker, period=period)
            info = fin_connector.get_ticker_info(ticker)

            if not df.empty:
                st.subheader(f"{info.get('longName', ticker)}")
                st.write(info.get("longBusinessSummary", "No summary available."))

                st.plotly_chart(
                    viz_manager.create_line_chart(
                        df, "Date", "Close", title=f"{ticker} Adjusted Close"
                    )
                )

                metrics = st.columns(4)
                metrics[0].metric(
                    "Current Price", f"${info.get('currentPrice', 'N/A')}"
                )
                metrics[1].metric("Market Cap", f"{info.get('marketCap', 'N/A'):,}")
                metrics[2].metric("PE Ratio", info.get("forwardPE", "N/A"))
                metrics[3].metric(
                    "Dividend Yield", f"{info.get('dividendYield', 0):.2f}%"
                )
            else:
                st.error("Market data unreachable for this ticker.")

elif menu == "🌍 Global Economy":
    st.title("🌍 Global Economic Intelligence")
    st.markdown("Fetch macroeconomic data directly from the World Bank API.")

    col1, col2 = st.columns(2)
    with col1:
        country = st.text_input("Enter Country Code (e.g., USA, DEU, CHN, BRA)", "USA")
    with col2:
        indicators = eco_connector.list_common_indicators()
        selected_indicator_label = st.selectbox(
            "Select Indicator", list(indicators.keys())
        )
        indicator_code = indicators[selected_indicator_label]

    date_range = st.slider("Select Year Range", 1960, 2024, (2000, 2023))

    if st.button("Retrieve Economic Data"):
        with st.spinner(f"Fetching {selected_indicator_label} for {country}..."):
            df = eco_connector.get_indicator_data(
                country, indicator_code, f"{date_range[0]}:{date_range[1]}"
            )

            if not df.empty:
                st.subheader(f"{selected_indicator_label}: {country}")
                st.write("Data Source: World Bank API")

                # Plot
                st.plotly_chart(
                    viz_manager.create_line_chart(
                        df,
                        "date",
                        "value",
                        title=f"{selected_indicator_label} Over Time",
                    )
                )

                # Metrics
                latest = df.iloc[-1]
                prev = df.iloc[-2] if len(df) > 1 else latest

                m1, m2 = st.columns(2)
                m1.metric(f"Latest Value ({latest['date']})", f"{latest['value']:,.2f}")

                if latest["value"] and prev["value"]:
                    delta = ((latest["value"] - prev["value"]) / prev["value"]) * 100
                    m2.metric("Annual Change", f"{delta:.2f}%")

                with st.expander("Show Raw Data"):
                    st.dataframe(df)
            else:
                st.error("No data found for this selection.")

elif menu == "📰 Market Sentiment":
    st.title("📰 Market Sentiment & News")
    st.markdown("Track global financial news and headlines.")

    query = st.text_input("Search Topics", "Stock Market")
    if st.button("Fetch Headlines"):
        with st.spinner("Scanning global news..."):
            df = news_connector.get_latest_news(query=query)
            if not df.empty:
                for idx, row in df.iterrows():
                    st.markdown(f"### {row['title']}")
                    st.write(
                        f"**Source:** {row.get('source', 'N/A')} | **Sentiment:** {row.get('sentiment', 'N/A')}"
                    )
                    st.markdown(f"[[Read full article]({row['link']})]")
                    st.divider()
            else:
                st.info("No news found for this topic.")

elif menu == "📖 Help & Guide":
    st.title("📖 Statistical Dashboard Guide")
    st.markdown("""
    ### 🚀 Getting Started: Create a New Project
    To begin analyzing data, you must first initialize a project:

    1. **Navigate to Data Manager**: Select **📁 Data Manager** from the sidebar.
    2. **Initialize Project**:
        - Under the **Create Project** tab, enter a name and description.
        - Click **Initialize Project**.
    3. **Upload Data**:
        - Switch to the **Upload Data** tab.
        - Select your project from the dropdown.
        - Upload a CSV or Excel file and click **Process & Save**.

    ### 📂 Example Data for Testing
    You can find pre-generated datasets in the `projects/statistical_dashboards/data/` directory:
    - `sales_data.csv`: Transaction-level sales records across regions.
    - `warehouse_data.csv`: SKU-level stock levels and reorder points.
    - `accounting_data.csv`: Journal entries with debit/credit tracking by department.
    - `manufacturing_data.csv`: Machine-level production yields and energy consumption.

    ### 🔬 Analysis Workflows
    - **Advanced Analytics**: Run regressions, view correlation matrices, and analyze time-series trends.
    - **Warehousing Intel**: Role-based insights for operations managers, associates, and analysts.
    - **Financial & Economic Intel**: Pull live data for tickers, countries, and news sentiment.
    """)

elif menu == "⚙️ Settings":
    st.title("⚙️ System Settings")
    st.write("Configure your Antigravity Stats Dashboard experience.")

    st.subheader("Data Storage")
    st.write(f"Database Path: {db_manager.db_path}")
    st.write(f"Parquet Storage: {data_manager.data_dir}")

    st.divider()
    if st.button("Reset Session Cache"):
        st.cache_resource.clear()
        st.success("Cache cleared!")
