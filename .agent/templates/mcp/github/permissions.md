# GitHub Personal Access Token Permissions

This document outlines the required scopes (permissions) for the GitHub MCP server.

## Required Scopes

### Repository Scopes

- **`repo`** (Full control of private repositories)
  - Required for: Accessing private repositories, creating/updating issues, PRs, etc.
  - **Note**: This is a broad scope. Consider using fine-grained tokens for better security.

### Alternative: Fine-Grained Token Permissions

If using fine-grained personal access tokens (recommended for better security):

#### Repository Permissions

- **Contents**: Read and Write
  - Read repository contents
  - Create, update, delete files
  - Manage branches and tags

- **Issues**: Read and Write
  - Read and create issues
  - Update issue status and labels
  - Add comments

- **Pull Requests**: Read and Write
  - Read and create pull requests
  - Review pull requests
  - Merge pull requests (if needed)

- **Metadata**: Read-only
  - Access repository metadata (always required)

- **Actions**: Read (optional)
  - View workflow runs and logs

- **Discussions**: Read and Write (optional)
  - Read and create discussions

#### Account Permissions

- **Email addresses**: Read-only (optional)
  - Access user email addresses

## Minimal Scopes for Read-Only Access

If you only need read access:

- **`public_repo`**: Access public repositories
- **`read:org`**: Read organization membership (if accessing org repos)

## Security Best Practices

1. **Use Fine-Grained Tokens**: When available, prefer fine-grained tokens over classic tokens
2. **Principle of Least Privilege**: Only grant the minimum permissions needed
3. **Repository-Specific Tokens**: For fine-grained tokens, limit access to specific repositories
4. **Regular Rotation**: Rotate tokens every 90 days or as per your security policy
5. **Monitor Usage**: Regularly review token usage in GitHub Settings
6. **Expiration Dates**: Set appropriate expiration dates for tokens

## Token Scope Reference

### Classic Token Scopes

- `repo` - Full control of private repositories
- `repo:status` - Access commit status
- `repo_deployment` - Access deployment status
- `public_repo` - Access public repositories
- `read:org` - Read organization membership
- `read:user` - Read user profile data
- `user:email` - Access user email addresses

### Fine-Grained Token Permissions

See [GitHub Documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) for the complete list of fine-grained permissions.

## Recommended Configuration

For most use cases with the GitHub MCP server:

**Classic Token:**
```
Scopes: repo, read:org, user:email
Expiration: 90 days
```

**Fine-Grained Token:**
```
Repository Access: Selected repositories (or all if needed)
Permissions:
  - Contents: Read and Write
  - Issues: Read and Write
  - Pull Requests: Read and Write
  - Metadata: Read-only
Expiration: 90 days
```
