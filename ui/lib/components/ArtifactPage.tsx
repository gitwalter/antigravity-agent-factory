'use client'
import { useEffect, useState, Suspense } from 'react'
import { api } from '@/lib/api'

interface Artifact {
  name: string
  path: string
  title: string
  description: string
}

interface ArtifactPageProps {
  title: string
  fetchList: () => Promise<Artifact[]>
  searchPlaceholder?: string
  artifactType: string
}

export default function ArtifactPage({ title, fetchList, searchPlaceholder, artifactType }: ArtifactPageProps) {
  const [artifacts, setArtifacts] = useState<Artifact[]>([])
  const [selected, setSelected] = useState<{ path: string; name: string; content: string } | null>(null)
  const [editContent, setEditContent] = useState('')
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [msg, setMsg] = useState('')

  useEffect(() => {
    fetchList().then(list => {
      setArtifacts(list)
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [fetchList])

  async function selectArtifact(path: string) {
    setMsg('')
    try {
      const art = await api.artifact(path)
      setSelected(art)
      setEditContent(art.content)
    } catch (e) {
      setMsg('✗ Failed to load: ' + (e as Error).message)
    }
  }

  async function saveArtifact() {
    if (!selected) return
    setSaving(true)
    try {
      await api.saveArtifact(selected.path, editContent)
      setMsg('✓ Saved successfully')
      setTimeout(() => setMsg(''), 3000)
    } catch (e) {
      setMsg('✗ Save failed: ' + (e as Error).message)
    }
    setSaving(false)
  }

  const filtered = artifacts.filter(a =>
    a.name.toLowerCase().includes(search.toLowerCase()) ||
    (a.title || '').toLowerCase().includes(search.toLowerCase()) ||
    (a.description || '').toLowerCase().includes(search.toLowerCase())
  )

  if (loading) return <div style={{ textAlign: 'center', padding: 60 }}><div className="loading-spinner" /></div>

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: 20, height: 'calc(100vh - 104px)' }}>
      <div style={{ overflowY: 'auto' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
          <h2 style={{ fontSize: 16, fontWeight: 600 }}>{title}</h2>
        </div>
        <input
          type="search"
          placeholder={searchPlaceholder || `Search ${artifactType}...`}
          value={search}
          onChange={e => setSearch(e.target.value)}
          style={{ marginBottom: 12 }}
        />
        <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          {filtered.map(a => (
            <button
              key={a.path}
              onClick={() => selectArtifact(a.path)}
              className={`phase-node ${selected?.path === a.path ? 'active' : ''}`}
              style={{ textAlign: 'left', cursor: 'pointer', display: 'flex', flexDirection: 'column', gap: 4, padding: '10px 12px' }}
            >
              <div style={{ fontSize: 13, fontWeight: 500, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{a.title || a.name}</div>
              <div style={{ fontSize: 11, color: 'var(--text-muted)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                {a.path}
              </div>
            </button>
          ))}
        </div>
      </div>

      <div style={{ overflowY: 'auto' }}>
        {selected ? (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
              <div style={{ overflow: 'hidden' }}>
                <h2 style={{ fontSize: 18, fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{selected.name}</h2>
                <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>{selected.path}</div>
              </div>
              <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                {msg && <span style={{ fontSize: 12, color: msg.startsWith('✓') ? 'var(--success)' : 'var(--error)' }}>{msg}</span>}
                <button className="btn btn-primary" onClick={saveArtifact} disabled={saving}>
                  {saving ? 'Saving...' : '💾 Save Changes'}
                </button>
              </div>
            </div>

            <div className="card" style={{ height: 'calc(100vh - 200px)', padding: 0 }}>
              <textarea
                value={editContent}
                onChange={e => setEditContent(e.target.value)}
                style={{ width: '100%', height: '100%', background: 'transparent', color: '#a5d6ff', border: 'none', fontFamily: 'monospace', fontSize: 13, padding: 20, resize: 'none', outline: 'none' }}
                placeholder="Edit artifact content..."
              />
            </div>
          </div>
        ) : (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-muted)' }}>
            <p>Select a {artifactType.toLowerCase()} from the list to view or edit</p>
          </div>
        )}
      </div>
    </div>
  )
}
