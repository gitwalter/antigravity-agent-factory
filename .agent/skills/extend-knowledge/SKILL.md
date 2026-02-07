---
name: extend-knowledge
description: Extend Factory knowledge, skills, and templates via research, documents, or user links
type: skill
agents: [knowledge-extender]
templates: [knowledge/knowledge-file.tmpl, factory/skill.md.tmpl, factory/agent.md.tmpl]
patterns: [knowledge/knowledge-schema.json]
knowledge: [agent-taxonomy]
---

# Extend Knowledge Skill

Extend the Factory's knowledge base, skills, and templates through multiple research methods:
- **Web Search**: Use `web_search` tool to find current information
- **Document Reading**: Read files, PDFs, or code repositories
- **User Links**: Process URLs provided by users in chat
- **Synthesis**: Combine sources into structured Factory artifacts

## Artifacts Used

| Artifact | Path | Purpose |
|----------|------|---------|
| Knowledge Template | `templates/knowledge/knowledge-file.tmpl` | JSON structure for knowledge |
| Skill Template | `templates/factory/skill.md.tmpl` | Markdown structure for skills |
| Agent Template | `templates/factory/agent.md.tmpl` | Markdown structure for agents |
| Schema | `patterns/knowledge/knowledge-schema.json` | Validation rules |
| Taxonomy | `scripts/taxonomy/agent_taxonomy.json` | Topic definitions |

## When to Use

- Gap analysis identified missing or shallow topics
- User requests knowledge extension on a topic
- User provides links or documents to incorporate
- Blueprint needs artifacts that don't exist
- New patterns or frameworks need documentation

## Research Methods

### Method 1: Web Search Research

Use when: Topic needs current, online information

**Tool**: `web_search`

```
Step 1: web_search("{{topic}} best practices patterns 2026")
Step 2: web_search("{{topic}} implementation examples")
Step 3: web_search("{{topic}} common pitfalls anti-patterns")
```

**What I Do**:
1. Execute web searches for the topic
2. Read and synthesize results
3. Extract patterns, examples, best practices
4. Cite sources in the knowledge file

### Method 2: Document Reading

Use when: User has existing docs, code, or files to incorporate

**Tool**: `read_file`

```
Step 1: read_file("{{path_to_document}}")
Step 2: Extract key patterns and concepts
Step 3: Transform into structured knowledge
```

**Supported Formats**:
- Markdown files (`.md`)
- JSON files (`.json`)
- Python/TypeScript code (extract patterns)
- YAML configuration files
- Text documentation

### Method 3: User-Provided Links

Use when: User shares URLs in chat

**Process**:
1. User provides URL: "Add knowledge from https://example.com/article"
2. I use `web_search` with site-specific query: `web_search("site:example.com {{topic}}")`
3. Synthesize findings into knowledge structure
4. Cite the source URL

**Example**:
```
User: Extend knowledge using https://docs.anthropic.com/constitutional-ai

Agent: I'll research Constitutional AI from Anthropic's docs...
[web_search("site:docs.anthropic.com constitutional AI principles")]
[Synthesizes findings]
[Creates knowledge/constitutional-ai-patterns.json]
```

### Method 4: Repository Analysis

Use when: Learning from code repositories

**Tools**: `list_dir`, `read_file`, `grep`

```
Step 1: list_dir("{{repo_path}}") - Understand structure
Step 2: grep("pattern|implementation", "{{repo_path}}") - Find key code
Step 3: read_file("{{interesting_files}}") - Analyze implementation
Step 4: Synthesize patterns into knowledge
```

## Extension Procedures

### Procedure A: Create Knowledge File

**Trigger**: "Extend knowledge for {{topic}}", "Add knowledge about {{topic}}"

**Steps**:

1. **Check Existing Knowledge**
   ```
   list_dir("knowledge")
   → See what already exists
   ```

2. **Read Taxonomy**
   ```
   read_file("scripts/taxonomy/agent_taxonomy.json")
   → Understand topic requirements (depth, keywords)
   ```

3. **Read Template**
   ```
   read_file("templates/knowledge/knowledge-file.tmpl")
   → Get JSON structure to follow
   ```

4. **Read Schema**
   ```
   read_file("patterns/knowledge/knowledge-schema.json")
   → Get validation rules (min 3 patterns)
   ```

5. **Research Topic** (one or more methods)
   ```
   web_search("{{topic}} best practices 2026")
   web_search("{{topic}} implementation patterns")
   read_file("{{user_provided_doc}}") if provided
   ```

