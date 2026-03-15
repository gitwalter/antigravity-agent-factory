'use client'
import { useState } from 'react'
import { api, Skill } from '@/lib/api'
import { useEffect } from 'react'

export default function AgentWorkflowsPage() {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [framework, setFramework] = useState<'langgraph' | 'crewai'>('langgraph')
  const [steps, setSteps] = useState<{ name: string; description: string }[]>([
    { name: 'Step 1', description: '' }
  ])
  const [tools, setTools] = useState('')
  const [generating, setGenerating] = useState(false)
  const [result, setResult] = useState<{ path: string; code_preview: string } | null>(null)
  const [error, setError] = useState('')
  const [skills, setSkills] = useState<Skill[]>([])

  useEffect(() => {
    api.skills().catch(() => []).then(setSkills)
  }, [])

  function addStep() {
    setSteps([...steps, { name: `Step ${steps.length + 1}`, description: '' }])
  }

  function removeStep(idx: number) {
    if (steps.length <= 1) return
    setSteps(steps.filter((_, i) => i !== idx))
  }

  function updateStep(idx: number, field: 'name' | 'description', value: string) {
    setSteps(steps.map((s, i) => i === idx ? { ...s, [field]: value } : s))
  }

  async function generate() {
    if (!name.trim()) {
      setError('Name is required')
      return
    }
    setGenerating(true)
    setError('')
    setResult(null)
    try {
      const res = await api.generateAgentWorkflow({
        name,
        description,
        framework,
        steps,
        tools: tools.split(',').map(t => t.trim()).filter(Boolean),
      })
      setResult(res)
    } catch (e) {
      setError((e as Error).message)
    }
    setGenerating(false)
  }

  return (
    <div style={{ maxWidth: 800, margin: '0 auto' }}>
      <h1 style={{ fontSize: 24, fontWeight: 700, marginBottom: 8 }}>Agent Workflow Generator</h1>
      <p style={{ color: 'var(--text-secondary)', fontSize: 14, marginBottom: 24 }}>
        Generate executable LangGraph or CrewAI workflows powered by Gemini via aisuite.
        All agent runs are automatically traced in LangSmith.
      </p>

      {/* Framework Selection */}
      <div className="tabs">
        <button className={`tab ${framework === 'langgraph' ? 'active' : ''}`} onClick={() => setFramework('langgraph')}>
          🔗 LangGraph
        </button>
        <button className={`tab ${framework === 'crewai' ? 'active' : ''}`} onClick={() => setFramework('crewai')}>
          👥 CrewAI
        </button>
      </div>

      <div className="card" style={{ marginBottom: 16 }}>
        <div style={{ display: 'grid', gap: 12 }}>
          <div>
            <label style={{ fontSize: 11, color: 'var(--text-muted)', display: 'block', marginBottom: 4 }}>Workflow Name</label>
            <input type="text" value={name} onChange={e => setName(e.target.value)} placeholder="e.g. research-and-analyze" />
          </div>
          <div>
            <label style={{ fontSize: 11, color: 'var(--text-muted)', display: 'block', marginBottom: 4 }}>Description</label>
            <textarea
              value={description}
              onChange={e => setDescription(e.target.value)}
              placeholder="Describe what this workflow should do..."
              rows={3}
            />
          </div>
          <div>
            <label style={{ fontSize: 11, color: 'var(--text-muted)', display: 'block', marginBottom: 4 }}>
              Tools / MCP Servers (comma-separated)
            </label>
            <input
              type="text"
              value={tools}
              onChange={e => setTools(e.target.value)}
              placeholder="e.g. tavily_search, memory, fetch"
            />
          </div>
        </div>
      </div>

      {/* Steps */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
        <h3 style={{ fontSize: 14, fontWeight: 600 }}>Workflow Steps</h3>
        <button className="btn btn-secondary btn-sm" onClick={addStep}>+ Add Step</button>
      </div>

      <div className="workflow-canvas" style={{ marginBottom: 16 }}>
        {steps.map((step, idx) => (
          <div key={idx}>
            <div className="phase-node">
              <div className="phase-node-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, flex: 1 }}>
                  <span className="phase-number">{idx + 1}</span>
                  <input
                    type="text"
                    value={step.name}
                    onChange={e => updateStep(idx, 'name', e.target.value)}
                    style={{ background: 'transparent', border: 'none', color: 'var(--text-primary)', fontWeight: 500, fontSize: 14, padding: 0, flex: 1 }}
                  />
                </div>
                <button className="btn-icon" onClick={() => removeStep(idx)} style={{ color: 'var(--error)' }}>✕</button>
              </div>
              <div style={{ marginTop: 8 }}>
                <input
                  type="text"
                  value={step.description}
                  onChange={e => updateStep(idx, 'description', e.target.value)}
                  placeholder={framework === 'langgraph' ? 'Node logic description...' : 'Agent task description...'}
                />
              </div>
            </div>
            {idx < steps.length - 1 && <div className="phase-connector" />}
          </div>
        ))}
      </div>

      {/* Generate */}
      <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
        <button className="btn btn-primary" onClick={generate} disabled={generating}>
          {generating ? (
            <><div className="loading-spinner" style={{ width: 14, height: 14 }} /> Generating...</>
          ) : (
            `⚡ Generate ${framework === 'langgraph' ? 'LangGraph' : 'CrewAI'} Workflow`
          )}
        </button>
        {error && <span style={{ fontSize: 12, color: 'var(--error)' }}>{error}</span>}
      </div>

      {/* Result */}
      {result && (
        <div className="card" style={{ marginTop: 20 }}>
          <div className="card-header">
            <span className="card-title">Generated: {result.path}</span>
            <span className="tag tag-success">✓ Saved</span>
          </div>
          <p style={{ fontSize: 12, color: 'var(--text-secondary)', marginBottom: 8 }}>
            Output saved to <code style={{ color: 'var(--accent-primary)' }}>{result.path}</code>.
            LangSmith tracing is enabled — all runs will appear in the{' '}
            <a href="https://smith.langchain.com" target="_blank" rel="noopener" style={{ color: 'var(--accent-secondary)' }}>
              LangSmith dashboard
            </a>.
          </p>
          <div className="code-block">{result.code_preview}</div>
        </div>
      )}

      {/* Available Skills Reference */}
      {skills.length > 0 && (
        <div style={{ marginTop: 24 }}>
          <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 8 }}>Available Skills for Reference</h3>
          <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
            {skills.slice(0, 30).map(s => (
              <span key={s.path} className="tag" title={s.description}>{s.name}</span>
            ))}
            {skills.length > 30 && <span className="tag">+{skills.length - 30} more</span>}
          </div>
        </div>
      )}
    </div>
  )
}
