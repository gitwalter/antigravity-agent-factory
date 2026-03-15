'use client'
import { useEffect, useState, Suspense } from 'react'
import { useSearchParams } from 'next/navigation'
import { api, Workflow, Phase as ApiPhase, Agent, Skill } from '@/lib/api'

interface Phase {
  name: string
  goal?: string
  agent: string
  skills: string[]
  tools: string[]
  description?: string
}

function WorkflowsContent() {
  const searchParams = useSearchParams()
  const editParam = searchParams.get('edit')

  const [workflows, setWorkflows] = useState<Workflow[]>([])
  const [agents, setAgents] = useState<Agent[]>([])
  const [skills, setSkills] = useState<Skill[]>([])
  const [selected, setSelected] = useState<(Workflow & { raw_body?: string }) | null>(null)

  const [editPhases, setEditPhases] = useState<Phase[]>([])
  const [editTitle, setEditTitle] = useState('')
  const [editDesc, setEditDesc] = useState('')
  const [editTags, setEditTags] = useState('')
  const [rawText, setRawText] = useState('')
  const [draft, setDraft] = useState('')

  const [search, setSearch] = useState('')
  const [showNew, setShowNew] = useState(false)
  const [newName, setNewName] = useState('')
  const [saving, setSaving] = useState(false)
  const [msg, setMsg] = useState('')
  const [loading, setLoading] = useState(true)
  const [loadingDetail, setLoadingDetail] = useState(false)
  const [activeTab, setActiveTab] = useState<'visual' | 'source' | 'draft'>('visual')

  useEffect(() => {
    Promise.all([
      api.workflows().catch(() => []),
      api.agents().catch(() => []),
      api.skills().catch(() => []),
    ]).then(([wf, ag, sk]) => {
      setWorkflows(wf)
      setAgents(ag)
      setSkills(sk)
      setLoading(false)
      if (editParam) {
        selectWorkflow(editParam)
      }
    })
  }, [editParam])

  async function selectWorkflow(filename: string) {
    setLoadingDetail(true)
    setMsg('')
    try {
      const wf = await api.workflow(filename)
      setSelected(wf)
      setEditPhases(wf.phases || [])
      setEditTitle(wf.title || filename)
      setEditDesc(wf.description || '')
      setEditTags((wf.tags || []).join(', '))
      setRawText(wf.raw_body || '')
      setActiveTab('visual')
    } catch (e) {
      setMsg('✗ Failed to load: ' + (e as Error).message)
    }
    setLoadingDetail(false)
  }

  function addPhase() {
    setEditPhases([...editPhases, { name: 'New Phase', goal: '', agent: '', skills: [], tools: [] }])
  }

  function removePhase(idx: number) {
    setEditPhases(editPhases.filter((_, i) => i !== idx))
  }

  function movePhase(idx: number, delta: number) {
    const next = idx + delta
    if (next < 0 || next >= editPhases.length) return
    const arr = [...editPhases]
    ;[arr[idx], arr[next]] = [arr[next], arr[idx]]
    setEditPhases(arr)
  }

  function updatePhase(idx: number, field: keyof Phase, value: any) {
    setEditPhases(editPhases.map((p, i) => i === idx ? { ...p, [field]: value } : p))
  }

  async function saveWorkflow() {
    if (!selected) return
    setSaving(true)
    try {
      await api.saveWorkflow(selected.filename, {
        title: editTitle,
        description: editDesc,
        tags: editTags.split(',').map(t => t.trim()).filter(Boolean),
        version: selected.version,
        phases: editPhases as any,
        raw_body: activeTab === 'source' ? rawText : undefined
      })
      setMsg('✓ Saved successfully')
      setTimeout(() => setMsg(''), 3000)
      const wf = await api.workflows()
      setWorkflows(wf)
    } catch (e) {
      setMsg('✗ Save failed: ' + (e as Error).message)
    }
    setSaving(false)
  }

  async function createWorkflow() {
    if (!newName.trim()) return
    const filename = newName.trim().toLowerCase().replace(/\s+/g, '-')
    try {
      await api.createWorkflow(filename, {
        title: newName.trim(),
        description: '',
        tags: [],
        version: '1.0.0',
        phases: [{ name: 'Step 1', goal: 'Define the goal', agent: '', skills: [], tools: [] }] as any,
      })
      setShowNew(false)
      setNewName('')
      const wf = await api.workflows()
      setWorkflows(wf)
      selectWorkflow(filename)
    } catch (e) {
      setMsg('✗ Creation failed')
    }
  }

  const filtered = workflows.filter(wf =>
    wf.filename.includes(search.toLowerCase()) ||
    (wf.title || '').toLowerCase().includes(search.toLowerCase()) ||
    (wf.description || '').toLowerCase().includes(search.toLowerCase())
  )

  if (loading) return <div style={{ textAlign: 'center', padding: 60 }}><div className="loading-spinner" /></div>

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: 20, height: 'calc(100vh - 104px)' }}>
      <div style={{ overflowY: 'auto' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
          <h2 style={{ fontSize: 16, fontWeight: 600 }}>Workflows</h2>
          <button className="btn btn-primary btn-sm" onClick={() => setShowNew(true)}>+ New</button>
        </div>
        <input
          type="search"
          placeholder="Search workflows..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          style={{ marginBottom: 12 }}
        />
        <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          {filtered.map(wf => (
            <button
              key={wf.filename}
              onClick={() => selectWorkflow(wf.filename)}
              className={`phase-node ${selected?.filename === wf.filename ? 'active' : ''}`}
              style={{ textAlign: 'left', cursor: 'pointer', display: 'flex', flexDirection: 'column', gap: 4, padding: '10px 12px' }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
                <div style={{ fontSize: 13, fontWeight: 500, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{wf.title || wf.filename}</div>
              </div>
              <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                {wf.phase_count} phases · v{wf.version}
              </div>
            </button>
          ))}
        </div>
      </div>

      <div style={{ overflowY: 'auto' }}>
        {selected ? (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
              <h2 style={{ fontSize: 18, fontWeight: 600 }}>{editTitle}</h2>
              <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                {msg && <span style={{ fontSize: 12, color: msg.startsWith('✓') ? 'var(--success)' : 'var(--error)' }}>{msg}</span>}
                <button className="btn btn-primary" onClick={saveWorkflow} disabled={saving}>
                  {saving ? 'Saving...' : '💾 Save Changes'}
                </button>
              </div>
            </div>

            <div className="tabs" style={{ marginBottom: 16 }}>
              <button className={`tab ${activeTab === 'visual' ? 'active' : ''}`} onClick={() => setActiveTab('visual')}>Visual Builder</button>
              <button className={`tab ${activeTab === 'source' ? 'active' : ''}`} onClick={() => setActiveTab('source')}>Raw Source</button>
              <button className={`tab ${activeTab === 'draft' ? 'active' : ''}`} onClick={() => setActiveTab('draft')}>Design Draft ✏️</button>
            </div>

            {activeTab === 'source' ? (
              <div className="card" style={{ height: 'calc(100vh - 250px)', padding: 0 }}>
                <textarea
                  value={rawText}
                  onChange={e => setRawText(e.target.value)}
                  style={{ width: '100%', height: '100%', background: 'transparent', color: '#a5d6ff', border: 'none', fontFamily: 'monospace', fontSize: 13, padding: 20, resize: 'none', outline: 'none' }}
                  placeholder="Paste workflow YAML + Markdown here..."
                />
              </div>
            ) : activeTab === 'draft' ? (
              <div className="card" style={{ height: 'calc(100vh - 250px)', padding: 24 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
                  <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>Draft your workflow logic here before committing to formal phases.</p>
                  <button className="btn btn-secondary btn-sm" onClick={() => { setRawText(draft); setActiveTab('source'); }}>Promote to Source</button>
                </div>
                <textarea
                  placeholder="E.g. Step 1: Research, Step 2: Implement..."
                  value={draft}
                  onChange={e => setDraft(e.target.value)}
                  style={{ width: '100%', height: 'calc(100% - 40px)', background: 'rgba(0,0,0,0.15)', color: 'var(--text-secondary)', padding: 24, borderRadius: 8, border: '1px dashed var(--border)', fontFamily: 'monospace', outline: 'none', resize: 'none' }}
                />
              </div>
            ) : (
              <>
                <div className="card" style={{ marginBottom: 16 }}>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
                    <div>
                      <label style={{ fontSize: 11, color: 'var(--text-secondary)', fontWeight: 600, display: 'block', marginBottom: 4 }}>Title</label>
                      <input type="text" value={editTitle} onChange={e => setEditTitle(e.target.value)} />
                    </div>
                    <div>
                      <label style={{ fontSize: 11, color: 'var(--text-secondary)', fontWeight: 600, display: 'block', marginBottom: 4 }}>Tags (comma-separated)</label>
                      <input type="text" value={editTags} onChange={e => setEditTags(e.target.value)} />
                    </div>
                  </div>
                  <div style={{ marginTop: 12 }}>
                    <label style={{ fontSize: 11, color: 'var(--text-secondary)', fontWeight: 600, display: 'block', marginBottom: 4 }}>Description</label>
                    <input type="text" value={editDesc} onChange={e => setEditDesc(e.target.value)} />
                  </div>
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                  <h3 style={{ fontSize: 14, fontWeight: 600 }}>Phases</h3>
                  <button className="btn btn-secondary btn-sm" onClick={addPhase}>+ Add Phase</button>
                </div>

                <div className="workflow-canvas">
                  {editPhases.map((phase, idx) => (
                    <div key={idx}>
                      <div className="phase-node active">
                        <div className="phase-node-header">
                          <div style={{ display: 'flex', alignItems: 'center' }}>
                            <span className="phase-number">{idx + 1}</span>
                            <input
                              type="text"
                              value={phase.name}
                              onChange={e => updatePhase(idx, 'name', e.target.value)}
                              style={{ background: 'transparent', border: 'none', color: 'var(--text-primary)', fontWeight: 700, fontSize: 14, padding: 0 }}
                            />
                          </div>
                          <div style={{ display: 'flex', gap: 4 }}>
                            <button className="btn-icon" onClick={() => movePhase(idx, -1)} disabled={idx === 0}>↑</button>
                            <button className="btn-icon" onClick={() => movePhase(idx, 1)} disabled={idx === editPhases.length - 1}>↓</button>
                            <button className="btn-icon" onClick={() => removePhase(idx)} style={{ color: 'var(--error)' }}>✕</button>
                          </div>
                        </div>
                        <div style={{ marginTop: 10, display: 'grid', gap: 12 }}>
                          <div>
                            <label style={{ fontSize: 10, color: 'var(--text-muted)', fontWeight: 600 }}>GOAL</label>
                            <input type="text" value={phase.goal} onChange={e => updatePhase(idx, 'goal', e.target.value)} />
                          </div>
                          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
                            <div>
                              <label style={{ fontSize: 10, color: 'var(--text-muted)', fontWeight: 600 }}>AGENT</label>
                              <select value={phase.agent} onChange={e => updatePhase(idx, 'agent', e.target.value)}>
                                <option value="">— Generic —</option>
                                {agents.map(a => <option key={a.name} value={a.name}>{a.name}</option>)}
                              </select>
                            </div>
                            <div>
                              <label style={{ fontSize: 10, color: 'var(--text-muted)', fontWeight: 600 }}>TOOLS</label>
                              <input
                                type="text"
                                value={(phase.tools || []).join(', ')}
                                onChange={e => updatePhase(idx, 'tools', e.target.value.split(',').map(s => s.trim()))}
                              />
                            </div>
                          </div>
                        </div>
                      </div>
                      {idx < editPhases.length - 1 && <div className="phase-connector" />}
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        ) : (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-muted)' }}>
            <p>Select a workflow from the list or create a new one</p>
          </div>
        )}
      </div>

      {showNew && (
        <div className="modal-overlay" onClick={() => setShowNew(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <h3 className="modal-title">Create New Workflow</h3>
            <div style={{ marginBottom: 16 }}>
              <label style={{ fontSize: 12, color: 'var(--text-muted)', display: 'block', marginBottom: 4 }}>Workflow Name</label>
              <input type="text" value={newName} onChange={e => setNewName(e.target.value)} placeholder="e.g. My Custom Pipeline" autoFocus />
            </div>
            <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end' }}>
              <button className="btn btn-secondary" onClick={() => setShowNew(false)}>Cancel</button>
              <button className="btn btn-primary" onClick={createWorkflow}>Create</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default function WorkflowsPage() {
  return (
    <Suspense fallback={<div style={{ textAlign: 'center', padding: 60 }}><div className="loading-spinner" /></div>}>
      <WorkflowsContent />
    </Suspense>
  )
}
