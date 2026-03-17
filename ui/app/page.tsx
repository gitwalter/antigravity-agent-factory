'use client'
import { useEffect, useState } from 'react'
import { api, Workflow, Agent, Script } from '@/lib/api'

export default function Dashboard() {
  const [workflows, setWorkflows] = useState<Workflow[]>([])
  const [agents, setAgents] = useState<Agent[]>([])
  const [scripts, setScripts] = useState<Script[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([
      api.workflows().catch(() => []),
      api.agents().catch(() => []),
      api.scripts().catch(() => []),
    ]).then(([wf, ag, sc]) => {
      setWorkflows(wf)
      setAgents(ag)
      setScripts(sc)
      setLoading(false)
    }).catch(() => {
      setError('Cannot connect to backend. Start the API with: python scripts/api/mcp_api.py')
      setLoading(false)
    })
  }, [])

  if (loading) return <div style={{ textAlign: 'center', padding: 60 }}><div className="loading-spinner" /></div>

  return (
    <div>
      <div className="dashboard-header" style={{ marginBottom: 32 }}>
        <h1 className="glow-text" style={{ fontSize: 32, fontWeight: 800, marginBottom: 8, letterSpacing: '-0.04em' }}>
          Dashboard
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: 16, opacity: 0.8 }}>
          Antigravity Agent Factory — Premium Development Experience
        </p>
      </div>

      {error && (
        <div className="card" style={{ borderColor: 'var(--warning)', marginBottom: 24, background: 'rgba(255, 184, 108, 0.05)' }}>
          <p style={{ color: 'var(--warning)', fontSize: 13, display: 'flex', alignItems: 'center', gap: 8 }}>
            <span>⚠</span> {error}
          </p>
        </div>
      )}

      {/* Stats */}
      <div className="stats-row">
        <div className="stat-card">
          <div className="stat-value">{workflows.length}</div>
          <div className="stat-label">Workflows</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{agents.length}</div>
          <div className="stat-label">Agents</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{scripts.length}</div>
          <div className="stat-label">Scripts</div>
        </div>
      </div>

      {/* Quick Actions */}
      <div style={{ marginBottom: 40 }}>
        <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 16, letterSpacing: '-0.02em' }}>Quick Actions</h2>
        <div style={{ display: 'flex', gap: 16 }}>
          <a href="/workflows" className="btn btn-primary glow-primary">⚙ Build Workflow</a>
          <a href="/agent-workflows" className="btn btn-primary">⚡ Generate Agent Workflow</a>
          <a href="/tools" className="btn btn-secondary">🔧 Browse Tools</a>
        </div>
      </div>

      {/* Recent Workflows */}
      <div style={{ marginBottom: 24, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <h2 style={{ fontSize: 18, fontWeight: 700, letterSpacing: '-0.02em' }}>Recent Workflows</h2>
        <a href="/workflows" style={{ fontSize: 13, color: 'var(--accent-primary)', textDecoration: 'none' }}>View all →</a>
      </div>

      <div className="card-grid">
        {workflows.slice(0, 6).map(wf => (
          <a href={`/workflows?edit=${wf.filename}`} key={wf.filename} style={{ textDecoration: 'none', color: 'inherit' }}>
            <div className="card">
              <div className="card-header">
                <span className="card-title">{wf.title || wf.filename}</span>
                <span className="tag tag-success">{wf.phase_count} phases</span>
              </div>
              <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginBottom: 16, display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                {wf.description || 'No description provided for this factory workflow.'}
              </p>
              <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                {(wf.tags || []).slice(0, 3).map(tag => (
                  <span key={tag} className="tag">{tag}</span>
                ))}
              </div>
            </div>
          </a>
        ))}
      </div>
    </div>
  )
}
