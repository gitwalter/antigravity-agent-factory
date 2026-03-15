'use client'
import { useEffect, useState } from 'react'
import { api, Agent } from '@/lib/api'

export default function AgentsPage() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [selected, setSelected] = useState<(Agent & { content: string }) | null>(null)
  const [loading, setLoading] = useState(true)
  const [loadingDetail, setLoadingDetail] = useState(false)
  const [saving, setSaving] = useState(false)
  const [msg, setMsg] = useState('')
  const [search, setSearch] = useState('')

  useEffect(() => {
    api.agents().then(data => {
      setAgents(data)
      setLoading(false)
    })
  }, [])

  async function selectAgent(name: string) {
    setLoadingDetail(true)
    setMsg('')
    try {
      const detail = await api.agent(name)
      setSelected(detail)
    } catch (e) {
      setMsg('✗ Failed to load: ' + (e as Error).message)
    }
    setLoadingDetail(false)
  }

  async function saveAgent() {
    if (!selected) return
    setSaving(true)
    try {
      await api.saveAgent(selected.name, selected.path, selected.content)
      setMsg('✓ Saved successfully')
      setTimeout(() => setMsg(''), 3000)
    } catch (e) {
      setMsg('✗ Save failed: ' + (e as Error).message)
    }
    setSaving(false)
  }

  const filtered = agents.filter(a =>
    a.name.toLowerCase().includes(search.toLowerCase()) ||
    a.description.toLowerCase().includes(search.toLowerCase()) ||
    a.pattern.toLowerCase().includes(search.toLowerCase())
  )

  if (loading) return <div style={{ textAlign: 'center', padding: 60 }}><div className="loading-spinner" /></div>

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: 20, height: 'calc(100vh - 104px)' }}>
      {/* Agent List */}
      <div style={{ overflowY: 'auto' }}>
        <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>Specialist Agents</h2>
        <input
          type="search"
          placeholder="Search agents..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          style={{ marginBottom: 12 }}
        />
        <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          {filtered.map(a => (
            <button
              key={a.path}
              onClick={() => selectAgent(a.name)}
              className={`phase-node ${selected?.name === a.name ? 'active' : ''}`}
              style={{ textAlign: 'left', cursor: 'pointer' }}
            >
              <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-primary)' }}>{a.name}</div>
              <div style={{ fontSize: 11, color: 'var(--text-secondary)', marginTop: 4 }}>{a.pattern}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Editor */}
      <div style={{ overflowY: 'auto' }}>
        {selected ? (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
              <div>
                <h2 style={{ fontSize: 18, fontWeight: 600 }}>{selected.name}</h2>
                <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>{selected.path}</div>
              </div>
              <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                {msg && <span style={{ fontSize: 12, color: msg.startsWith('✓') ? 'var(--success)' : 'var(--error)' }}>{msg}</span>}
                <button className="btn btn-primary" onClick={saveAgent} disabled={saving}>
                  {saving ? 'Saving...' : '💾 Save Definition'}
                </button>
              </div>
            </div>

            <div className="card" style={{ height: 'calc(100vh - 200px)', padding: 0 }}>
              <textarea
                value={selected.content}
                onChange={e => setSelected({ ...selected, content: e.target.value })}
                style={{
                  width: '100%',
                  height: '100%',
                  background: 'transparent',
                  color: '#e6edf3',
                  border: 'none',
                  fontFamily: 'monospace',
                  fontSize: 13,
                  padding: 20,
                  resize: 'none',
                  outline: 'none'
                }}
              />
            </div>
          </div>
        ) : (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-muted)' }}>
            <p>Select an agent to edit its markdown definition</p>
          </div>
        )}
      </div>
    </div>
  )
}
