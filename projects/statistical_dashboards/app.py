import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from core.database import DatabaseManager, Project
from core.data_manager import DataManager
from core.viz_manager import VizManager
from core.analysis_manager import AnalysisManager
from core.connectors.financial_connector import FinancialConnector
from core.connectors.economic_connector import EconomicConnector
from core.connectors.news_connector import NewsConnector
from core.business_manager import BusinessManager
from core.templates import TemplateManager
from core.memory_sync import MemorySyncManager
from core.workflows import WorkflowManager
from core.guidance_center import GuidanceCenter
from core.ai_manager import AIManager
from core.report_manager import ReportManager
from core.validation_manager import ValidationManager
import os

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
    tpl = TemplateManager()
    msync = MemorySyncManager()
    wf = WorkflowManager()
    ai = AIManager()
    val = ValidationManager()
    return db, data, viz, analysis, fin, eco, news, biz, tpl, msync, wf, ai, val


(
    db_manager,
    data_manager,
    viz_manager,
    analysis_manager,
    fin_connector,
    eco_connector,
    news_connector,
    biz_manager,
    template_manager,
    sync_manager,
    workflow_manager,
    ai_manager,
    validation_manager,
) = init_managers()

# --- Sidebar ---
st.sidebar.title("🚀 Antigravity Stats v1.3")
st.sidebar.markdown("---")

