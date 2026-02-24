import json
from jinja2 import Template
import os


class TemplateManager:
    """Manages Jinja2-based dashboard and diagram templates."""

    def __init__(
        self, templates_dir="projects/statistical_dashboards/core/layout_templates"
    ):
        self.templates_dir = templates_dir
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir)
        self._initialize_default_templates()

    def _initialize_default_templates(self):
        """Creates basic default templates if they don't exist."""
        # Diagram Template: Scatter Plot
        scatter_tpl = {
            "title": "{{ title|default('Correlation Analysis') }}",
            "labels": {"x": "{{ x_label }}", "y": "{{ y_label }}"},
            "template": "plotly_dark",
            "show_regression": "{{ show_regression|default('false') }}",
        }
        self.save_template("diagrams", "basic_scatter.json", scatter_tpl)

        # Diagram Template: Time Series Line
        line_tpl = {
            "title": "{{ title|default('Trend Analysis') }}",
            "labels": {"x": "{{ x_label|default('Date') }}", "y": "{{ y_label }}"},
            "template": "plotly_dark",
            "line_shape": "spline",
        }
        self.save_template("diagrams", "smooth_line.json", line_tpl)

        # Layout Template: 2x2 Grid
        grid_tpl = """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            {% for chart in charts %}
                <div class="chart-container" style="background: #1c2128; border: 1px solid #30363d; padding: 10px; border-radius: 8px;">
                    {{ chart }}
                </div>
            {% endfor %}
        </div>
        """
        self.save_template("layouts", "grid_2x2.html", grid_tpl)

        # Layout Template: Executive Summary
        exec_tpl = """
        <div style="padding: 20px; border-radius: 12px; background: linear-gradient(135deg, #161b22 0%, #0d1117 100%); border: 1px solid #30363d;">
            <h2 style="color: #58a6ff; margin-top: 0;">{{ title }}</h2>
            <p style="color: #8b949e; font-size: 1.1em;">{{ summary }}</p>
            <div style="margin-top: 20px;">
                {{ content }}
            </div>
        </div>
        """
        self.save_template("layouts", "exec_summary.html", exec_tpl)

    def save_template(self, category, name, content):
        """Saves a template to the filesystem."""
        path = os.path.join(self.templates_dir, category)
        if not os.path.exists(path):
            os.makedirs(path)

        file_path = os.path.join(path, name)
        if isinstance(content, dict):
            with open(file_path, "w") as f:
                json.dump(content, f, indent=4)
        else:
            with open(file_path, "w") as f:
                f.write(content)

    def list_templates(self, category):
        """Lists all templates in a category."""
        path = os.path.join(self.templates_dir, category)
        if not os.path.exists(path):
            return []
        return os.listdir(path)

    def render_diagram_config(self, template_name, **kwargs):
        """Renders a diagram configuration from a Jinja2 template."""
        path = os.path.join(self.templates_dir, "diagrams", template_name)
        if not os.path.exists(path):
            return None

        with open(path, "r") as f:
            tpl_content = f.read()

        # Render the JSON string
        rendered_str = Template(tpl_content).render(**kwargs)
        # Handle "false" string to bool if needed, but simple JSON load is fine
        return json.loads(rendered_str)

    def render_layout(self, template_name, **kwargs):
        """Renders a layout template for HTML components."""
        path = os.path.join(self.templates_dir, "layouts", template_name)
        if not os.path.exists(path):
            return ""

        with open(path, "r") as f:
            tpl_content = f.read()

        return Template(tpl_content).render(**kwargs)
