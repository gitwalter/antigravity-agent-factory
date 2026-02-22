import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import pandas as pd


class VizManager:
    def __init__(self):
        pass

    def create_line_chart(self, df, x, y, title="Line Chart"):
        if x == "index" or (hasattr(df.index, "name") and x == df.index.name):
            plot_df = df.reset_index()
            x_col = df.index.name if df.index.name else "index"
            fig = px.line(plot_df, x=x_col, y=y, title=title, template="plotly_dark")
        else:
            fig = px.line(df, x=x, y=y, title=title, template="plotly_dark")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e0e0e0",
        )
        return fig

    def create_bar_chart(self, df, x, y, title="Bar Chart"):
        if x == "index" or (hasattr(df.index, "name") and x == df.index.name):
            plot_df = df.reset_index()
            x_col = df.index.name if df.index.name else "index"
            fig = px.bar(plot_df, x=x_col, y=y, title=title, template="plotly_dark")
        else:
            fig = px.bar(df, x=x, y=y, title=title, template="plotly_dark")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e0e0e0",
        )
        return fig

    def create_scatter_chart(self, df, x, y, color=None, title="Scatter Plot"):
        if x == "index" or (hasattr(df.index, "name") and x == df.index.name):
            plot_df = df.reset_index()
            x_col = df.index.name if df.index.name else "index"
            fig = px.scatter(
                plot_df, x=x_col, y=y, color=color, title=title, template="plotly_dark"
            )
        else:
            fig = px.scatter(
                df, x=x, y=y, color=color, title=title, template="plotly_dark"
            )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e0e0e0",
        )
        return fig

    def create_heatmap(self, df, title="Heatmap"):
        fig = px.imshow(
            df,
            text_auto=True,
            aspect="auto",
            title=title,
            template="plotly_dark",
            color_continuous_scale="RdBu_r",
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e0e0e0",
        )
        return fig

    def create_altair_heatmap(self, df, x, y, color, title="Heatmap"):
        chart = (
            alt.Chart(df)
            .mark_rect()
            .encode(x=f"{x}:O", y=f"{y}:O", color=f"{color}:Q", tooltip=[x, y, color])
            .properties(title=title, width=600, height=400)
            .configure_view(strokeWidth=0)
            .configure_axis(grid=False, labelColor="#e0e0e0", titleColor="#e0e0e0")
        )
        return chart
