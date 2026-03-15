'use client'
import { useEffect, useState } from 'react'
import { api } from '@/lib/api'

export default function AgentConfigPage() {
  const [config, setConfig] = useState<any>(null)
  const [editJson, setEditJson] = useState('')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [msg, setMsg] = useState('')

  useEffect(() => {
    api.agentConfig().then(data => {
      setConfig(data)
      setEditJson(JSON.stringify(data, null, 2))
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  async function saveConfig() {
    setSaving(true)
    setMsg('')
    try {
      const data = JSON.parse(editJson)
      await api.saveAgentConfig(data)
      setMsg('✓ Settings saved successfully')
      setConfig(data)
      setTimeout(() => setMsg(''), 3000)
    } catch (e) {
      setMsg('✗ Error: ' + (e as Error).message)
    }
    setSaving(false)
  }

  if (loading) return <div style={{ textAlign: 'center', padding: 60 }}><div className="loading-spinner" /></div>

  return (
    <div style={{ maxWidth: 800, margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h2 style={{ fontSize: 24, fontWeight: 700 }}>.agent Configuration</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: 14 }}>Manage factory settings and environment metadata</p>
        </div>
        <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
          {msg && <span style={{ fontSize: 12, color: msg.startsWith('✓') ? 'var(--success)' : 'var(--error)' }}>{msg}</span>}
          <button className="btn btn-primary" onClick={saveConfig} disabled={saving}>
            {saving ? 'Saving...' : '💾 Save Settings'}
          </button>
        </div>
      </div>

      <div className="card" style={{ marginBottom: 24 }}>
        <h3 style={{ fontSize: 16, fontWeight: 600, marginBottom: 16 }}>Settings (JSON)</h3>
        <div style={{ height: 500 }}>
          <textarea
            value={editJson}
            onChange={e => setEditJson(e.target.value)}
            style={{
              width: '100%',
              height: '100%',
              background: 'var(--bg-input)',
              color: '#a5d6ff',
              border: '1px solid var(--border)',
              borderRadius: 'var(--radius-sm)',
              fontFamily: 'monospace',
              fontSize: 13,
              padding: 16,
              resize: 'none',
              outline: 'none'
            }}
            placeholder="{ ... settings ... }"
          />
        </div>
      </div>

      <div className="card">
        <h3 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12 }}>Environment Info</h3>
        <div style={{ display: 'grid', gridTemplateColumns: '150px 1fr', gap: 8, fontSize: 13 }}>
          <div style={{ color: 'var(--text-muted)' }}>Factory Root:</div>
          <div style={{ fontFamily: 'monospace' }}>{config?.path || 'N/A'}</div>
          <div style={{ color: 'var(--text-muted)' }}>Status:</div>
          <div><span className="tag tag-success">{config?.status || 'Active'}</span></div>
        </div>
      </div>
    </div>
  )
}
