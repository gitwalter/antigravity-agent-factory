# Azure DevOps MCP Server Setup Guide

This guide walks you through setting up the Azure DevOps MCP server for Antigravity.
## Prerequisites

- Node.js 18+ installed
- An Azure DevOps account and organization
- Antigravity IDE installed
## Step 1: Generate a Personal Access Token (PAT)

1. Sign in to [Azure DevOps](https://dev.azure.com)
2. Click on your profile picture in the top right
3. Select **Personal access tokens**
4. Click **+ New Token**
5. Configure your token:
   - **Name**: Give it a descriptive name (e.g., "Antigravity MCP Azure DevOps")   - **Organization**: Select your organization
   - **Expiration**: Set expiration date (recommended: 90 days)
   - **Scopes**: Select the following:
     - **Code**: Read & Write (for repository access)
     - **Work Items**: Read & Write (for work item management)
     - **Build**: Read (for build information)
     - **Release**: Read (optional, for release information)
     - **Project and Team**: Read (for project access)
6. Click **Create**
7. **Copy the token immediately** - you won't be able to see it again!

## Step 2: Configure Environment Variables

1. Copy `env.template` to `.env` in your project root or user config directory
2. Fill in your Azure DevOps credentials:

```bash
AZURE_DEVOPS_PAT=your_pat_token_here
AZURE_DEVOPS_ORG=yourorganization
AZURE_DEVOPS_PROJECT=yourproject
```

**Note**: 
- Organization name is the part after `dev.azure.com/` in your URL
- Project name is optional but recommended for default operations
- For Azure DevOps Server (on-premises), also set `AZURE_DEVOPS_URL`

## Step 3: Configure Antigravity MCP Settings

1. Open Antigravity Settings (Ctrl+, or Cmd+,)
2. Navigate to **Features** > **Model Context Protocol**
3. Click **Edit Config** or locate your MCP config file:
   - **Windows**: `%APPDATA%\Antigravity\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`
   - **macOS**: `~/Library/Application Support/Antigravity/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
   - **Linux**: `~/.config/Antigravity/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
4. Copy the contents of `mcp-config.json.tmpl` into your MCP config
5. Replace the placeholder variables:
   - `${AZURE_DEVOPS_PAT}` → Your Personal Access Token
   - `${AZURE_DEVOPS_ORG}` → Your organization name
   - `${AZURE_DEVOPS_PROJECT}` → Your default project name

## Step 4: Verify Installation

1. Restart Antigravity
2. Open the MCP panel or check the status indicator
3. The Azure DevOps MCP server should appear as connected
4. Try using Azure DevOps-related commands in Antigravity (e.g., query work items, list repositories)
## Troubleshooting

### Server Not Connecting

- Verify Node.js is installed: `node --version`
- Check that `npx` is available: `npx --version`
- Ensure your PAT is valid and not expired
- Verify your organization name is correct (case-sensitive)
- Check Antigravity's MCP logs for error messages
### Authentication Errors

- Verify your PAT is correct (regenerate if needed)
- Ensure your PAT has the required scopes
- Check that your organization name matches exactly (no spaces, correct casing)
- Verify your account has access to the specified organization and project

### Permission Issues

- Ensure your PAT has the necessary scopes:
  - Code (Read & Write) for repository operations
  - Work Items (Read & Write) for work item operations
  - Build (Read) for build information
- Verify your account has appropriate permissions in Azure DevOps
- Check project-level permissions if accessing specific projects

### Azure DevOps Server (On-Premises)

If using Azure DevOps Server (formerly TFS):

1. Set `AZURE_DEVOPS_URL` in your environment:
```bash
AZURE_DEVOPS_URL=https://tfs.yourcompany.com/tfs
```

2. Update the MCP config to use the custom URL
3. Ensure your PAT is valid for the on-premises instance
4. Verify network connectivity to your Azure DevOps Server

## PAT Scopes Reference

### Required Scopes

- **Code (Read & Write)**: Access repositories, branches, pull requests
- **Work Items (Read & Write)**: Read and create work items, queries
- **Build (Read)**: View build definitions and results

### Optional Scopes

- **Release (Read)**: View release pipelines
- **Test Management (Read)**: Access test plans and results
- **Project and Team (Read)**: Access project and team information

## Security Best Practices

1. **Use Minimal Scopes**: Only grant the permissions you need
2. **Set Expiration Dates**: Use short expiration periods (90 days recommended)
3. **Regular Rotation**: Rotate PATs regularly per your security policy
4. **Never Commit PATs**: Never commit tokens to version control
5. **Use Environment Variables**: Store PATs in secure environment variables
6. **Monitor Usage**: Regularly review PAT usage in Azure DevOps

## Next Steps

- Explore work item management capabilities
- Set up repository access and pull request workflows
- Configure build and release pipeline integration
- Set up additional MCP servers for other services
