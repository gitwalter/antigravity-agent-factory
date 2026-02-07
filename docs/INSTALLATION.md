# Installation Guide

Follow these steps to set up the **Antigravity Agent Factory** on your local machine.

## Prerequisites

- **Python 3.9+**: Ensure you have Python installed. Check with `python --version`.
- **Node.js & npm**: Required for running MCP servers.
- **Git**: Required for version control integration.

## Setup Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo/antigravity-agent-factory.git
   cd antigravity-agent-factory
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**
   ```bash
   python cli/factory_cli.py --list-blueprints
   ```

## Configuration

The factory uses a `.env` file for API keys and environment variables. Copy the template:
```bash
cp .env.example .env
```
Edit `.env` to include your `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, or `GEMINI_API_KEY`.
