# Atlassian MCP Server Setup Guide

This guide walks you through setting up the Atlassian MCP server for Antigravity, supporting both Atlassian Cloud and self-hosted instances.

## Prerequisites

- Node.js 18+ installed
- An Atlassian account (Cloud) or access to Atlassian Server/Data Center
- Antigravity IDE installed

## Step 1: Generate an API Token

### For Atlassian Cloud

1. Go to [Atlassian Account Settings > Security > API tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click **Create API token**
3. Give your token a label (e.g., "Antigravity MCP Atlassian")
4. Click **Create**
5. **Copy the token immediately** - you won't be able to see it again!

### For Self-Hosted/Server Instances

1. Log in to your Atlassian instance
2. Go to **Account Settings** > **Security** > **API Tokens**
3. Create a new API token following your organization's security policies
4. Copy the token securely

## Step 2: Configure Environment Variables

1. Copy `env.template` to `.env` in your project root or user config directory
2. Fill in your Atlassian credentials:

```bash
ATLASSIAN_DOMAIN=yourcompany
ATLASSIAN_EMAIL=your.email@example.com
ATLASSIAN_API_TOKEN=your_api_token_here
```

**For Cloud**: Use your domain name (the part before `.atlassian.net`)

**For Self-Hosted**: Set `ATLASSIAN_BASE_URL` instead of `ATLASSIAN_DOMAIN`:
```bash
ATLASSIAN_BASE_URL=https://jira.yourcompany.com
ATLASSIAN_EMAIL=your.email@example.com
ATLASSIAN_API_TOKEN=your_api_token_here
```

## Step 3: Choose Configuration Type

### Option A: Cloud Configuration (Recommended)

Use `mcp-config-cloud.json.tmpl` for Atlassian Cloud instances. This uses the npm package directly.

### Option B: Local Configuration

Use `mcp-config-local.json.tmpl` if you've installed the MCP server locally or need custom configuration.

1. Install the MCP server locally (if needed):
```bash
npm install -g @modelcontextprotocol/server-atlassian
# or clone and build from source
```

2. Set `MCP_ATLASSIAN_LOCAL_PATH` in your `.env` file

## Step 4: Configure Antigravity MCP Settings

1. Open Antigravity Settings (Ctrl+, or Cmd+,)
2. Navigate to **Features** > **Model Context Protocol**
3. Click **Edit Config** or locate your MCP config file:
   - **Windows**: `%APPDATA%\Antigravity\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`
   - **macOS**: `~/Library/Application Support/Antigravity/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
   - **Linux**: `~/.config/Antigravity/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`

4. Copy the contents of your chosen config template (`mcp-config-cloud.json.tmpl` or `mcp-config-local.json.tmpl`)
5. Replace the placeholder variables:
   - `${ATLASSIAN_DOMAIN}` → Your Atlassian domain
   - `${ATLASSIAN_EMAIL}` → Your email
   - `${ATLASSIAN_API_TOKEN}` → Your API token
   - `${ATLASSIAN_BASE_URL}` → Your base URL (self-hosted only)

## Step 5: Verify Installation

1. Restart Antigravity
2. Open the MCP panel or check the status indicator
3. The Atlassian MCP server should appear as connected
4. Try using Atlassian-related commands in Antigravity (e.g., query Jira issues)

## Troubleshooting

### Server Not Connecting

- Verify Node.js is installed: `node --version`
- Check that `npx` is available: `npx --version`
- Verify your domain/base URL is correct
- Ensure your API token is valid and not expired
- Check Antigravity's MCP logs for error messages

### Authentication Errors

- Verify your email matches your Atlassian account
- Ensure your API token is correct (regenerate if needed)
- For Cloud: Check that your domain doesn't include `.atlassian.net`
- For Self-Hosted: Verify the base URL is accessible and correct

### Permission Issues

- Ensure your account has appropriate permissions in Atlassian
- Check that your API token has the necessary scopes
- Verify you can access the projects/issues you're trying to query

### Self-Hosted Specific Issues

- Verify your instance URL is accessible from your machine
- Check firewall/network settings
- Ensure SSL certificates are valid (if using HTTPS)
- Some self-hosted instances may require additional authentication

## Next Steps

- Explore Jira issue management capabilities
- Set up Confluence integration (if available)
- Configure project-specific filters
- Set up additional MCP servers for other services

## Security Notes

- Never commit API tokens to version control
- Use environment variables or secure credential storage
- Rotate tokens regularly per your security policy
- Use the principle of least privilege for API token permissions