6. **Generate Content**
   - Synthesize research into JSON structure
   - Include at least 3 patterns
   - Add code examples
   - Cite sources

7. **Write File**
   ```
   write("knowledge/{{topic-name}}-patterns.json", content)
   ```

8. **Validate**
   ```
   read_file("knowledge/{{topic-name}}-patterns.json")
   → Verify JSON is valid
   ```

**Output**: `knowledge/{topic}-patterns.json` (50-200 lines)

---

### Procedure B: Create New Skill

**Trigger**: "Create skill for {{purpose}}", "Add a skill that {{does_what}}"

**Steps**:

1. **Check Existing Skills**
   ```
   list_dir(".agent/skills")
   → See what already exists, avoid duplicates
   ```

2. **Read Skill Template**
   ```
   read_file("templates/factory/skill.md.tmpl")
   → Get markdown structure
   ```

3. **Read Example Skill** (for reference)
   ```
   read_file(".agent/skills/extend-knowledge/SKILL.md")
   → See good skill structure
   ```

4. **Research if Needed**
   ```
   web_search("{{purpose}} workflow best practices")
   ```

5. **Generate Skill Content**
   - Fill template placeholders
   - Define clear process steps
   - Include tool usage examples
   - Add fallback procedures

6. **Create Skill Directory**
   ```
   write(".agent/skills/{{skill-name}}/SKILL.md", content)
   ```

**Output**: `.agent/skills/{skill-name}/SKILL.md`

**Skill Template Structure**:
```markdown
---
name: {{skill-name}}
description: {{what it does}}
type: skill
agents: [{{which agents use it}}]
templates: [{{templates used}}]
knowledge: [{{knowledge referenced}}]
---

# {{Skill Title}}

## When to Use
{{conditions for using this skill}}

## Process
### Step 1: {{action}}
### Step 2: {{action}}

## What Gets Created/Changed
| Action | File | Change |

## Fallback Procedures
| Issue | Resolution |
```

---

### Procedure C: Create New Template

**Trigger**: "Create template for {{purpose}}", "Add a {{type}} template"

**Steps**:

1. **Determine Template Category**
   ```
   list_dir("templates")
   → Find appropriate category folder
   ```

2. **Read Similar Template** (for style)
   ```
   read_file("templates/{{category}}/{{similar}}.tmpl")
   → Understand existing conventions
   ```

3. **Design Template**
   - Identify placeholders needed (`{{VARIABLE_NAME}}`)
   - Structure for target file type
   - Include helpful comments

4. **Write Template**
   ```
   write("templates/{{category}}/{{name}}.tmpl", content)
   ```

**Output**: `templates/{category}/{name}.tmpl`

**Template Conventions**:
- Use `{{VARIABLE_NAME}}` for placeholders
- Use `{# comment #}` for template comments
- Include header documenting all variables

---

### Procedure D: Create New Agent

**Trigger**: "Create agent for {{purpose}}", "Add an agent that {{does_what}}"

**Steps**:

1. **Check Existing Agents**
   ```
   list_dir(".agent/agents")
   → See what already exists
   ```

2. **Read Agent Template**
   ```
   read_file("templates/factory/agent.md.tmpl")
   → Get markdown structure
   ```

3. **Read Example Agent** (for reference)
   ```
   read_file(".agent/agents/knowledge-extender.md")
   → See good agent structure
   ```

4. **Generate Agent Content**
   - Define clear activation triggers
   - List capabilities
   - Document workflow
   - Reference skills used

5. **Write Agent**
   ```
   write(".agent/agents/{{agent-name}}.md", content)
   ```

**Output**: `.agent/agents/{agent-name}.md`

---

### Procedure E: Extend Existing Knowledge (Shallow Gap)

**Trigger**: "Improve knowledge about {{topic}}", "Add more to {{topic}}"

**Steps**:

1. **Read Existing File**
   ```
   read_file("knowledge/{{topic}}-patterns.json")
   → Understand current content
   ```

2. **Identify Gaps**
   - Missing patterns?
   - Lacking code examples?
   - No best practices?

3. **Research Missing Content**
   ```
   web_search("{{topic}} advanced patterns")
   ```

4. **Update File**
   ```
   search_replace or write with merged content
   ```

**Output**: Updated `knowledge/{topic}-patterns.json`

---

## Chat Examples

