---
description: Extend Factory knowledge, skills, and templates via research, documents,
  or user links
name: extending-knowledge
type: skill
---
# Extend Knowledge

Extend Factory knowledge, skills, and templates via research, documents, or user links

Extend the Factory's knowledge base, skills, and templates through multiple research methods:
- **Web Search**: Use `web_search` tool to find current information
- **Document Reading**: Read files, PDFs, or code repositories
- **User Links**: Process URLs provided by users in chat
- **Synthesis**: Combine sources into structured Factory artifacts

## Artifacts Used

| Artifact | Path | Purpose |
|----------|------|---------|
| Knowledge Template | `{directories.templates}/knowledge/knowledge-file.tmpl` | JSON structure for knowledge |
| Skill Template | `{directories.templates}/factory/skill.md.tmpl` | Markdown structure for skills |
| Agent Template | `{directories.templates}/factory/agent.md.tmpl` | Markdown structure for agents |
| Schema | `{directories.patterns}/knowledge/knowledge-schema.json` | Validation rules |
| Taxonomy | `{directories.scripts}/taxonomy/agent_taxonomy.json` | Topic definitions |

## Research Methods

### Method 1: Advanced Research Research
Use when: Topic needs current, online information or deep domain expertise.

**Tools**: `tavily_search`, `fetch_url`, `deepwiki_ask_question`

```
Step 1: tavily_search("{{topic}} best practices patterns 2026")
Step 2: fetch_url("{{documentation_url}}") -> extract markdown
Step 3: deepwiki_ask_question(repoName="{{repo}}", question="{{specific_question}}")
```

**What I Do**:
1. Execute multi-layered searches using Tavily for high-fidelity results.
2. Scrape official documentation directly using Fetch/Playwright.
3. Query the DeepWiki knowledge base for repository-specific insights.
4. Extract patterns, examples, and pitfalls with citations.

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
[Creates {directories.knowledge}/constitutional-ai-patterns.json]
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
   list_dir("{directories.knowledge}")
   → See what already exists
   ```

2. **Read Taxonomy**
   ```
   read_file("{directories.scripts}/taxonomy/agent_taxonomy.json")
   → Understand topic requirements (depth, keywords)
   ```

3. **Read Template**
   ```
   read_file("{directories.templates}/knowledge/knowledge-file.tmpl")
   → Get JSON structure to follow
   ```

4. **Read Schema**
   ```
   read_file("{directories.patterns}/knowledge/knowledge-schema.json")
   → Get validation rules (min 3 patterns)
   ```

5. **Research Topic** (one or more methods)
   ```
   tavily_search("{{topic}} best practices 2026")
   fetch_url("{{official_docs}}")
   deepwiki_ask_question(repoName="owner/repo", question="How does X work?")
   read_file("{{user_provided_doc}}") if provided
   ```

6. **Generate Content**
   - Synthesize research into JSON structure
   - Include at least 3 patterns
   - Add code examples
   - Cite sources

7. **Write File**
   ```
   write("{directories.knowledge}/{{topic-name}}-patterns.json", content)
   ```

8. **Validate**
   ```
   read_file("{directories.knowledge}/{{topic-name}}-patterns.json")
   → Verify JSON is valid
   ```

**Output**: `{directories.knowledge}/{topic}-patterns.json` (50-200 lines)

---

### Procedure B: Create New Skill

**Trigger**: "Create skill for {{purpose}}", "Add a skill that {{does_what}}"

**Steps**:

1. **Check Existing Skills**
   ```
   list_dir("{directories.skills}")
   → See what already exists, avoid duplicates
   ```

2. **Read Skill Template**
   ```
   read_file("{directories.templates}/factory/skill.md.tmpl")
   → Get markdown structure
   ```

3. **Read Example Skill** (for reference)
   ```
   read_file("{directories.skills}/extend-knowledge/SKILL.md")
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
   write("{directories.skills}/{{skill-name}}/SKILL.md", content)
   ```

**Output**: `{directories.skills}/{skill-name}/SKILL.md`

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

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
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
   list_dir("{directories.templates}")
   → Find appropriate category folder
   ```

2. **Read Similar Template** (for style)
   ```
   read_file("{directories.templates}/{{category}}/{{similar}}.tmpl")
   → Understand existing conventions
   ```

3. **Design Template**
   - Identify placeholders needed (`{{VARIABLE_NAME}}`)
   - Structure for target file type
   - Include helpful comments

4. **Write Template**
   ```
   write("{directories.templates}/{{category}}/{{name}}.tmpl", content)
   ```

