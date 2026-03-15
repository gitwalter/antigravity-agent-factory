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
      <h1 style={{ fontSize: 24, fontWeight: 700, marginBottom: 8, letterSpacing: '-0.02em' }}>
        Dashboard
      </h1>
      <p style={{ color: 'var(--text-secondary)', marginBottom: 24, fontSize: 14 }}>
        Antigravity Agent Factory — Development Experience
      </p>

      {error && (
        <div className="card" style={{ borderColor: 'var(--warning)', marginBottom: 20 }}>
          <p style={{ color: 'var(--warning)', fontSize: 13 }}>⚠ {error}</p>
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
      <div style={{ marginBottom: 24 }}>
        <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>Quick Actions</h2>
        <div style={{ display: 'flex', gap: 12 }}>
          <a href="/workflows" className="btn btn-primary">⚙ Build Workflow</a>
          <a href="/agent-workflows" className="btn btn-primary">⚡ Generate Agent Workflow</a>
          <a href="/tools" className="btn btn-secondary">🔧 Browse Tools</a>
        </div>
      </div>

      {/* Recent Workflows */}
      <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>Recent Workflows</h2>
      <div className="card-grid">
        {workflows.slice(0, 6).map(wf => (
          <a href={`/workflows?edit=${wf.filename}`} key={wf.filename} style={{ textDecoration: 'none', color: 'inherit' }}>
            <div className="card">
              <div className="card-header">
                <span className="card-title" style={{ color: 'var(--text-primary)' }}>{wf.title || wf.filename}</span>
                <span className="tag" style={{ border: '1px solid var(--accent-primary)', color: 'var(--accent-primary)', fontWeight: 600 }}>{wf.phase_count} phases</span>
              </div>
              <p style={{ fontSize: 12, color: 'var(--text-secondary)', marginBottom: 12 }}>
                {wf.description || 'No description'}
              </p>
              <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                {(wf.tags || []).slice(0, 4).map(tag => (
                  <span key={tag} className="tag" style={{ fontSize: 10, background: 'var(--bg-secondary)', border: '1px solid var(--border)' }}>{tag}</span>
                ))}
              </div>
            </div>
          </a>
        ))}
      </div>
    </div>
  )
}