### Example 1: Web Search Extension
```
User: Extend knowledge for OpenAI Agents SDK

Agent: I'll research OpenAI Agents SDK and create a knowledge file.

[list_dir("knowledge")] → No existing file
[read_file("templates/knowledge/knowledge-file.tmpl")]
[web_search("OpenAI Agents SDK patterns 2026")]
[web_search("OpenAI Agents SDK implementation examples")]
[Synthesizes findings]
[write("knowledge/openai-agents-sdk-patterns.json", ...)]

Created: knowledge/openai-agents-sdk-patterns.json
- 5 patterns added
- Code examples included
- Sources: OpenAI documentation, community best practices

Would you like me to add this to a blueprint?
```

### Example 2: User-Provided Link
```
User: Add knowledge from this article: https://langchain.dev/docs/agents

Agent: I'll incorporate knowledge from the LangChain agents documentation.

[web_search("site:langchain.dev agents patterns implementation")]
[Synthesizes findings]
[read_file("knowledge/langchain-patterns.json")] → Exists, will extend
[Updates existing file with new patterns]

Updated: knowledge/langchain-patterns.json
- Added 3 new patterns from langchain.dev
- Added agent types section
- Cited source: https://langchain.dev/docs/agents
```

### Example 3: Create New Skill
```
User: Create a skill for prompt testing

Agent: I'll create a skill for systematic prompt testing.

[list_dir(".agent/skills")] → No prompt-testing skill
[read_file("templates/factory/skill.md.tmpl")]
[read_file(".agent/skills/extend-knowledge/SKILL.md")] → Reference
[Designs skill structure]
[write(".agent/skills/prompt-testing/SKILL.md", ...)]

Created: .agent/skills/prompt-testing/SKILL.md

Skill includes:
- When to use: Testing prompts before deployment
- Process: Define test cases → Run variations → Analyze results
- Tools: Test matrix template, evaluation criteria

Would you like to add this skill to an agent?
```

### Example 4: Document Incorporation
```
User: Add knowledge from docs/research/CONSTITUTIONAL_AI.md

Agent: I'll incorporate the constitutional AI research document.

[read_file("docs/research/CONSTITUTIONAL_AI.md")]
[Extracts key patterns and concepts]
[read_file("templates/knowledge/knowledge-file.tmpl")]
[Structures into knowledge format]
[write("knowledge/constitutional-ai-patterns.json", ...)]

Created: knowledge/constitutional-ai-patterns.json
- Sourced from: docs/research/CONSTITUTIONAL_AI.md
- 4 patterns extracted
- Best practices included
```

## Summary: What Gets Created

| Extension Type | Output Location | Format |
|----------------|-----------------|--------|
| Knowledge | `knowledge/{topic}-patterns.json` | JSON |
| Skill | `.agent/skills/{name}/SKILL.md` | Markdown |
| Agent | `.agent/agents/{name}.md` | Markdown |
| Template | `templates/{category}/{name}.tmpl` | Template |

## Post-Extension Automation (MANDATORY)

> **Excellence Standard**: Every extension MUST complete ALL post-extension steps. This is not optional.

### Step 0: Determine What to Update

**Read the dependency map:**
```
read_file("knowledge/artifact-dependencies.json")
```

**Detection by artifact type:**

| If I Created/Modified | Must Update |
|-----------------------|-------------|
| `knowledge/*.json` (new) | manifest.json (add entry + stats), KNOWLEDGE_FILES.md (table + count + details), CHANGELOG.md |
| `knowledge/*.json` (extend) | manifest.json (bump version + change_history), KNOWLEDGE_FILES.md (if description changed), CHANGELOG.md |
| `.agent/skills/*/SKILL.md` (any) | skill-catalog.json, CHANGELOG.md |
| `.agent/skills/*/SKILL.md` (Factory skill) | skill-catalog.json, **FACTORY_COMPONENTS.md** (table + details + diagram), CHANGELOG.md |
| `.agent/agents/*.md` (any) | CHANGELOG.md |
| `.agent/agents/*.md` (Factory agent) | **FACTORY_COMPONENTS.md** (table + details + diagram + integration points), CHANGELOG.md |
| `templates/*.tmpl` | CHANGELOG.md, (TEMPLATES.md if major) |
| `blueprints/*/blueprint.json` | BLUEPRINTS.md (table + details), CHANGELOG.md |

**Is it a Factory component?** Check `knowledge/artifact-dependencies.json` → `factory_artifact_detection`:
- Factory agents: requirements-architect, stack-builder, knowledge-extender, etc.
- Factory skills: extend-knowledge, requirements-gathering, update-knowledge, etc.
- If in list → MUST update `docs/reference/FACTORY_COMPONENTS.md`

