# MCP Server Selection Skill

## Purpose

Guide users through selecting appropriate MCP servers during project generation based on their role, technology stack, and specific needs.

## Trigger Conditions

- User is generating a new project with the factory
- User asks about MCP server options or recommendations
- Phase 6 of interactive project generation
- User wants to configure MCP servers for existing project

## Skill Flow

### Step 1: Determine User Role

Ask the user about their primary role:

```
What is your primary role?
1. Full-Stack Developer
2. Frontend Developer
3. Backend Developer
4. Data Scientist
5. ML Engineer
6. Agent Developer
7. DevOps Engineer
8. SAP Developer
```

### Step 2: Offer Starter Pack or Custom Selection

Based on role, offer pre-configured starter packs:

```
Would you like to start with a pre-configured pack?

1. Minimal Starter (3 servers)
   - filesystem, git, memory
   
2. Web Developer Starter (6 servers)
   - + github, postgresql, playwright
   
3. Data Science Starter (6 servers)
   - + jupyter, bigquery, pinecone
   
4. AI Agent Starter (6 servers)
   - + langgraph, knowledge-graph, chromadb
   
5. Enterprise Starter (7 servers)
   - + atlassian, slack, sentry

6. Custom Selection
   - Browse all categories
```

### Step 3: Category Browsing (if Custom)

Present servers by category:

```
## Category 1: Essential/Core Tools (Recommended for ALL)
[ ] filesystem - File operations
[ ] git - Git repository operations
[ ] memory - Persistent knowledge graph
[ ] time - Date/time utilities
[ ] fetch - Web content retrieval
[ ] brave-search - Web search (free tier)
[ ] sequentialthinking - Structured problem-solving

## Category 2: Code, Testing, Version Control
[ ] github - GitHub integration
[ ] gitlab - GitLab integration
[ ] sentry - Error tracking
[ ] playwright - Browser automation
[ ] deepwiki - GitHub repo documentation

## Category 3: Data and Databases
[ ] postgresql - PostgreSQL database
[ ] mongodb - MongoDB database
[ ] bigquery - Google BigQuery
[ ] pinecone - Vector database
[ ] chromadb - Local embeddings

... (continue for all categories)
```

### Step 4: Custom/Local Servers

Ask about team-specific servers:

```
Does your team have custom or local MCP servers?
- If yes, collect:
  - Server name
  - Command to run (e.g., python, npx)
  - Arguments
  - Required environment variables
  - Description
```

### Step 5: Generate Configuration

After selection, generate:

1. **MCP config for project** (`.cursor/mcp.json`)
2. **Environment template** (`.env.mcp`)
3. **Setup checklist** in README

## Reference Data

Load recommendations from:
- `knowledge/mcp-servers-catalog.json` - Full server catalog
- `knowledge/mcp-selection-guide.json` - Role/stack recommendations

## Smart Suggestions

### Based on Technology Stack

```python
def suggest_by_stack(stack):
    suggestions = {
        "python": ["filesystem", "git", "memory", "github", "postgresql", "sentry"],
        "typescript": ["filesystem", "git", "memory", "github", "postgresql", "playwright"],
        "nextjs": ["filesystem", "git", "memory", "github", "playwright", "figma"],
        "fastapi": ["filesystem", "git", "memory", "github", "postgresql", "openapi"],
        ...
    }
    return suggestions.get(stack, ["filesystem", "git", "memory"])
```

### Based on Selected Triggers

If user selected workflow triggers:
- `jira` or `confluence` → Add `atlassian`
- `github` → Add `github`, `deepwiki`
- `slack` → Add `slack`
- `sentry` → Add `sentry`

### Based on Role

See `roleToServers` in `mcp-selection-guide.json`

## Output Format

### MCP Configuration File

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "${PROJECT_PATH}"]
    },
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git", "--repository", "."]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### Environment Template

```bash
# MCP Server Environment Variables
# Copy to .env and fill in values

# GitHub (if using github server)
GITHUB_TOKEN=your-github-token

# Brave Search (if using brave-search server)
BRAVE_API_KEY=your-brave-api-key

# Database (if using postgresql server)
DATABASE_URL=postgresql://user:pass@host:5432/db
```

### README Section

```markdown
## MCP Server Configuration

This project uses the following MCP servers:

| Server | Purpose | Setup Required |
|--------|---------|----------------|
| filesystem | File operations | None |
| git | Git operations | None |
| memory | Persistent context | None |
| github | GitHub integration | Set GITHUB_TOKEN |

### Setup Steps

1. Copy `.env.mcp.template` to `.env.mcp`
2. Fill in required API keys and tokens
3. Restart Cursor to activate MCP servers

### Verification

Ask the AI to verify each server:
- "Show git status"
- "List files in the project"
- "What do you remember about this project?"
```

## Best Practices

1. **Always include core servers** - filesystem, git, memory are recommended for all projects
2. **Start minimal** - Begin with starter pack, add servers as needed
3. **Document authentication** - Always include setup instructions for servers requiring auth
4. **Test verification** - Include commands to verify each server works
5. **Environment separation** - Keep MCP env vars in separate `.env.mcp` file

## Error Handling

- If server catalog not found, use built-in defaults
- If authentication fails, provide clear setup instructions
- If server not responding, suggest troubleshooting steps

## Related Files

- `knowledge/mcp-servers-catalog.json` - Full catalog
- `knowledge/mcp-selection-guide.json` - Recommendations
- `templates/mcp/*/setup-guide.md` - Per-server setup guides
- `docs/MCP-SERVERS.md` - Comprehensive documentation
