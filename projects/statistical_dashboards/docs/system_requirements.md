# Statistical Dashboard System Requirements

## R1: Guidance & Education
- **RE1.1**: The application MUST provide a centralized Guidance Center explaining the end-to-end workflow (Data Ingestion -> Analysis -> Insights).
- **RE1.2**: The application MUST provide a KPI Dictionary defining all domain-specific metrics (e.g., UPH, Inventory Turnover) and their calculation logic.
- **RE1.3**: The application MUST provide a Statistical Primer for non-specialists to understand AI/ML outputs (Clustering, Regression).
- **RE1.4**: Contextual tooltips and information boxes MUST be available near interactive controls to guide data entry and analysis choices.

## R2: Template-Based Visualization System
- **RE2.1**: The system MUST support a template-based dashboard engine (using Jinja2 or equivalent).
- **RE2.2**: Users MUST be able to define and reuse "Diagram Templates" for standardized Plotly configurations.
- **RE2.3**: Users MUST be able to load "Dashboard Blueprints" (Layout Templates) that combine multiple diagrams into a structured view.
- **RE2.4**: The system SHOULD allow saving current UI states as reusable JSON-backed templates.

## R3: Real-World Example Library
- **RE3.1**: The application MUST include "Real-Life Use" example datasets for multiple domains (Warehouse, Sales, Finance).
- **RE3.2**: Each example MUST be accompanied by a "Story" explaining the business problem it solves.

## R4: Project Life-Cycle Tracking
- **RE4.1**: The application MUST allow users to track the life-cycle of an analytics project (e.g., Status: Discovery, In Progress, Review, Completed).
- **RE4.2**: The application MUST support assigning "Priority" and "Target Dates" to projects.
- **RE4.3**: The system MUST provide a "Project Summary" view showing progress, datasets attached, and key milestones reached.
- **RE4.4**: Users MUST be able to define "Analysis Tasks" within a project (e.g., "Analyze Q3 Outbound Volatility") and track their completion status.
- **RE4.5**: The application MUST provide a synchronization hook for the **Memory MCP**, allowing dashboard projects to be registered as entities in the Antigravity Factory Knowledge Graph.
