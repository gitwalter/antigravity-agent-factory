---
## Overview

description: How to migrate an existing skill to the new Jinja2 template format
---
# Migrate Skill to Jinja2 Template

Use this workflow to migrate an existing static Markdown skill to the new Jinja2 template format (`.j2`).

**Version:** 1.0.0

## Trigger Conditions

This workflow is activated when:
- Existing skill needs migration to Jinja2
- Standardizing skill format requested
- Refactoring skill templates

**Trigger Examples:**
- "Migrate the web-browsing skill to Jinja2"
- "Convert this skill to the new template format"

## Steps

1.  **Identify Skill**
    *   Navigate to `.agent/skills/<skill-name>`.
    *   Open `SKILL.md` to reference the existing content.

2.  **Create Template File**
    *   Create a new file `.agent/templates/skills/<skill-name>/SKILL.md.j2`.
    *   **Note**: The directory structure in `templates` must match the `skills` ID.

3.  **Extend Base Template**
    *   Start the file with:
        ```jinja2
        {% extends "skills/base_skill.md.j2" %}
        ```

4.  **Import Macros**
    *   Add the macros import:
        ```jinja2
        {% from "_macros/skills.tmpl" import capabilities_section, troubleshooting_guide, checklist, resource_list, usage_context %}
        ```

5.  **Migrate Content Blocks**
    *   **Summary**: The summary is automatically pulled from the pattern introduction or frontmatter. You generally don't need to manually add it unless overriding.
    *   **Capabilities**:
        ```jinja2
        {% block capabilities %}
        {{ capabilities_section([
            {'title': 'Capability 1', 'description': 'Description...'},
            {'title': 'Capability 2', 'description': 'Description...'}
        ]) }}
        {% endblock %}
        ```
    *   **Usage**:
        ```jinja2
        {% block usage %}
        {{ usage_context(project_name) }}
        Add specific usage instructions here.
        {% endblock %}
        ```
    *   **Troubleshooting**:
        ```jinja2
        {% block troubleshooting %}
        {{ troubleshooting_guide([
            {'problem': 'Problem', 'cause': 'Cause', 'solution': 'Solution'}
        ]) }}
        {% endblock %}
        ```
    *   **Resources**:
        ```jinja2
        {% block resources %}
        {{ resource_list([
            {'title': 'Title', 'url': 'URL', 'description': 'Description'}
        ]) }}
        {% endblock %}
        ```
    *   **Other Sections**: use `{% block additional_sections %}` for anything that doesn't fit standard blocks.

6.  **Verify**
    *   Run `python scripts/debug/verify_skills.py` (you may need to modify the script to target your specific skill ID) to ensure it renders correctly.

// turbo
7.  **Delete Legacy File** (Optional)
    *   Once verified, you *could* remove the static `SKILL.md` from the `patterns` or `skills` source, but usually, we keep the pattern as data and just use the template for rendering.


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