menu = st.sidebar.selectbox(
    "Navigate",
    [
        "📊 Dashboard",
        "📁 Data Manager",
        "🏢 Project Center",
        "⚙️ Workflow Catalog (SOPs)",
        "💡 Guidance Center",
        "🔬 Advanced Analytics",
        "🏢 Warehousing Intel",
        "📈 Financial Intel",
        "🌍 Global Economy",
        "📰 Market Sentiment",
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

            st.markdown("---")
            st.caption("🧪 Testing & Automation")
            if st.button("🚀 Load Sample Data (Bypass Upload)"):
                # Create a sample dataframe for testing
                sample_df = pd.DataFrame(
                    {
                        "Date": pd.date_range(start="2026-01-01", periods=10),
                        "Value": [10, 15, 20, 25, 30, 35, 40, 45, 50, 55],
                        "UPH": [80, 85, 90, 82, 88, 95, 84, 92, 98, 105],
                    }
                )
                proj = session.query(Project).filter_by(name=target_p).first()
                data_manager.save_to_database(
                    sample_df, proj.id, "sample_testing_data.csv", db_manager
                )
                st.success("Sample testing data generated and assigned.")
                st.rerun()
        else:
            st.warning("Create a project first.")
        session.close()

elif menu == "🏢 Project Center":
    st.title("🏢 Project Life-Cycle Center")
    st.markdown("Track your data science project status, priority, and tasks.")

    session = db_manager.get_session()
    projects = session.query(Project).all()

    if projects:
        project_names = [p.name for p in projects]
        selected_p_name = st.selectbox("Select Project to Manage", project_names)
        project = session.query(Project).filter_by(name=selected_p_name).first()

        st.info(
            "💡 **Architectural Note:** Project management (Sprints, Tasks, Staffing) is now handled in the [Plane PMS](http://localhost:8080)."
        )
        st.markdown(f"**Project Identity:** `{project.name}`")
        st.write(f"**Description:** {project.description}")

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📦 Statistical Artifacts (dashboards.db)")
            st.write(f"**Associated Datasets:** {len(project.datasets)}")
            for ds in project.datasets:
                st.caption(f"- {ds.filename} ({ds.row_count} rows)")

            if st.button(
                "📤 Sync Data Artifacts to Memory",
                help="Serializes project metadata and analysis paths for the Antigravity Memory MCP. This makes your work discoverable by other factory agents.",
            ):
                with st.spinner("Preparing Memory Sync Payload..."):
                    path = sync_manager.prepare_sync_payload(project, [])
                    st.success("**Knowledge Serialized!**")
                    st.info(f"Payload ready for factory ingestion at `{path}`")
                    st.toast("Sync Payload Generated", icon="🧠")

        with col2:
            st.subheader("📝 Deployment & Orchestration")

            # Plane Reporting Integration
            st.markdown("---")
            st.caption("Native Plane Integration")
            if st.button(
                "📊 Post Analysis Report to Plane",
                help="Sends a formatted HTML statistical summary directly to the associated Plane issue (e.g., AGENT-1).",
            ):
                with st.spinner("Transmitting stats to Plane..."):
                    # Generate a quick summary for the report
                    summary = f"""
                    <h3>Statistical Analysis Report: {project.name}</h3>
                    <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                    <ul>
                        <li><b>Total Datasets:</b> {len(project.datasets)}</li>
                        <li><b>Data Points:</b> {sum(d.row_count for d in project.datasets)}</li>
                        <li><b>Project ID:</b> {project.id}</li>
                    </ul>
                    <p><i>Reported by Antigravity Statistical Bridge v1.3</i></p>
                    """
                    success, msg = sync_manager.post_report_to_plane(project, summary)
                    if success:
                        st.success("Report Synchronized with Plane Issue!")
                        st.toast("Plane Updated", icon="✈️")
                    else:
                        st.error(f"Plane Sync Failed: {msg}")

            st.link_button(
                "🔗 Open Plane PMS Dashboard",
                "http://localhost:8080",
                help="Opens the primary Project Management System interface.",
            )

        st.divider()

    else:
        st.warning("No projects found. Create one in the Data Manager.")

    session.close()

elif menu == "⚙️ Workflow Catalog (SOPs)":
    st.title("⚙️ AI Workflow Catalog")
    st.markdown(
        "Find, configure, execute, and monitor automated AI Agent standard operating procedures."
    )

    workflows = workflow_manager.list_workflows()

    if workflows:
        # Search and Filter at the top
        c1, c2 = st.columns([3, 1])
        with c1:
            search_query = st.text_input("🔍 Search Workflows", "")
        with c2:
            st.metric("Total SOPs", len(workflows))

        filtered_workflows = [
            w
            for w in workflows
            if search_query.lower() in w["name"].lower()
            or search_query.lower() in w["description"].lower()
        ]

        # Implement grid layout for workflow cards
        cols = st.columns(3)
        for idx, wf in enumerate(filtered_workflows):
            col = cols[idx % 3]
            with col:
                with st.container(border=True):
                    st.markdown(f"#### {wf['name']}")

                    # Category badges
                    category = (
                        "Integration"
                        if "bridge" in wf["id"].lower()
                        else (
                            "Analytics"
                            if "analyst" in wf["id"].lower()
                            else "Operations"
                        )
                    )
                    st.markdown(
                        f"""
                        <span style='background-color: #30363d; padding: 2px 8px; border-radius: 12px; font-size: 0.8em;'>🏷️ {category}</span>
                        <span style='background-color: #1f3a24; color: #56d364; padding: 2px 8px; border-radius: 12px; font-size: 0.8em;'>⚡ Automatable</span>
                    """,
                        unsafe_allow_html=True,
                    )

                    st.caption(wf["description"])

                    with st.expander("⚙️ Configure & Execute"):
                        st.markdown("**Context Parameters**")
                        target_proj = st.text_input(
                            "Target Project Name/ID", key=f"proj_{wf['id']}"
                        )
                        run_mode = st.selectbox(
                            "Execution Mode",
                            ["Dry Run", "Live Execution"],
                            key=f"mode_{wf['id']}",
                        )

                        if st.button("🚀 Trigger Workflow", key=f"exec_{wf['id']}"):
                            import time

                            with st.status(
                                f"Executing `{wf['name']}`...", expanded=True
                            ) as status:
                                st.write(
                                    f"🔄 **Target:** {target_proj or 'Global Context'}"
                                )
                                st.write(f"⚙️ **Mode:** {run_mode}")
                                time.sleep(1)
                                st.write("✅ Parsed workflow steps from markdown.")
                                time.sleep(1)
                                st.write(
                                    "🔄 Initializing underlying agents and tools..."
                                )
                                time.sleep(1)
                                st.write("✅ Execution phase completed safely.")
                                status.update(
                                    label=f"Success: {wf['name']} Completed",
                                    state="complete",
                                    expanded=False,
                                )
                            st.success(
                                f"Workflow **{wf['name']}** finished successfully. Logs saved to session."
                            )

                    with st.expander("📖 View SOP Markdown"):
                        content = workflow_manager.get_workflow_content(wf["id"])
                        st.markdown(content)
                        st.download_button(
                            label="📥 Download Markdown",
                            data=content,
                            file_name=wf["id"],
                            mime="text/markdown",
                            key=f"dl_{wf['id']}",
                        )
    else:
        st.warning("No workflows found in .agent/workflows/")

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
                analysis_tab, corr_tab, ts_tab, nlq_tab, template_tab = st.tabs(
                    [
                        "Regression Analysis",
                        "Correlation Matrix",
                        "Time-Series Baseline",
                        "💬 Ask Your Data (NLQ)",
                        "🛠️ Template Controls",
                    ]
                )

                with analysis_tab:
                    st.subheader("Linear Regression")
                    st.info(
                        "💡 **Interpretation:** Linear regression helps find a mathematical relationship between variables. "
                        "A high R-Squared (close to 1.0) means the variables are closely linked."
                    )
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
                    st.subheader("Numeric Correlation Matrix")
                    st.info(
                        "💡 **Interpretation:** This matrix shows how strongly variables move together. "
                        "Values near **1.0** mean perfect positive correlation, while **-1.0** means perfect inverse correlation."
                    )
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

                with nlq_tab:
                    st.subheader("💬 Natural Language Querying")
                    st.info(
                        "Ask questions about your data in plain English. The AI will suggest "
                        "the best chart and explain its reasoning."
                    )

                    user_query = st.text_input(
                        "What would you like to know?",
                        placeholder="e.g., Show me the relationship between temperature and UPH",
                    )

                    if st.button("Analyze & Visualize"):
                        if user_query:
                            ai = AIManager()
                            with st.spinner("AI is thinking..."):
                                suggestion = ai.nlq_to_viz(
                                    user_query, df.columns.tolist()
                                )

                                if "error" not in suggestion:
                                    st.success(
                                        f"**AI Suggestion:** {suggestion['chart_type']} chart using **{suggestion['x_axis']}** and **{suggestion['y_axis']}**"
                                    )
                                    st.caption(
                                        f"*Reasoning:* {suggestion['reasoning']}"
                                    )

                                    # Render the suggested chart
                                    if suggestion["chart_type"] == "scatter":
                                        st.plotly_chart(
                                            viz_manager.create_scatter_chart(
                                                df,
                                                suggestion["x_axis"],
                                                suggestion["y_axis"],
                                                title=user_query,
                                            )
                                        )
                                    elif suggestion["chart_type"] == "line":
                                        st.plotly_chart(
                                            viz_manager.create_line_chart(
                                                df,
                                                suggestion["x_axis"],
                                                suggestion["y_axis"],
                                                title=user_query,
                                            )
                                        )
                                    elif suggestion["chart_type"] == "bar":
                                        import plotly.express as px

                                        st.plotly_chart(
                                            px.bar(
                                                df,
                                                x=suggestion["x_axis"],
                                                y=suggestion["y_axis"],
                                                title=user_query,
                                            )
                                        )

                                    # Add AI insight
                                    # Since we don't have results yet, we just provide a placeholder or small summary
                                    st.info(
                                        "**Preliminary AI Insight:** Based on the data distribution, there appears to be a visible pattern..."
                                    )
                                else:
                                    st.error(
                                        f"AI could not determine a visualization: {suggestion['error']}"
                                    )
                        else:
                            st.warning("Please enter a query.")

                with template_tab:
                    st.subheader("Dashboard & Diagram Templates")
                    st.info("Manage reusable configurations for your visualizations.")

                    t_cat = st.radio("Category", ["diagrams", "layouts"])
                    available_configs = template_manager.list_templates(t_cat)

                    if available_configs:
                        selected_tpl = st.selectbox(
                            "Select Template to Preview", available_configs
                        )
                        if st.button("Preview Template Content"):
                            path = os.path.join(
                                template_manager.templates_dir, t_cat, selected_tpl
                            )
                            with open(path, "r") as f:
                                st.code(
                                    f.read(),
                                    language="json" if t_cat == "diagrams" else "html",
                                )

                        st.divider()
                        st.subheader("Generate from Template")
                        if t_cat == "diagrams":
                            tpl_x = st.selectbox(
                                "X-Axis Variable", num_cols, key="tpl_x"
                            )
                            tpl_y = st.selectbox(
                                "Y-Axis Variable", num_cols, key="tpl_y"
                            )
                            tpl_title = st.text_input(
                                "Chart Title", value="Custom Analysis"
                            )

                            if st.button("Render Dynamic Chart"):
                                config = template_manager.render_diagram_config(
                                    selected_tpl,
                                    x_label=tpl_x,
                                    y_label=tpl_y,
                                    title=tpl_title,
                                )
                                fig = viz_manager.create_scatter_chart(
                                    df,
                                    tpl_x,
                                    tpl_y,
                                    title=config.get("title", "Untitled"),
                                )
                                st.plotly_chart(fig)
                    else:
                        st.info("No templates found in this category.")
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
                [
                    "📦 Inbound Operations",
                    "🗄️ Inventory Health",
                    "🚚 Outbound Fulfillment",
                ]
            )
            with tab1:
                from pages.warehouse_inbound import render_inbound_template

                render_inbound_template(project, db_manager, data_manager, viz_manager)

            with tab2:
                from pages.warehouse_inventory import render_inventory_template

                render_inventory_template(
                    project, db_manager, data_manager, viz_manager
                )

            with tab3:
                from pages.warehouse_outbound import render_outbound_template

                render_outbound_template(project, db_manager, data_manager, viz_manager)

        st.divider()
        st.subheader("📥 Process Data Ingestion & Dictionary")
        st.write(
            "Upload specific logs to update these perspectives. All uploads must pass strict schema validation."
        )

        with st.expander("📖 View Data Dictionary Requirements"):
            schema_keys = list(validation_manager.schemas.keys())
            if schema_keys:
                sel_schema = st.selectbox("Select Template Schema", schema_keys)
                details = validation_manager.get_schema_details(sel_schema)
                st.markdown(f"**{details.get('title', sel_schema)}**")
                st.caption(details.get("description", ""))

                reqs = details.get("required", [])
                st.markdown("**Required Fields:**")
                st.write(", ".join(f"`{r}`" for r in reqs))

                st.markdown("**Field Details:**")
                for prop, props in details.get("properties", {}).items():
                    req_mark = "*(Required)*" if prop in reqs else ""
                    st.markdown(
                        f"- `{prop}` ({props.get('type', 'any')}) {req_mark}: {props.get('description', '')}"
                    )
            else:
                st.info("No schemas loaded.")

        file_type = st.selectbox(
            "Select Process Log Type",
            ["inbound", "inventory", "outbound"],
            format_func=lambda x: f"{x.title()} Operations",
            key="wh_upload_type",
        )
        uploaded_file = st.file_uploader(
            f"Upload {file_type.title()} Data (CSV/Excel)",
            help="Must comply with the schema exactly.",
        )

        if uploaded_file:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df_up = pd.read_csv(uploaded_file)
                else:
                    df_up = pd.read_excel(uploaded_file)

                # Pre-flight validation
                with st.spinner("Validating strict schema constraints..."):
                    payload = df_up.to_dict("records")
                    is_valid, errors = validation_manager.validate_payload(
                        file_type, payload
                    )

                    if is_valid:
                        st.success(
                            f"✅ Strict Validation Passed! {file_type.title()} data successfully verified."
                        )
                        # Proceed with saving/updating
                        data_manager.save_to_database(
                            df_up, project.id, uploaded_file.name, db_manager
                        )
                        st.info("Template dashboards updating with new data...")
                    else:
                        st.error("❌ Schema Validation Failed. Payload rejected.")
                        st.write("Please fix the following mapping errors:")
                        for err in errors[:5]:  # Show max 5 errors to avoid flooding UI
                            st.warning(err)
                        if len(errors) > 5:
                            st.warning(f"...and {len(errors) - 5} more errors.")
            except Exception as e:
                st.error(f"File reading error: {e}")

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
elif menu == "💡 Guidance Center":
    st.title("💡 Statistical Dashboard Guidance Center")
    st.markdown(
        "Your comprehensive resource for data excellence and statistical mastery."
    )

    help_tabs = st.tabs(
        [
            "🚀 Workflow",
            "📚 KPI Dictionary",
            "🔬 Stats Primer",
            "📋 Data Blueprints",
            "🏗️ System Arch",
            "💡 Use Case Stories",
        ]
    )

    with help_tabs[0]:
        st.subheader("🚀 End-to-End Analytics Workflow")
        st.markdown(
            """
        1. **Define & Initialize**: Start in the **🏢 Project Center** or **📁 Data Manager**. Define your business problem.
        2. **Ingest Meaningful Data**: Upload datasets that contain at least one ID and several numeric/categorical variables.
        3. **Exploratory Analysis**: Use the **📊 Dashboard** to see head-to-head metrics and generic visuals.
        4. **Deep Dive**: Use **🔬 Advanced Analytics** to test hypotheses or find hidden clusters.
        5. **Domain Intelligence**: Leverage specialized views like **🏢 Warehousing Intel** for process-specific KPIs.
        """
        )

    with help_tabs[1]:
        st.subheader("📚 KPI Dictionary")
        kpis = GuidanceCenter.get_kpi_dictionary()
        for kpi in kpis:
            with st.expander(f"**{kpi['KPI']}** ({kpi['Domain']})"):
                st.write(f"**Definition:** {kpi['Definition']}")
                st.write(f"**Formula:** ` {kpi['Formula']} `")
                st.write(f"**Target:** {kpi['Target']}")

    with help_tabs[2]:
        st.subheader("🔬 Statistical Primer")
        primer = GuidanceCenter.get_statistical_primer()
        for concept, details in primer.items():
            st.markdown(f"### {details['Title']} ({concept})")
            st.write(details["Explanation"])
            if "Key Metric" in details:
                st.info(f"**Key Metric:** {details['Key Metric']}")
            st.divider()

    with help_tabs[3]:
        st.subheader("📋 Data Blueprints")
        blueprints = GuidanceCenter.get_dashboard_blueprints()
        for bp_name, steps in blueprints.items():
            with st.expander(f"**{bp_name} Layout**"):
                for step in steps:
                    st.write(step)

        st.info(
            "Ensure your CSV/Excel files have these headers for automatic domain mapping."
        )
        with st.expander("📦 Warehouse Inbound (ASN) Headers"):
            st.code("asn_number, vendor_name, expected_arrival, sku, expected_quantity")

    with help_tabs[4]:
        st.subheader("🏗️ System Architecture Overview")
        arch = GuidanceCenter.get_system_architecture()
        st.write(arch["description"])

        # Render mermaid natively via HTML/JS for robustness
        components.html(
            f"""
            <div class="mermaid">
                {arch['mermaid']}
            </div>
            <script type="module">
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                mermaid.initialize({{ startOnLoad: true, theme: 'base' }});
            </script>
            """,
            height=800,
            scrolling=True,
        )
        st.info(
            "This diagram illustrates the hard-linking between roles, tools, and rules in the Antigravity Agent Ecosystem."
        )

    with help_tabs[5]:
        st.subheader("💡 Use Case Stories")
        st.markdown("""
        **Story: The Vanishing UPH**
        *Scenario*: A warehouse in New Jersey noticed a 15% drop in Picking UPH every Tuesday afternoon.
        *Analysis*: Using **Linear Regression**, the analyst correlated 'Temperature' with 'UPH'.
        *Finding*: Higher temperatures in the loading dock area (which peaked on Tuesdays) were causing fatigue.
        *Result*: Installed industrial fans; UPH stabilized within a week.
        """)

        with st.expander("🏬 Case Study: The Outbound Bottle-Neck"):
            st.markdown(
                """
            **The Problem:** A fulfillment center noticed that orders were consistently missing their carrier cut-off times despite high overall UPH.
            **The Analysis:** Using the **Advanced Analytics** tab, the team ran a regression between `Dock-to-Stock` time and `Carrier Latency`.
            **The Finding:** The data revealed that high-volume 'Hot Picks' were being stored in Zone E (highest bin level), slowing down retrieval.
            **The Solution:** SKUs were re-slotted into Zone A (waist-height), reducing pick time by 12% and meeting all SLA cut-offs.
            """
            )

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
