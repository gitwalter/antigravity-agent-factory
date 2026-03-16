'use client'
import { useEffect, useState, useRef, useMemo } from 'react'
import { api } from '@/lib/api'
import JsonView from '@uiw/react-json-view'
import { JSONEditor } from 'vanilla-jsoneditor'
import 'vanilla-jsoneditor/themes/jse-theme-dark.css'
import yaml from 'js-yaml'
import { parseFrontmatter } from '@/lib/yaml'
import { TriPaneArtifactEditor } from './TriPaneArtifactEditor'

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
  const [viewMode, setViewMode] = useState<'code' | 'tree' | 'metadata'>('code')

  // JSON Editor Ref
  const editorRef = useRef<HTMLDivElement>(null)
  const editorInstance = useRef<any>(null)

  useEffect(() => {
    fetchList().then(list => {
      setArtifacts(list)
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [fetchList])

  // Initialize/Update Vanilla JSON Editor
  useEffect(() => {
    if (editorRef.current && viewMode === 'code' && selected) {
      if (!editorInstance.current) {
        editorInstance.current = new (JSONEditor as any)({
          target: editorRef.current,
          props: {
            content: { text: editContent },
            mode: 'text' as any, // Use text mode for raw JSON editing
            onChange: (updatedContent: any) => {
              // @ts-ignore
              if (updatedContent.text !== undefined) {
                // @ts-ignore
                setEditContent(updatedContent.text)
              }
            },
            theme: 'jse-theme-dark'
          }
        })
      } else {
        editorInstance.current.update({ content: { text: editContent } })
      }
    }

    return () => {
      if (editorInstance.current) {
        editorInstance.current.destroy()
        editorInstance.current = null
      }
    }
  }, [viewMode, selected])

  async function selectArtifact(path: string) {
    setMsg('')
    try {
      const art = await api.artifact(path)
      setSelected(art)
      setEditContent(art.content)
      // Auto-switch to tree if it's JSON or YAML
      const isRule = path.includes('.agent/rules/') || false
      if (isJson || isYaml || isRule) {
        setViewMode(isRule || isYaml ? 'metadata' : 'tree')
      } else {
        setViewMode('code')
      }
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

  const isJson = selected?.path.endsWith('.json') || false
  const isYaml = selected?.path.endsWith('.yaml') || selected?.path.endsWith('.yml') || selected?.content.startsWith('---\n') || false
  const isRule = selected?.path.includes('.agent/rules/') || false

  const parsedData = useMemo(() => {
    if (!selected) return null
    if (!isJson && !isYaml && !isRule) return null

    try {
      if (isYaml || isRule) {
        const { data } = parseFrontmatter(editContent)
        return data || {}
      }
      return JSON.parse(editContent)
    } catch (e) {
      return { error: `Invalid ${isJson ? 'JSON' : 'YAML'}`, message: (e as Error).message }
    }
  }, [editContent, selected, isJson, isYaml, isRule])

  if (loading) return <div style={{ textAlign: 'center', padding: 60 }}><div className="loading-spinner" /></div>

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: 20, height: 'calc(100vh - 104px)' }}>
      <div style={{ overflowY: 'auto', borderRight: '1px solid var(--border-color)', paddingRight: 20 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
          <h2 style={{ fontSize: 16, fontWeight: 600 }}>{title}</h2>
        </div>
        <input
          type="search"
          placeholder={searchPlaceholder || `Search ${artifactType}...`}
          value={search}
          onChange={e => setSearch(e.target.value)}
          style={{ marginBottom: 16, width: '100%' }}
        />
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          {filtered.map(a => (
            <button
              key={a.path}
              onClick={() => selectArtifact(a.path)}
              className={`phase-node ${selected?.path === a.path ? 'active' : ''}`}
              style={{ textAlign: 'left', cursor: 'pointer', display: 'flex', flexDirection: 'column', gap: 4, padding: '10px 12px', border: 'none', background: 'transparent', borderRadius: 8, transition: 'all 0.2s' }}
            >
              <div style={{ fontSize: 13, fontWeight: 500, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{a.title || a.name}</div>
              <div style={{ fontSize: 11, color: 'var(--text-muted)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                {a.path}
              </div>
            </button>
          ))}
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
        {selected ? (
          <>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
              <div style={{ overflow: 'hidden' }}>
                <h2 style={{ fontSize: 18, fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{selected.name}</h2>
                <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>{selected.path}</div>
              </div>
              <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
                <div className="tab-group" style={{ display: 'flex', background: 'rgba(255,255,255,0.05)', padding: 4, borderRadius: 8 }}>
                  <button
                    className={`tab ${viewMode === 'code' ? 'active' : ''}`}
                    onClick={() => setViewMode('code')}
                    style={{ padding: '4px 12px', fontSize: 12, borderRadius: 6, border: 'none', background: viewMode === 'code' ? 'var(--accent)' : 'transparent', color: viewMode === 'code' ? 'white' : 'var(--text-muted)', cursor: 'pointer' }}
                  >
                    Code
                  </button>
                  {isYaml && (
                    <button
                      className={`tab ${viewMode === 'metadata' ? 'active' : ''}`}
                      onClick={() => setViewMode('metadata')}
                      style={{ padding: '4px 12px', fontSize: 12, borderRadius: 6, border: 'none', background: viewMode === 'metadata' ? 'var(--accent)' : 'transparent', color: viewMode === 'metadata' ? 'white' : 'var(--text-muted)', cursor: 'pointer' }}
                    >
                      Metadata
                    </button>
                  )}
                  {(isJson || isYaml || isRule) && (
                    <button
                      className={`tab ${viewMode === 'tree' ? 'active' : ''}`}
                      onClick={() => setViewMode('tree')}
                      style={{ padding: '4px 12px', fontSize: 12, borderRadius: 6, border: 'none', background: viewMode === 'tree' ? 'var(--accent)' : 'transparent', color: viewMode === 'tree' ? 'white' : 'var(--text-muted)', cursor: 'pointer' }}
                    >
                      Tree
                    </button>
                  )}
                </div>
                {msg && <span style={{ fontSize: 12, color: msg.startsWith('✓') ? 'var(--success)' : 'var(--error)' }}>{msg}</span>}
                <button className="btn btn-primary" onClick={saveArtifact} disabled={saving}>
                  {saving ? 'Saving...' : '💾 Save'}
                </button>
              </div>
            </div>

            <div className="card" style={{ flex: 1, padding: 0, overflow: 'hidden', display: 'flex', flexDirection: 'column', background: 'rgba(10, 10, 15, 0.4)', backdropFilter: 'blur(20px)', border: '1px solid rgba(255,255,255,0.1)' }}>
              {viewMode === 'code' ? (
                <div ref={editorRef} style={{ height: '100%', width: '100%' }} />
              ) : viewMode === 'tree' ? (
                <div style={{ height: '100%', overflow: 'auto', padding: 20 }}>
                  <JsonView
                    value={parsedData || {}}
                    displayDataTypes={false}
                    displayObjectSize={true}
                    style={{
                      '--w-rjv-background-color': 'transparent',
                      '--w-rjv-color': '#d1d5db',
                      '--w-rjv-key-string': '#7dd3fc',
                      '--w-rjv-key-number': '#fbbf24',
                      '--w-rjv-key-boolean': '#f87171',
                      '--w-rjv-line-color': 'rgba(255,255,255,0.1)',
                    } as any}
                  />
                </div>
              ) : viewMode === 'metadata' && (isYaml || isRule) && (selected.path.includes('.agent') || isRule) ? (
                <div style={{ height: '100%', overflow: 'hidden' }}>
                    <TriPaneArtifactEditor
                        content={editContent}
                        path={selected.path}
                        onSave={(newContent) => {
                            setEditContent(newContent)
                            saveArtifact()
                        }}
                    />
                </div>
              ) : (
                <div style={{ height: '100%', overflow: 'auto', padding: 24 }}>
                  <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 12, overflow: 'hidden', boxShadow: '0 4px 20px rgba(0,0,0,0.3)' }}>
                    <thead>
                      <tr style={{ background: 'rgba(255,255,255,0.05)', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                        <th style={{ padding: '14px 20px', textAlign: 'left', fontSize: 12, textTransform: 'uppercase', color: '#94a3b8', letterSpacing: '0.05em' }}>Key</th>
                        <th style={{ padding: '14px 20px', textAlign: 'left', fontSize: 12, textTransform: 'uppercase', color: '#94a3b8', letterSpacing: '0.05em' }}>Value</th>
                      </tr>
                    </thead>
                    <tbody>
                      {parsedData && typeof parsedData === 'object' && !Array.isArray(parsedData) ? (
                        Object.entries(parsedData).map(([key, val], idx) => (
                          <tr key={key} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)', background: idx % 2 === 0 ? 'rgba(255,255,255,0.01)' : 'transparent', transition: 'background 0.2s' }}>
                            <td style={{ padding: '14px 20px', color: '#8b6eff', width: '220px', fontSize: 13, borderRight: '1px solid rgba(255,255,255,0.05)', fontWeight: 700, verticalAlign: 'top' }}>{key}</td>
                            <td style={{ padding: '14px 20px', color: '#f8fafc', fontSize: 13, lineHeight: 1.6 }}>
                              {Array.isArray(val) ? (
                                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                                  {val.map((item, i) => <span key={i} style={{ background: 'rgba(139, 110, 255, 0.1)', border: '1px solid rgba(139, 110, 255, 0.2)', color: '#a78bfa', borderRadius: 6, padding: '4px 10px', fontSize: 11, fontWeight: 500 }}>{String(item)}</span>)}
                                </div>
                              ) : typeof val === 'object' && val !== null ? (
                                <pre style={{ margin: 0, fontSize: 12, color: '#38bdf8', background: 'rgba(0,0,0,0.2)', padding: 12, borderRadius: 8, border: '1px solid rgba(255,255,255,0.05)' }}>{JSON.stringify(val, null, 2)}</pre>
                              ) : (
                                <span style={{ fontWeight: 500 }}>{String(val)}</span>
                              )}
                            </td>
                          </tr>
                        ))
                      ) : (
                        <tr><td colSpan={2} style={{ padding: 40, color: '#94a3b8', textAlign: 'center', fontSize: 14, fontStyle: 'italic' }}>No structured metadata found.</td></tr>
                      )}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </>
        ) : (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-muted)' }}>
            <p>Select a {artifactType.toLowerCase()} from the list to view or edit</p>
          </div>
        )}
      </div>
    </div>
  )
}