**Output**: `{directories.templates}/{category}/{name}.tmpl`

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
   list_dir("{directories.agents}")
   → See what already exists
   ```

2. **Read Agent Template**
   ```
   read_file("{directories.templates}/factory/agent.md.tmpl")
   → Get markdown structure
   ```

3. **Read Example Agent** (for reference)
   ```
   read_file("{directories.agents}/knowledge-extender.md")
   → See good agent structure
   ```

4. **Generate Agent Content**
   - Define clear activation triggers
   - List capabilities
   - Document workflow
   - Reference skills used

5. **Write Agent**
   ```
   write("{directories.agents}/{{agent-name}}.md", content)
   ```

**Output**: `{directories.agents}/{agent-name}.md`

---

### Procedure E: Extend Existing Knowledge (Shallow Gap)

**Trigger**: "Improve knowledge about {{topic}}", "Add more to {{topic}}"

**Steps**:

1. **Read Existing File**
   ```
   read_file("{directories.knowledge}/{{topic}}-patterns.json")
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

**Output**: Updated `{directories.knowledge}/{topic}-patterns.json`

---

## Chat Examples

### Example 1: Web Search Extension
```
User: Extend knowledge for OpenAI Agents SDK

Agent: I'll research OpenAI Agents SDK and create a knowledge file.

[list_dir("{directories.knowledge}")] → No existing file
[read_file("{directories.templates}/knowledge/knowledge-file.tmpl")]
[web_search("OpenAI Agents SDK patterns 2026")]
[web_search("OpenAI Agents SDK implementation examples")]
[Synthesizes findings]
[write("{directories.knowledge}/openai-agents-sdk-patterns.json", ...)]

Created: {directories.knowledge}/openai-agents-sdk-patterns.json
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
[read_file("{directories.knowledge}/langchain-patterns.json")] → Exists, will extend
[Updates existing file with new patterns]

Updated: {directories.knowledge}/langchain-patterns.json
- Added 3 new patterns from langchain.dev
- Added agent types section
- Cited source: https://langchain.dev/docs/agents
```

### Example 3: Create New Skill
```
User: Create a skill for prompt testing

Agent: I'll create a skill for systematic prompt testing.

[list_dir("{directories.skills}")] → No prompt-testing skill
[read_file("{directories.templates}/factory/skill.md.tmpl")]
[read_file("{directories.skills}/extend-knowledge/SKILL.md")] → Reference
[Designs skill structure]
[write("{directories.skills}/prompt-testing/SKILL.md", ...)]

Created: {directories.skills}/prompt-testing/SKILL.md

Skill includes:
- When to use: Testing prompts before deployment
- Process: Define test cases → Run variations → Analyze results
- Tools: Test matrix template, evaluation criteria

Would you like to add this skill to an agent?
```

### Example 4: Document Incorporation
```
User: Add knowledge from {directories.docs}/research/CONSTITUTIONAL_AI.md

Agent: I'll incorporate the constitutional AI research document.

[read_file("{directories.docs}/research/CONSTITUTIONAL_AI.md")]
[Extracts key patterns and concepts]
[read_file("{directories.templates}/knowledge/knowledge-file.tmpl")]
[Structures into knowledge format]
[write("{directories.knowledge}/constitutional-ai-patterns.json", ...)]

Created: {directories.knowledge}/constitutional-ai-patterns.json
- Sourced from: {directories.docs}/research/CONSTITUTIONAL_AI.md
- 4 patterns extracted
- Best practices included
```

## Summary: What Gets Created

| Extension Type | Output Location | Format |
|----------------|-----------------|--------|
| Knowledge | `{directories.knowledge}/{topic}-patterns.json` | JSON |
| Skill | `{directories.skills}/{name}/SKILL.md` | Markdown |
| Agent | `{directories.agents}/{name}.md` | Markdown |
| Template | `{directories.templates}/{category}/{name}.tmpl` | Template |

## Post-Extension Automation (MANDATORY)

> **Excellence Standard**: Every extension MUST complete ALL post-extension steps. This is not optional.

### Step 0: Determine What to Update

**Read the dependency map:**
```
read_file("{directories.knowledge}/artifact-dependencies.json")
```

**Detection by artifact type:**

| If I Created/Modified | Must Update |
|-----------------------|-------------|
| `{directories.knowledge}/*.json` (new) | manifest.json (add entry + stats), KNOWLEDGE_FILES.md (table + count + details), CHANGELOG.md |
| `{directories.knowledge}/*.json` (extend) | manifest.json (bump version + change_history), KNOWLEDGE_FILES.md (if description changed), CHANGELOG.md |
| `{directories.skills}/*/SKILL.md` (any) | skill-catalog.json, CHANGELOG.md |
| `{directories.skills}/*/SKILL.md` (Factory skill) | skill-catalog.json, **FACTORY_COMPONENTS.md** (table + details + diagram), CHANGELOG.md |
| `{directories.agents}/*.md` (any) | CHANGELOG.md |
| `{directories.agents}/*.md` (Factory agent) | **FACTORY_COMPONENTS.md** (table + details + diagram + integration points), CHANGELOG.md |
| `{directories.templates}/*.tmpl` | CHANGELOG.md, (TEMPLATES.md if major) |
| `{directories.blueprints}/*/blueprint.json` | BLUEPRINTS.md (table + details), CHANGELOG.md |

