# GitHub MCP Server Setup Guide

This guide walks you through setting up the GitHub MCP server for Antigravity.
## Prerequisites

- Node.js 18+ installed
- A GitHub account
- Antigravity IDE installed
## Step 1: Generate a Personal Access Token

1. Go to [GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)](https://github.com/settings/tokens)
2. Click **Generate new token** > **Generate new token (classic)**
3. Give your token a descriptive name (e.g., "Antigravity MCP GitHub")4. Set an expiration date (recommended: 90 days or custom)
5. Select the required scopes (see `permissions.md` for details)
6. Click **Generate token**
7. **Copy the token immediately** - you won't be able to see it again!

## Step 2: Configure Environment Variables

1. Copy `env.template` to `.env` in your project root or user config directory
2. Replace `your_github_personal_access_token_here` with your actual token:

```bash
GITHUB_TOKEN=ghp_your_actual_token_here
```

## Step 3: Configure Antigravity MCP Settings

1. Open Antigravity Settings (Ctrl+, or Cmd+,)
2. Navigate to **Features** > **Model Context Protocol**
3. Click **Edit Config** or locate your MCP config file:
   - **Windows**: `%APPDATA%\Antigravity\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`
   - **macOS**: `~/Library/Application Support/Antigravity/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
   - **Linux**: `~/.config/Antigravity/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
4. Copy the contents of `mcp-config.json.tmpl` into your MCP config
5. Replace `${GITHUB_TOKEN}` with your actual token, or ensure your `.env` file is loaded

## Step 4: Verify Installation

1. Restart Antigravity
2. Open the MCP panel or check the status indicator
3. The GitHub MCP server should appear as connected
4. Try using GitHub-related commands in Antigravity
## Troubleshooting

### Server Not Connecting

- Verify Node.js is installed: `node --version`
- Check that `npx` is available: `npx --version`
- Ensure your token has the correct permissions
- Check Antigravity's MCP logs for error messages
### Permission Errors

- Review `permissions.md` for required scopes
- Regenerate your token with the correct scopes
- Ensure the token hasn't expired

### Token Security

- Never commit your token to version control
- Use environment variables or secure credential storage
- Rotate tokens regularly
- Use fine-grained tokens when possible (GitHub feature)

## Next Steps

- Review available GitHub MCP tools in Antigravity- Explore GitHub repository management capabilities
- Set up additional MCP servers for other services
