# Troubleshooting Guide

Find solutions to common issues when using the **Antigravity Agent Factory**.

## Common Issues

### 1. "Jinja2 is required" Error
**Solution**: The factory requires the Jinja2 template engine. Install it using:
```bash
pip install Jinja2
```

### 2. MCP Server Failures
**Issue**: Agents cannot access tools or the filesystem.
**Solution**:
- Ensure the MCP server is installed (e.g., `npm install -g @modelcontextprotocol/server-filesystem`).
- Check that the `command` and `args` in `.agent/mcp.json` are correct for your OS.
- Verify that you have permissions to the directory specified in the arguments.

### 3. Agent Rules not Loading
**Issue**: IDE (Cursor/VS Code) is not picking up the instructions.
**Solution**:
- Ensure the file is named exactly `.agentrules` in the root of your project.
- If you are still using Cursor, it may require a `.agentrules` file or a specific plugin to read `.agentrules`. You can create a symlink:
  ```bash
  # Windows (Run as Admin)
  mklink .agentrules .agentrules
  ```

### 4. Python Import Errors
**Issue**: `ModuleNotFoundError` when running `factory_cli.py`.
**Solution**: Ensure you are running the CLI from the factory root directory, or that you have added the root to your `PYTHONPATH`.

## Getting Help

If you encounter an issue not listed here:
- Open an issue on GitHub.
- Use the `--help` flag with any CLI command.
- Check the [User Guide](USER_GUIDE.md) for detailed usage instructions.