**Is it a Factory component?** Check `{directories.knowledge}/artifact-dependencies.json` → `factory_artifact_detection`:
- Factory agents: requirements-architect, stack-builder, knowledge-extender, etc.
- Factory skills: extend-knowledge, requirements-gathering, update-knowledge, etc.
- If in list → MUST update `{directories.docs}/reference/FACTORY_COMPONENTS.md`

**Find additional references:**
```
grep("{{artifact_name}}", "knowledge", output_mode="files_with_matches")
grep("{{artifact_name}}", "docs", output_mode="files_with_matches")
grep("{{artifact_name}}", "blueprints", output_mode="files_with_matches")
grep("{{artifact_name}}", ".cursor", output_mode="files_with_matches")
```

After creating or extending ANY artifact, ALWAYS execute these steps in order:

### Step 1: Update Manifest (Knowledge Files Only)

```
read_file("{directories.knowledge}/manifest.json")
→ Find entry for the file (or add new entry)
→ Bump version (1.0.0 → 1.1.0 for additions, 1.0.0 → 1.0.1 for fixes)
→ Update timestamp
→ Add change_history entry

search_replace("{directories.knowledge}/manifest.json", ...)
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
read_file("{directories.knowledge}/skill-catalog.json")
→ Add entry in "skills" section
→ Add to category list at bottom

search_replace("{directories.knowledge}/skill-catalog.json", ...)
```

**Required Entry**:
```json
"{{skill-id}}": {
  "id": "{{skill-id}}",
  "name": "{{Skill Name}}",
  "category": "{{category}}",
  "stackAgnostic": true,
  "description": "{{description}}",
  "factorySkill": "{directories.skills}/{{skill-id}}/SKILL.md",
  "whenToUse": ["{{condition1}}", "{{condition2}}"]
}
```

### Step 3: Update Documentation

```
read_file("{directories.docs}/reference/KNOWLEDGE_FILES.md")
→ Update table entry for modified knowledge file
→ Update detailed description section

search_replace("{directories.docs}/reference/KNOWLEDGE_FILES.md", ...)
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
python -c "import json; json.load(open('{directories.knowledge}/{{file}}.json', encoding='utf-8')); print('Valid!')"
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

## Important Rules

1. **Use `{directories.XXX}` path variables** — NEVER hardcode directory paths like `.cursor/skills/`, `knowledge/`, or `templates/` in any generated artifact content. Always use configured path variables from `{directories.config}/settings.json` (e.g. `{directories.skills}`, `{directories.knowledge}`, `{directories.templates}`, `{directories.agents}`). This applies to ALL artifacts: knowledge files, skills, agents, templates, and workflows.

## Best Practices

- **Verify sources before synthesis**: Always check that web search results are from reputable sources (official docs, established frameworks, recognized experts) before incorporating into knowledge files
- **Maintain citation integrity**: Include source URLs, dates, and attribution in knowledge files so future users can verify and update information
- **Validate against schema early**: Check knowledge files against `knowledge-schema.json` during creation, not after, to catch structural issues immediately
- **Use multiple research methods**: Combine web search, document reading, and repository analysis for comprehensive coverage rather than relying on a single source
- **Check for existing knowledge first**: Always search existing knowledge files before creating new ones to avoid duplication and ensure consistency
- **Update related artifacts together**: When extending knowledge, update manifest.json, KNOWLEDGE_FILES.md, and CHANGELOG.md in the same session to maintain documentation coherence

## Error Handling

| Issue | Resolution |
|-------|------------|
| Web search fails | Use built-in LLM knowledge |
| File already exists | Ask: extend or replace? |
| Invalid JSON output | Validate and fix syntax |
| Topic not in taxonomy | Add to taxonomy first |
| Missing patterns | Research more sources |

## Related Artifacts

- **Agent**: `{directories.agents}/knowledge-extender.md`
- **Templates**: `{directories.templates}/factory/*.tmpl`, `{directories.templates}/knowledge/*.tmpl`
- **Schema**: `{directories.patterns}/knowledge/knowledge-schema.json`
- **Taxonomy**: `{directories.scripts}/taxonomy/agent_taxonomy.json`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
