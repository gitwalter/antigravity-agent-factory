'use client'
import { useEffect, useState } from 'react'
import { api, McpServer } from '@/lib/api'

export default function McpPage() {
  const [servers, setServers] = useState<McpServer[]>([])
  const [loading, setLoading] = useState(true)
  const [testing, setTesting] = useState<string | null>(null)
  const [testResults, setTestResults] = useState<Record<string, any>>({})
  const [showNew, setShowNew] = useState(false)
  const [newServer, setNewServer] = useState({ name: '', command: '', args: '' })
  const [msg, setMsg] = useState('')

  useEffect(() => {
    refresh()
  }, [])

  function refresh() {
    api.mcpServers().then(s => { setServers(s); setLoading(false) })
  }

  async function testServer(name: string) {
    setTesting(name)
    try {
      const res = await api.testMcpServer(name)
      setTestResults(prev => ({ ...prev, [name]: res }))
    } catch (e) {
      setTestResults(prev => ({ ...prev, [name]: { status: 'error', error: (e as Error).message } }))
    }
    setTesting(null)
  }

  async function deleteServer(name: string) {
    if (!confirm(`Delete ${name}?`)) return
    try {
      await api.deleteMcpServer(name)
      refresh()
    } catch (e) {
      alert('Delete failed: ' + (e as Error).message)
    }
  }

  async function createServer() {
    try {
      await api.createMcpServer({
        name: newServer.name,
        command: newServer.command,
        args: newServer.args.split(' ').filter(Boolean),
      })
      setShowNew(false)
      setNewServer({ name: '', command: '', args: '' })
      refresh()
    } catch (e) {
      alert('Create failed: ' + (e as Error).message)
    }
  }

  if (loading) return <div style={{ textAlign: 'center', padding: 60 }}><div className="loading-spinner" /></div>

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 700 }}>MCP Servers</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: 14 }}>
            Manage Model Context Protocol servers for the Antigravity IDE
          </p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowNew(true)}>+ Add Server</button>
      </div>

      <div className="card-grid">
        {servers.map(server => (
          <div key={server.id} className="card" style={{ display: 'flex', flexDirection: 'column' }}>
            <div className="card-header">
              <span className="card-title">◎ {server.name}</span>
              <div style={{ display: 'flex', gap: 6 }}>
                <button
                  className="btn btn-secondary btn-sm"
                  onClick={() => testServer(server.name)}
                  disabled={testing === server.name}
                >
                  {testing === server.name ? 'Testing...' : 'Test'}
                </button>
                <button
                  className="btn btn-secondary btn-sm"
                  style={{ color: 'var(--error)' }}
                  onClick={() => deleteServer(server.name)}
                >
                  ✕
                </button>
              </div>
            </div>
            <div style={{ flex: 1 }}>
              {server.type && <p style={{ fontSize: 12, color: 'var(--text-secondary)' }}>Type: {server.type}</p>}
              <code style={{ fontSize: 11, color: 'var(--text-muted)', display: 'block', marginTop: 8, wordBreak: 'break-all' }}>
                {server.command} {server.args?.join(' ')}
              </code>
            </div>

            {testResults[server.name] && (
              <div style={{ marginTop: 12, padding: 8, background: 'rgba(0,0,0,0.2)', borderRadius: 4, position: 'relative' }}>
                <button
                  className="btn-icon"
                  style={{ position: 'absolute', right: 4, top: 4, padding: 2, fontSize: 10 }}
                  onClick={() => setTestResults(prev => {
                    const next = { ...prev }; delete next[server.name]; return next;
                  })}
                >✕</button>
                <div style={{ fontSize: 11, fontWeight: 600, color: testResults[server.name].status === 'success' ? 'var(--success)' : 'var(--error)' }}>
                  {testResults[server.name].status?.toUpperCase()}
                </div>
                {testResults[server.name].stdout && <pre style={{ fontSize: 10, whiteSpace: 'pre-wrap', color: 'var(--text-muted)', maxHeight: 100, overflow: 'auto' }}>{testResults[server.name].stdout}</pre>}
                {testResults[server.name].error && <div style={{ fontSize: 10, color: 'var(--error)' }}>{testResults[server.name].error}</div>}
              </div>
            )}
          </div>
        ))}
      </div>

      {showNew && (
        <div className="modal-overlay" onClick={() => setShowNew(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <h3 className="modal-title">Add MCP Server</h3>
            <div style={{ display: 'grid', gap: 12, marginBottom: 20 }}>
              <div>
                <label style={{ fontSize: 12, color: 'var(--text-muted)', display: 'block', marginBottom: 4 }}>Server Name</label>
                <input
                  type="text"
                  value={newServer.name}
                  onChange={e => setNewServer({ ...newServer, name: e.target.value })}
                  placeholder="e.g. documentation-helper"
                />
              </div>
              <div>
                <label style={{ fontSize: 12, color: 'var(--text-muted)', display: 'block', marginBottom: 4 }}>Command</label>
                <input
                  type="text"
                  value={newServer.command}
                  onChange={e => setNewServer({ ...newServer, command: e.target.value })}
                  placeholder="e.g. npx"
                />
              </div>
              <div>
                <label style={{ fontSize: 12, color: 'var(--text-muted)', display: 'block', marginBottom: 4 }}>Arguments (space separated)</label>
                <input
                  type="text"
                  value={newServer.args}
                  onChange={e => setNewServer({ ...newServer, args: e.target.value })}
                  placeholder="e.g. -y @modelcontextprotocol/server-memory"
                />
              </div>
            </div>
            <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end' }}>
              <button className="btn btn-secondary" onClick={() => setShowNew(false)}>Cancel</button>
              <button className="btn btn-primary" onClick={createServer}>Add Server</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
