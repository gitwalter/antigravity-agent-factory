# Cursor Agent Factory - Extension Guide

This guide explains how to extend the factory with new patterns, blueprints, and capabilities.

> **Tool Paths:** Commands in this document use default Windows paths from `.cursor/config/tools.json`.
> See [Configuration Guide](CONFIGURATION.md) to customize for your environment.

## Table of Contents

1. [Adding New Blueprints](#adding-new-blueprints)
2. [Creating Agent Patterns](#creating-agent-patterns)
3. [Creating Skill Patterns](#creating-skill-patterns)
4. [Adding Knowledge Files](#adding-knowledge-files) ← **Chat-based or Manual**
5. [Template Development](#template-development)
6. [MCP Server Integration](#mcp-server-integration)
7. [Post-Extension Automation](#post-extension-automation-mandatory) ← **MANDATORY**

## Adding New Blueprints

### Blueprint Structure

```
blueprints/{blueprint-id}/
└── blueprint.json
```

### Blueprint Schema

```json
{
  "metadata": {
    "blueprintId": "my-blueprint",
    "blueprintName": "My Blueprint",
    "description": "Description of this blueprint",
    "version": "1.0.0",
    "tags": ["tag1", "tag2"]
  },
  "stack": {
    "primaryLanguage": "python",
    "frameworks": [
      {"name": "Framework", "version": "1.0+", "purpose": "Purpose"}
    ],
    "tools": [
      {"name": "Tool", "purpose": "Purpose"}
    ]
  },
  "agents": [
    {"patternId": "code-reviewer", "required": true}
  ],
  "skills": [
    {"patternId": "bugfix-workflow", "required": true}
  ],
  "mcpServers": [
    {"name": "server", "url": "https://...", "purpose": "Purpose"}
  ]
}
```

### Example: Adding Go Blueprint

1. Create `blueprints/go-gin/blueprint.json`:

```json
{
  "metadata": {
    "blueprintId": "go-gin",
    "blueprintName": "Go Gin Blueprint",
    "description": "Web API development with Go and Gin",
    "version": "1.0.0",
    "tags": ["go", "gin", "api", "backend"]
  },
  "stack": {
    "primaryLanguage": "go",
    "frameworks": [
      {"name": "Gin", "version": "1.9+", "purpose": "Web framework"}
    ],
    "tools": [
      {"name": "testing", "purpose": "Built-in testing"},
      {"name": "golangci-lint", "purpose": "Linting"}
    ]
  },
  "agents": [
    {"patternId": "code-reviewer", "required": true},
    {"patternId": "test-generator", "required": true}
  ],
  "skills": [
    {"patternId": "bugfix-workflow", "required": true},
    {"patternId": "tdd", "required": true}
  ]
}
```

2. Update `knowledge/stack-capabilities.json` to include Go capabilities.

## Creating Agent Patterns

### Pattern Location

```
patterns/agents/{agent-id}.json
```

### Agent Pattern Schema

```json
{
  "metadata": {
    "patternId": "my-agent",
    "patternName": "My Agent",
    "category": "quality",
    "stackAgnostic": true,
    "description": "What this agent does"
  },
  "frontmatter": {
    "name": "my-agent",
    "description": "Agent description",
    "type": "agent",
    "skills": ["skill-1", "skill-2"],
    "knowledge": ["file.json"]
  },
  "sections": {
    "title": "My Agent",
    "purpose": "Purpose description",
    "whenActivated": ["Trigger 1", "Trigger 2"],
    "workflow": [
      {
        "step": 1,
        "name": "Step Name",
        "description": "What this step does",
        "actions": ["Action 1", "Action 2"]
      }
    ],
    "skillsUsed": [
      {"skill": "skill-1", "purpose": "Why this skill"}
    ],
    "importantRules": ["Rule 1", "Rule 2"]
  }
}
```

### Example: Documentation Agent

```json
{
  "metadata": {
    "patternId": "documentation-agent",
    "patternName": "Documentation Agent",
    "category": "documentation",
    "stackAgnostic": true,
    "description": "Generates and maintains documentation"
  },
  "frontmatter": {
    "name": "documentation-agent",
    "description": "Generate and maintain project documentation",
    "type": "agent",
    "skills": ["documentation-generation"],
    "knowledge": ["doc-templates.json"]
  },
  "sections": {
    "title": "Documentation Agent",
    "purpose": "Generate comprehensive documentation for code and APIs",
    "whenActivated": [
      "When user requests documentation",
      "After new code is created",
      "When API endpoints change"
    ],
    "workflow": [
      {
        "step": 1,
        "name": "Analyze Code",
        "description": "Read and understand the code to document",
        "actions": ["Parse source files", "Identify public interfaces"]
      },
      {
        "step": 2,
        "name": "Generate Documentation",
        "description": "Create documentation content",
        "actions": ["Use doc templates", "Include code examples"]
      }
    ],
    "importantRules": [
      "Document all public interfaces",
      "Include usage examples",
      "Keep documentation synchronized with code"
    ]
  }
}
```

## Creating Skill Patterns

### Pattern Location

```
patterns/skills/{skill-id}.json
```

### Skill Pattern Schema

```json
{
  "metadata": {
    "patternId": "my-skill",
    "patternName": "My Skill",
    "category": "category",
    "stackAgnostic": true,
    "description": "What this skill does",
    "composable": true
  },
  "frontmatter": {
    "name": "my-skill",
    "description": "Skill description",
    "type": "skill",
    "knowledge": ["file.json"]
  },
  "sections": {
    "title": "My Skill",
    "introduction": "Introduction text",
    "whenToUse": ["Use case 1", "Use case 2"],
    "process": [
      {
        "step": 1,
        "name": "Step Name",
        "description": "What this step does",
        "actions": ["Action 1"]
      }
    ],
    "fallbackProcedures": [
      {"condition": "If X fails", "action": "Do Y"}
    ],
    "importantRules": ["Rule 1"]
  }
}
```

### Example: API Documentation Skill

```json
{
  "metadata": {
    "patternId": "api-documentation",
    "patternName": "API Documentation Skill",
    "category": "documentation",
    "stackAgnostic": true,
    "description": "Generate OpenAPI/Swagger documentation",
    "composable": true
  },
  "frontmatter": {
    "name": "api-documentation",
    "description": "Generate API documentation from code",
    "type": "skill",
    "knowledge": ["api-patterns.json"]
  },
  "sections": {
    "title": "API Documentation Skill",
    "introduction": "Generates OpenAPI documentation from API endpoints.",
    "whenToUse": [
      "When creating new API endpoints",
      "When updating existing endpoints",
      "When generating API reference docs"
    ],
    "process": [
      {
        "step": 1,
        "name": "Scan Endpoints",
        "description": "Find all API endpoints",
        "actions": ["Parse route definitions", "Extract HTTP methods"]
      },
      {
        "step": 2,
        "name": "Extract Schemas",
        "description": "Get request/response schemas",
        "actions": ["Parse model definitions", "Extract validation rules"]
      },
      {
        "step": 3,
        "name": "Generate OpenAPI",
        "description": "Create OpenAPI specification",
        "actions": ["Create paths section", "Create components section"]
      }
    ],
    "fallbackProcedures": [
      {"condition": "If schema cannot be inferred", "action": "Ask user for type information"}
    ]
  }
}
```

## Adding Knowledge Files

There are **two ways** to extend the Factory's knowledge base:

### Method 1: Chat-Based Extension (Recommended)

Simply ask in chat:

```
"Extend knowledge for [topic]"
"Add knowledge about [subject]"
"Create a skill for [purpose]"
"Incorporate this document: [path or URL]"
```

The **knowledge-extender agent** will:
1. Research the topic (web search, documents, or your input)
2. Generate structured JSON following templates
3. Execute **Post-Extension Automation** (Rule 6):
   - Update `knowledge/manifest.json`
   - Update `knowledge/skill-catalog.json` (if skill)
   - Update `docs/reference/KNOWLEDGE_FILES.md`
   - Update `docs/reference/FACTORY_COMPONENTS.md` (if Factory component)
   - Update `CHANGELOG.md`
   - Run `scripts/validation/sync_manifest_versions.py --sync`
   - Run `scripts/validation/validate_readme_structure.py --update`
4. Ask before git commit/push

**See:** `.cursor/skills/extend-knowledge/SKILL.md` for full procedures.

### Method 2: Manual File Creation

For fine-grained control, create files manually:

### Knowledge File Location

Factory knowledge: `knowledge/{topic}.json`
Generated project knowledge: Copied to `{TARGET}/knowledge/`

### Knowledge File Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Knowledge Title",
  "description": "What this knowledge contains",
  "version": "1.0.0",
  "data": {
    // Your queryable data structure
  }
}
```

### Design for Querying

Structure data so agents can easily query it:

```json
{
  "conventions": {
    "variables": "snake_case",
    "classes": "PascalCase"
  },
  "patterns": {
    "service": {
      "naming": "{Domain}Service",
      "methods": ["create", "read", "update", "delete"]
    }
  }
}
```

### Example: API Patterns Knowledge

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "API Patterns",
  "description": "Common API design patterns",
  "version": "1.0.0",
  "restPatterns": {
    "endpoints": {
      "list": "GET /{resource}",
      "get": "GET /{resource}/{id}",
      "create": "POST /{resource}",
      "update": "PUT /{resource}/{id}",
      "delete": "DELETE /{resource}/{id}"
    },
    "statusCodes": {
      "success": {"200": "OK", "201": "Created", "204": "No Content"},
      "clientError": {"400": "Bad Request", "401": "Unauthorized", "404": "Not Found"},
      "serverError": {"500": "Internal Server Error"}
    }
  }
}
```

## Template Development

### Template Types

1. **Code Templates** - Generating source code
2. **Document Templates** - Generating markdown documentation
3. **Configuration Templates** - Generating config files

### Code Template Example

`templates/{language}/service-class/service.py`:

```python
"""
{CLASS_NAME} Service

{DESCRIPTION}
"""

from typing import List, Optional
from {MODULE_PATH}.models import {MODEL_NAME}
from {MODULE_PATH}.repository import {REPOSITORY_NAME}


class {CLASS_NAME}:
    """Service for managing {ENTITY_NAME} operations."""
    
    def __init__(self, repository: {REPOSITORY_NAME}):
        """Initialize the service.
        
        Args:
            repository: Repository for data access.
        """
        self._repository = repository
    
    def get_by_id(self, id: int) -> Optional[{MODEL_NAME}]:
        """Get {ENTITY_NAME} by ID.
        
        Args:
            id: The {ENTITY_NAME} ID.
            
        Returns:
            The {ENTITY_NAME} if found, None otherwise.
        """
        return self._repository.get(id)
    
    def get_all(self) -> List[{MODEL_NAME}]:
        """Get all {ENTITY_NAME}s.
        
        Returns:
            List of all {ENTITY_NAME}s.
        """
        return self._repository.get_all()
```

### Variable Conventions

| Variable | Description |
|----------|-------------|
| `{CLASS_NAME}` | Class name (PascalCase) |
| `{METHOD_NAME}` | Method name (snake_case for Python) |
| `{FILE_NAME}` | File name |
| `{ENTITY_NAME}` | Entity/model name |
| `{DESCRIPTION}` | Description text |

## MCP Server Integration

### Adding New MCP Server

1. Add to `knowledge/mcp-servers-catalog.json`:

```json
{
  "my-server": {
    "name": "My Server",
    "description": "What it does",
    "url": "https://my-server.example.com/mcp",
    "authentication": "none",
    "capabilities": ["capability1", "capability2"],
    "tools": [
      {"name": "tool1", "description": "What tool1 does"}
    ],
    "suggestedFor": ["skill-1", "skill-2"],
    "configExample": {
      "my-server": {
        "url": "https://my-server.example.com/mcp",
        "headers": {}
      }
    }
  }
}
```

2. Reference in blueprints that need it:

```json
{
  "mcpServers": [
    {"name": "my-server", "purpose": "Purpose", "required": false}
  ]
}
```

### Configuring Authentication

For servers requiring authentication, document in the catalog:

```json
{
  "authentication": "api-key",
  "authenticationNote": "Set MYSERVER_API_KEY environment variable",
  "configExample": {
    "my-server": {
      "url": "https://...",
      "headers": {
        "Authorization": "Bearer ${MYSERVER_API_KEY}"
      }
    }
  }
}
```

## Post-Extension Automation (MANDATORY)

After extending ANY artifact, you MUST complete these steps (enforced by `.cursorrules` Rule 6):

### Quick Reference

| Artifact Type | Must Update |
|---------------|-------------|
| Knowledge file (new) | manifest.json + KNOWLEDGE_FILES.md + CHANGELOG.md |
| Knowledge file (extend) | manifest.json (version) + CHANGELOG.md |
| Skill (new) | skill-catalog.json + CHANGELOG.md |
| Factory skill/agent | FACTORY_COMPONENTS.md + CHANGELOG.md |
| Blueprint (new) | BLUEPRINTS.md + CHANGELOG.md |

### Automation Scripts

```powershell
# Sync versions from source files (single source of truth)
python scripts/validation/sync_manifest_versions.py --sync

# Validate README counts match filesystem
python scripts/validation/validate_readme_structure.py --update
```

### Dependency Map

See `knowledge/artifact-dependencies.json` for the complete mapping of:
- `update_rules` - What must be updated for each artifact type
- `documentation_map` - Exact sections to update in each doc
- `factory_artifact_detection` - List of Factory components
- `post_extension_checklist` - Step-by-step automation

---

## Testing Extensions

### Verify Patterns Load

```powershell
C:\App\Anaconda\python.exe cli\factory_cli.py --list-patterns
```

### Test Blueprint Generation

```powershell
C:\App\Anaconda\python.exe cli\factory_cli.py ^
    --blueprint my-blueprint ^
    --output C:\Temp\test-output
```

### Verify Generated Structure

Check that:
1. All agents are created in `.cursor/agents/`
2. All skills are created in `.cursor/skills/`
3. Knowledge files are copied to `knowledge/`
4. `.cursorrules` contains correct configuration

---

For more details, see the main [README.md](../README.md).
