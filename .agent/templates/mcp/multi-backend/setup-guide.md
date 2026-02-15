# Multi-Backend MCP Server Setup Guide

This guide walks you through setting up multiple MCP servers simultaneously in Antigravity, allowing you to integrate with GitHub, Atlassian, Azure DevOps, Linear, and other services.

## Overview

The multi-backend configuration allows you to use multiple MCP servers at once, giving you access to tools and resources from different platforms within Antigravity. This is useful when your workflow spans multiple services.
## Prerequisites

- Node.js 18+ installed
- Accounts for the services you want to integrate
- Antigravity IDE installed- API tokens/keys for each service

## Step 1: Gather All Required Credentials

Before configuring, ensure you have credentials for each service:

### GitHub
- Personal Access Token (PAT)
- See `../github/setup-guide.md` for details

### Atlassian
- API Token
- Domain name
- Email address
- See `../atlassian/setup-guide.md` for details

### Azure DevOps
- Personal Access Token (PAT)
- Organization name
- Project name (optional)
- See `../azure-devops/setup-guide.md` for details

### Linear
- API Key
- See `../linear/setup-guide.md` for details

## Step 2: Configure Environment Variables

Create a comprehensive `.env` file with all your credentials:

```bash
# GitHub
GITHUB_TOKEN=ghp_your_github_token_here

# Atlassian
ATLASSIAN_DOMAIN=yourcompany
ATLASSIAN_EMAIL=your.email@example.com
ATLASSIAN_API_TOKEN=your_atlassian_token_here

# Azure DevOps
AZURE_DEVOPS_PAT=your_azure_devops_pat_here
AZURE_DEVOPS_ORG=yourorganization
AZURE_DEVOPS_PROJECT=yourproject

# Linear
LINEAR_API_KEY=lin_api_your_linear_key_here
```

**Security Note**: Never commit this file to version control. Add `.env` to your `.gitignore`.

## Step 3: Configure Antigravity MCP Settings

1. Open Antigravity Settings (Ctrl+, or Cmd+,)
2. Navigate to **Features** > **Model Context Protocol**
3. Click **Edit Config** or locate your MCP config file:
   - **Windows**: `%APPDATA%\Antigravity\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`
   - **macOS**: `~/Library/Application Support/Antigravity/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
   - **Linux**: `~/.config/Antigravity/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
4. Copy the contents of `combined-config.json.tmpl` into your MCP config
5. Replace all placeholder variables with your actual credentials

## Step 4: Selective Server Configuration

You don't need to enable all servers. You can selectively include only the ones you need:

### Minimal Configuration (GitHub Only)

```json
{
  "mcpServers": {
    "github-pm": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### GitHub + Atlassian

```json
{
  "mcpServers": {
    "github-pm": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "atlassian-cloud": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-atlassian"],
      "env": {
        "ATLASSIAN_API_TOKEN": "${ATLASSIAN_API_TOKEN}",
        "ATLASSIAN_DOMAIN": "${ATLASSIAN_DOMAIN}",
        "ATLASSIAN_EMAIL": "${ATLASSIAN_EMAIL}"
      }
    }
  }
}
```

### Custom Combination

Mix and match servers based on your needs. Each server is independent and can be added or removed without affecting others.

## Step 5: Verify Installation

1. Restart Antigravity2. Open the MCP panel or check the status indicator
3. All configured MCP servers should appear as connected
4. Test each service:
   - Try GitHub commands (e.g., list repositories)
   - Try Atlassian commands (e.g., query Jira issues)
   - Try Azure DevOps commands (e.g., list work items)
   - Try Linear commands (e.g., query issues)

## Troubleshooting

### Individual Server Issues

If one server fails to connect:

1. Check that server's specific configuration
2. Verify its credentials are correct
3. Review that server's setup guide for troubleshooting
4. Check Antigravity's MCP logs for specific error messages
### Environment Variable Issues

- Ensure all variables are set in your `.env` file
- Verify variable names match exactly (case-sensitive)
- Check that your `.env` file is in the correct location
- Some systems may require restarting Antigravity after changing `.env`
### Performance Considerations

- Running multiple MCP servers may increase resource usage
- Each server runs as a separate process
- Monitor system resources if experiencing slowdowns
- Consider disabling unused servers to improve performance

### Conflicting Server Names

If you need multiple instances of the same service (e.g., two GitHub accounts):

1. Use unique server names:
```json
{
  "mcpServers": {
    "github-personal": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_TOKEN}"
      }
    },
    "github-work": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_WORK_TOKEN}"
      }
    }
  }
}
```

2. Use different environment variables for each instance

## Best Practices

### Security

1. **Use Environment Variables**: Never hardcode credentials in config files
2. **Separate Credentials**: Use different tokens for different services
3. **Regular Rotation**: Rotate tokens regularly per your security policy
4. **Principle of Least Privilege**: Grant minimal required permissions
5. **Secure Storage**: Use secure credential storage solutions when possible

### Organization

1. **Document Your Setup**: Keep notes on which servers you use and why
2. **Version Control**: Commit your config template (without secrets) to version control
3. **Team Sharing**: Share setup guides with your team, not credentials
4. **Regular Audits**: Periodically review which servers you actually use

### Performance

1. **Disable Unused Servers**: Remove servers you don't actively use
2. **Monitor Resources**: Keep an eye on system resource usage
3. **Start Small**: Begin with one or two servers, add more as needed
4. **Test Incrementally**: Add servers one at a time and verify each works

## Common Use Cases

### Development Workflow
- **GitHub** + **Linear**: Code repositories + issue tracking
- **GitHub** + **Atlassian**: Code + project management

### Enterprise Workflow
- **Azure DevOps** + **Atlassian**: Enterprise tools integration
- **GitHub** + **Azure DevOps**: Multi-platform development

### Full Stack Integration
- **GitHub** + **Atlassian** + **Linear**: Complete development ecosystem

## Next Steps

- Explore cross-platform workflows (e.g., create GitHub PR from Linear issue)
- Set up automated workflows using multiple services
- Configure service-specific filters and preferences
- Add additional MCP servers as needed

## Additional Resources

- Individual setup guides in each service's directory
- [MCP Protocol Documentation](https://modelcontextprotocol.io)
- [Antigravity MCP Documentation](https://cursor.sh/docs/mcp)