**Find additional references:**
```
grep("{{artifact_name}}", "knowledge", output_mode="files_with_matches")
grep("{{artifact_name}}", "docs", output_mode="files_with_matches")
grep("{{artifact_name}}", "blueprints", output_mode="files_with_matches")
grep("{{artifact_name}}", ".agent", output_mode="files_with_matches")
```

After creating or extending ANY artifact, ALWAYS execute these steps in order:

### Step 1: Update Manifest (Knowledge Files Only)

```
read_file("knowledge/manifest.json")
→ Find entry for the file (or add new entry)
→ Bump version (1.0.0 → 1.1.0 for additions, 1.0.0 → 1.0.1 for fixes)
→ Update timestamp
→ Add change_history entry

search_replace("knowledge/manifest.json", ...)
```

**Required Fields**:
```json
{
  "version": "1.1.0",  // BUMP THIS
  "metadata": {
    "updated": "{{CURRENT_DATETIME}}"  // UPDATE THIS
  },
  "change_history": [  // ADD THIS
    {
      "version": "1.1.0",
      "date": "{{CURRENT_DATE}}",
      "changes": ["Added X", "Added Y"]
    }
  ]
}
```

### Step 2: Update Skill Catalog (New Skills Only)

```
read_file("knowledge/skill-catalog.json")
→ Add entry in "skills" section
→ Add to category list at bottom

search_replace("knowledge/skill-catalog.json", ...)
```

**Required Entry**:
```json
"{{skill-id}}": {
  "id": "{{skill-id}}",
  "name": "{{Skill Name}}",
  "category": "{{category}}",
  "stackAgnostic": true,
  "description": "{{description}}",
  "factorySkill": ".agent/skills/{{skill-id}}/SKILL.md",
  "whenToUse": ["{{condition1}}", "{{condition2}}"]
}
```

### Step 3: Update Documentation

```
read_file("docs/reference/KNOWLEDGE_FILES.md")
→ Update table entry for modified knowledge file
→ Update detailed description section

search_replace("docs/reference/KNOWLEDGE_FILES.md", ...)
```

**For Knowledge Files**: Update both the table row AND the detailed description.

### Step 4: Update Changelog

```
read_file("CHANGELOG.md")
→ Add new version entry at top (after header)

search_replace("CHANGELOG.md", ...)
```

**Required Format**:
```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added - {{Extension Title}}

{{Brief description}}

#### Changes

| File | Action | Description |
|------|--------|-------------|
| `path/to/file` | Extended/Created | What was done |

---
```

### Step 5: Validate JSON Files

```python
# Run after all edits:
python -c "import json; json.load(open('knowledge/{{file}}.json', encoding='utf-8')); print('Valid!')"
```

### Step 6: Git Operations (Ask User First)

**ALWAYS ask before git operations**:

```
⚠️ Ready to commit and push:

Modified: [list files]
New: [list files]

Proposed commit: feat(knowledge): {{description}}

Proceed? (yes/no/commit only)
```

---

## Validation Checklist

### Knowledge Files
- [ ] Valid JSON syntax
- [ ] Has `$schema`, `title`, `description`, `version`
- [ ] Has at least 3 patterns (per schema)
- [ ] Patterns have `name`, `description`, `category`, `when_to_use`
- [ ] Code examples included
- [ ] Sources cited
- [ ] **Manifest updated with new version**
- [ ] **Documentation updated**
- [ ] **Changelog entry added**

### Skills
- [ ] Valid YAML frontmatter
- [ ] Has `name`, `description`, `type: skill`
- [ ] Defines `When to Use`
- [ ] Has clear `Process` steps
- [ ] Includes `Fallback Procedures`
- [ ] **Registered in skill-catalog.json**
- [ ] **Changelog entry added**

### Agents
- [ ] Valid YAML frontmatter
- [ ] Has `name`, `description`, `type: agent`
- [ ] Defines `activation` triggers
- [ ] Lists `skills` used
- [ ] Has `Purpose` section
- [ ] **Changelog entry added**

## Error Handling

| Issue | Resolution |
|-------|------------|
| Web search fails | Use built-in LLM knowledge |
| File already exists | Ask: extend or replace? |
| Invalid JSON output | Validate and fix syntax |
| Topic not in taxonomy | Add to taxonomy first |
| Missing patterns | Research more sources |

## Related Artifacts

- **Agent**: `.agent/agents/knowledge-extender.md`
- **Templates**: `templates/factory/*.tmpl`, `templates/knowledge/*.tmpl`
- **Schema**: `patterns/knowledge/knowledge-schema.json`
- **Taxonomy**: `scripts/taxonomy/agent_taxonomy.json`
