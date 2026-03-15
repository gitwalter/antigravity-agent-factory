/** API client for the Antigravity IDX backend. */
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  })
  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`)
  }
  return res.json()
}

export interface Workflow {
  filename: string
  title: string
  description: string
  tags: string[]
  version: string
  phase_count: number
  phases: Phase[]
  sources?: string[]
}

export interface Phase {
  name: string
  goal: string
  actions: string[]
  agent: string
  skills: string[]
  tools: string[]
}

export interface Agent {
  name: string
  pattern: string
  description: string
  path: string
}

export interface Skill {
  name: string
  pattern: string
  description: string
  tools: string[]
  path: string
}

export interface Script {
  name: string
  path: string
  docstring: string
  category: string
}

export interface McpServer {
  id: string
  name: string
  status: string
  type?: string
  command?: string
  args?: string[]
}

export interface Rule {
  name: string
  path: string
  description: string
  title: string
}

export interface Blueprint {
  name: string
  path: string
  description: string
  title: string
}

export interface KnowledgeFile {
  name: string
  path: string
  description: string
  title: string
}

export interface Pattern {
  name: string
  path: string
  description: string
  title: string
}

// API functions
export const api = {
  health: () => apiFetch<{ status: string; version: string }>('/api/health'),
  workflows: () => apiFetch<Workflow[]>('/api/workflows'),
  workflow: (name: string) => apiFetch<Workflow & { raw_body: string; source: string }>(`/api/workflows/${name}`),
  saveWorkflow: (name: string, data: Partial<Workflow>) =>
    apiFetch<{ status: string }>(`/api/workflows/${name}`, { method: 'PUT', body: JSON.stringify(data) }),
  createWorkflow: (name: string, data: Partial<Workflow>) =>
    apiFetch<{ status: string }>(`/api/workflows/${name}`, { method: 'POST', body: JSON.stringify(data) }),
  agents: () => apiFetch<Agent[]>('/api/agents'),
  agent: (name: string) => apiFetch<Agent & { content: string }>(`/api/agents/${name}`),
  saveAgent: (name: string, path: string, content: string) =>
    apiFetch<{ status: string }>(`/api/agents/${name}`, { method: 'PUT', body: JSON.stringify({ path, content }) }),

  skills: () => apiFetch<Skill[]>('/api/skills'),
  skill: (name: string) => apiFetch<Skill & { content: string }>(`/api/skills/${name}`),
  saveSkill: (name: string, path: string, content: string) =>
    apiFetch<{ status: string }>(`/api/skills/${name}`, { method: 'PUT', body: JSON.stringify({ path, content }) }),

  scripts: () => apiFetch<Script[]>('/api/scripts'),
  script: (path: string) => apiFetch<Script & { content: string }>(`/api/scripts/${encodeURIComponent(path)}`),
  saveScript: (path: string, content: string) =>
    apiFetch<{ status: string }>(`/api/scripts/${encodeURIComponent(path)}`, { method: 'PUT', body: JSON.stringify({ path, content }) }),

  mcpServers: () => apiFetch<McpServer[]>('/api/mcp/servers'),
  mcpServer: (name: string) => apiFetch<McpServer & { env?: Record<string, string> }>(`/api/mcp/servers/${name}`),
  createMcpServer: (data: Partial<McpServer>) =>
    apiFetch<{ status: string }>(`/api/mcp/servers`, { method: 'POST', body: JSON.stringify(data) }),
  deleteMcpServer: (name: string) =>
    apiFetch<{ status: string }>(`/api/mcp/servers/${name}`, { method: 'DELETE' }),
  testMcpServer: (name: string) =>
    apiFetch<{ status: string; returncode?: number; stdout?: string; stderr?: string; error?: string }>(
      `/api/mcp/servers/${name}/test`,
      { method: 'POST' }
    ),
  generateAgentWorkflow: (data: {
    name: string
    description: string
    framework: string
    steps: { name: string; description: string }[]
    tools: string[]
  }) => apiFetch<{ status: string; path: string; framework: string; code_preview: string }>(
    '/api/agent-workflows/generate',
    { method: 'POST', body: JSON.stringify(data) }
  ),
  chat: (messages: { role: string; content: string }[]) =>
    apiFetch<{ content: string }>('/api/chat', { method: 'POST', body: JSON.stringify({ messages }) }),

  rules: () => apiFetch<Rule[]>('/api/rules'),
  blueprints: () => apiFetch<Blueprint[]>('/api/blueprints'),
  knowledgeFiles: () => apiFetch<KnowledgeFile[]>('/api/knowledge-files'),
  patterns: () => apiFetch<Pattern[]>('/api/patterns'),

  artifact: (path: string) => apiFetch<{ name: string; path: string; content: string }>(`/api/artifacts/${encodeURIComponent(path)}`),
  saveArtifact: (path: string, content: string) =>
    apiFetch<{ status: string }>(`/api/artifacts`, { method: 'PUT', body: JSON.stringify({ path, content }) }),

  agentConfig: () => apiFetch<any>('/api/agent-config'),
  saveAgentConfig: (data: any) =>
    apiFetch<{ status: string }>('/api/agent-config', { method: 'PUT', body: JSON.stringify(data) }),
}
