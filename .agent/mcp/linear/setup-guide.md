# Linear MCP Server Setup Guide

This guide walks you through setting up the Linear MCP server for Cursor using OAuth authentication.

## Prerequisites

- Node.js 18+ installed
- A Linear account
- Cursor IDE installed

## Step 1: Generate a Linear API Key

Linear uses API keys for authentication. You can generate one through Linear's web interface.

### Option A: Personal API Key (Recommended for Individual Use)

1. Go to [Linear Settings > API](https://linear.app/settings/api)
2. Scroll to **Personal API keys**
3. Click **Create API key**
4. Give your key a name (e.g., "Cursor MCP Linear")
5. Select the scopes/permissions you need:
   - **Read**: View issues, projects, teams
   - **Write**: Create and update issues, comments
   - **Admin**: Full access (use with caution)
6. Click **Create**
7. **Copy the API key immediately** - you won't be able to see it again!

### Option B: OAuth Application (For Team/Organization Use)

If you need OAuth-based authentication for team-wide access:

1. Go to [Linear Settings > Applications](https://linear.app/settings/applications)
2. Click **Create application**
3. Fill in application details:
   - **Name**: Cursor MCP Integration
   - **Description**: MCP server integration for Cursor IDE
   - **Redirect URLs**: Not required for MCP server
4. After creating, go to the **API** tab
5. Generate an API key from the application
6. Copy the API key

## Step 2: Configure Environment Variables

1. Create a `.env` file in your project root or user config directory
2. Add your Linear API key:

```bash
LINEAR_API_KEY=lin_api_your_api_key_here
```

**Note**: Linear API keys start with `lin_api_` prefix.

## Step 3: Configure Cursor MCP Settings

1. Open Cursor Settings (Ctrl+, or Cmd+,)
2. Navigate to **Features** > **Model Context Protocol**
3. Click **Edit Config** or locate your MCP config file:
   - **Windows**: `%APPDATA%\Cursor\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`
   - **macOS**: `~/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
   - **Linux**: `~/.config/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`

4. Copy the contents of `mcp-config.json.tmpl` into your MCP config
5. Replace `${LINEAR_API_KEY}` with your actual API key

## Step 4: Verify Installation

1. Restart Cursor
2. Open the MCP panel or check the status indicator
3. The Linear MCP server should appear as connected
4. Try using Linear-related commands in Cursor (e.g., query issues, create tasks)

## OAuth Setup (Advanced)

If you need OAuth-based authentication instead of API keys:

### Step 1: Create OAuth Application

1. Go to [Linear Settings > Applications](https://linear.app/settings/applications)
2. Create a new OAuth application
3. Note your **Client ID** and **Client Secret**

### Step 2: Configure OAuth Flow

The Linear MCP server may support OAuth. Check the server documentation for OAuth configuration options. Typically, you'll need:

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-linear"],
      "env": {
        "LINEAR_CLIENT_ID": "${LINEAR_CLIENT_ID}",
        "LINEAR_CLIENT_SECRET": "${LINEAR_CLIENT_SECRET}",
        "LINEAR_REDIRECT_URI": "http://localhost:3000/callback"
      }
    }
  }
}
```

### Step 3: Complete OAuth Authorization

1. The MCP server will initiate the OAuth flow
2. You'll be redirected to Linear to authorize the application
3. After authorization, the server will receive an access token
4. The token will be stored and used for subsequent requests

## Troubleshooting

### Server Not Connecting

- Verify Node.js is installed: `node --version`
- Check that `npx` is available: `npx --version`
- Ensure your API key is correct and starts with `lin_api_`
- Verify your API key hasn't expired or been revoked
- Check Cursor's MCP logs for error messages

### Authentication Errors

- Verify your API key is correct (regenerate if needed)
- Ensure your API key has the necessary scopes/permissions
- Check that your Linear account is active
- For team workspaces, verify you have access to the workspace

### Permission Issues

- Ensure your API key has the required scopes:
  - **Read**: For querying issues and data
  - **Write**: For creating/updating issues
  - **Admin**: For full access (use sparingly)
- Verify your account has appropriate permissions in Linear
- Check workspace-level permissions if accessing team workspaces

### OAuth-Specific Issues

- Verify your OAuth application is correctly configured
- Check that redirect URIs match your configuration
- Ensure client ID and secret are correct
- Verify the OAuth flow completes successfully
- Check that tokens are being stored correctly

## API Key Scopes Reference

### Read Scope
- View issues, projects, teams
- Query data
- Read comments and attachments

### Write Scope
- Create and update issues
- Add comments
- Update issue status and fields
- Create and update projects

### Admin Scope
- Full access to all resources
- Manage team settings
- Delete resources
- **Use with caution** - grants extensive permissions

## Security Best Practices

1. **Use Minimal Scopes**: Only grant the permissions you need
2. **Rotate Keys Regularly**: Regenerate API keys periodically
3. **Never Commit Keys**: Never commit API keys to version control
4. **Use Environment Variables**: Store keys in secure environment variables
5. **Monitor Usage**: Regularly review API key usage in Linear settings
6. **Revoke Unused Keys**: Delete API keys that are no longer needed
7. **Team Keys**: For team use, prefer OAuth applications over personal API keys

## Next Steps

- Explore Linear issue management capabilities
- Set up team workspace integration
- Configure project and milestone tracking
- Set up additional MCP servers for other services

## Additional Resources

- [Linear API Documentation](https://developers.linear.app/docs)
- [Linear API Reference](https://developers.linear.app/docs/graphql/working-with-the-graphql-api)
- [Linear OAuth Guide](https://developers.linear.app/docs/oauth)
