'use client'
import { useEffect, useState, Suspense, useCallback, useMemo } from 'react'
import { useSearchParams } from 'next/navigation'
import { api, Workflow, Agent, Skill, Phase } from '@/lib/api'
import ReactFlow, {
  Node,
  Edge,
  Controls,
  Background,
  Handle,
  Position,
  ConnectionMode,
  useNodesState,
  useEdgesState,
  addEdge,
  OnNodesChange,
  OnEdgesChange,
  OnConnect,
  XYPosition
} from 'reactflow'
import 'reactflow/dist/style.css'

// Custom Node for Workflow Phases
const WorkflowNode = ({ data }: { data: any }) => {
  return (
    <div className={`phase-node ${data.active ? 'active' : ''}`} style={{
      minWidth: 260,
      padding: '20px 24px',
      background: 'rgba(15, 15, 25, 0.95)',
      border: '2px solid rgba(139, 110, 255, 0.6)',
      borderRadius: 12,
      boxShadow: '0 10px 40px rgba(0,0,0,0.6), 0 0 20px rgba(139, 110, 255, 0.1)',
      backdropFilter: 'blur(20px)',
      color: 'white',
      transition: 'all 0.3s ease'
    }}>
      <Handle type="target" position={Position.Top} style={{ background: '#8b6eff', width: 10, height: 10, border: '2px solid #0f0f19' }} />
      <div style={{ fontSize: 10, color: '#8b6eff', fontWeight: 900, textTransform: 'uppercase', marginBottom: 6, letterSpacing: '0.1em' }}>Phase {data.index + 1}</div>
      <div style={{ fontSize: 16, fontWeight: 800, marginBottom: 12, letterSpacing: '-0.02em', color: '#f8fafc' }}>{data.name || data.label}</div>
      {data.goal && (
        <div style={{ fontSize: 12, color: '#94a3b8', fontStyle: 'italic', marginBottom: 14, lineHeight: 1.5, background: 'rgba(255,255,255,0.03)', padding: '8px 12px', borderRadius: 8, borderLeft: '3px solid #8b6eff' }}>
          "{data.goal}"
        </div>
      )}
      <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginTop: 12 }}>
        {data.agents?.map((a: string) => <span key={a} className="tag" style={{ fontSize: 10, background: 'rgba(139, 110, 255, 0.15)', border: '1px solid rgba(139, 110, 255, 0.3)', color: '#a78bfa' }}>👤 {a}</span>)}
        {data.skills?.map((s: string) => <span key={s} className="tag tag-success" style={{ fontSize: 10, background: 'rgba(34, 197, 94, 0.1)', border: '1px solid rgba(34, 197, 94, 0.2)', color: '#4ade80' }}>🧩 {s}</span>)}
      </div>
      <Handle type="source" position={Position.Bottom} style={{ background: '#8b6eff', width: 10, height: 10, border: '2px solid #0f0f19' }} />
    </div>
  )
}

const nodeTypes = {
  workflowNode: WorkflowNode,
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

  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])
  const [selectedPhaseIndex, setSelectedPhaseIndex] = useState<number | null>(null)

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

      // Initialize Graph
      const initialNodes: Node[] = (wf.phases || []).map((p, i) => ({
        id: `phase-${i}`,
        type: 'workflowNode',
        data: { ...p, index: i, active: true },
        position: { x: 250, y: i * 150 + 50 },
      }))
      setNodes(initialNodes)

      const initialEdges: Edge[] = []
      for (let i = 0; i < initialNodes.length - 1; i++) {
        initialEdges.push({
          id: `e${i}-${i+1}`,
          source: initialNodes[i].id,
          target: initialNodes[i+1].id,
          animated: true,
          style: { stroke: '#8b6eff', strokeWidth: 3, opacity: 0.8 },
        })
      }
      setEdges(initialEdges)
      setSelectedPhaseIndex(null)
    } catch (e) {
      setMsg('✗ Failed to load: ' + (e as Error).message)
    }
    setLoadingDetail(false)
  }

  const onConnect: OnConnect = useCallback((params) => {
    setEdges((eds) => addEdge({ ...params, animated: true, style: { stroke: '#8b6eff', strokeWidth: 2 } }, eds))
  }, [setEdges])

  const onNodeClick = useCallback((_: any, node: Node) => {
    const idx = node.data.index
    setSelectedPhaseIndex(idx)
  }, [])

  const updatePhaseField = (idx: number, field: keyof Phase, value: any) => {
    const updated = [...editPhases]
    updated[idx] = { ...updated[idx], [field]: value }
    setEditPhases(updated)

    // Also update node data
    setNodes((nds) =>
      nds.map((n) => {
        if (n.data.index === idx) {
          return { ...n, data: { ...n.data, [field]: value } }
        }
        return n
      })
    )
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
        phases: [{ name: 'Step 1', goal: 'Define the goal', agents: [], skills: [], tools: [], actions: [] }] as any,
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
      <div style={{ overflowY: 'auto', borderRight: '1px solid var(--border-color)', paddingRight: 20 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
          <h2 style={{ fontSize: 16, fontWeight: 600 }}>Workflows</h2>
          <button className="btn btn-primary btn-sm" onClick={() => setShowNew(true)}>+ New</button>
        </div>
        <input
          type="search"
          placeholder="Search workflows..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          style={{ marginBottom: 16, width: '100%' }}
        />
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          {filtered.map(wf => (
            <button
              key={wf.filename}
              onClick={() => selectWorkflow(wf.filename)}
              className={`phase-node ${selected?.filename === wf.filename ? 'active' : ''}`}
              style={{ textAlign: 'left', cursor: 'pointer', display: 'flex', flexDirection: 'column', gap: 4, padding: '10px 12px', background: 'transparent', border: 'none', borderRadius: 8 }}
            >
              <div style={{ fontSize: 13, fontWeight: 500, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{wf.title || wf.filename}</div>
              <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                {wf.phase_count} phases · v{wf.version}
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
                <h2 style={{ fontSize: 18, fontWeight: 600 }}>{editTitle}</h2>
                <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>{selected.filename}</div>
              </div>
              <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
                <div className="tab-group" style={{ display: 'flex', background: 'rgba(255,255,255,0.05)', padding: 4, borderRadius: 8 }}>
                  <button className={`tab ${activeTab === 'visual' ? 'active' : ''}`} onClick={() => setActiveTab('visual')} style={{ padding: '4px 12px', fontSize: 12, borderRadius: 6, border: 'none', background: activeTab === 'visual' ? 'var(--accent)' : 'transparent', color: activeTab === 'visual' ? 'white' : 'var(--text-muted)', cursor: 'pointer' }}>Graph</button>
                  <button className={`tab ${activeTab === 'source' ? 'active' : ''}`} onClick={() => setActiveTab('source')} style={{ padding: '4px 12px', fontSize: 12, borderRadius: 6, border: 'none', background: activeTab === 'source' ? 'var(--accent)' : 'transparent', color: activeTab === 'source' ? 'white' : 'var(--text-muted)', cursor: 'pointer' }}>Source</button>
                  <button className={`tab ${activeTab === 'draft' ? 'active' : ''}`} onClick={() => setActiveTab('draft')} style={{ padding: '4px 12px', fontSize: 12, borderRadius: 6, border: 'none', background: activeTab === 'draft' ? 'var(--accent)' : 'transparent', color: activeTab === 'draft' ? 'white' : 'var(--text-muted)', cursor: 'pointer' }}>Draft ✏️</button>
                </div>
                {msg && <span style={{ fontSize: 12, color: msg.startsWith('✓') ? 'var(--success)' : 'var(--error)' }}>{msg}</span>}
                <button className="btn btn-primary" onClick={saveWorkflow} disabled={saving}>
                  {saving ? 'Saving...' : '💾 Save'}
                </button>
              </div>
            </div>

            <div className="card" style={{ flex: 1, padding: 0, overflow: 'hidden', display: 'flex', flexDirection: 'column', background: 'rgba(10, 10, 15, 0.4)', backdropFilter: 'blur(20px)', border: '1px solid rgba(255,255,255,0.1)', position: 'relative' }}>
              {activeTab === 'visual' ? (
                <div style={{ width: '100%', height: '100%' }}>
                  <button
                    onClick={() => {
                      const newIdx = editPhases.length
                      const newPhase: Phase = { name: `Phase ${newIdx + 1}`, goal: '', agents: [], skills: [], tools: [], actions: [] }
                      setEditPhases([...editPhases, newPhase])
                      const newNode: Node = {
                        id: `phase-${newIdx}`,
                        type: 'workflowNode',
                        data: { ...newPhase, index: newIdx, active: true },
                        position: { x: 250, y: newIdx * 150 + 50 },
                      }
                      setNodes((nds) => [...nds, newNode])
                      setSelectedPhaseIndex(newIdx)
                    }}
                    style={{ position: 'absolute', top: 20, left: 20, zIndex: 10, padding: '8px 16px', background: 'var(--accent)', color: 'white', border: 'none', borderRadius: 8, cursor: 'pointer', fontWeight: 600, boxShadow: '0 4px 15px rgba(0,0,0,0.3)' }}
                  >
                    + Add Phase
                  </button>
                  <ReactFlow
                    nodes={nodes}
                    edges={edges}
                    onNodesChange={onNodesChange}
                    onEdgesChange={onEdgesChange}
                    onConnect={onConnect}
                    onNodeClick={onNodeClick}
                    nodeTypes={nodeTypes}
                    connectionMode={ConnectionMode.Loose}
                    fitView
                  >
                    <Controls />
                    <Background color="rgba(255,255,255,0.05)" gap={20} />
                  </ReactFlow>

                  {selectedPhaseIndex !== null && (
                    <div className="sidebar-detail" style={{ position: 'absolute', right: 0, top: 0, bottom: 0, width: 350, background: 'rgba(15, 15, 25, 0.95)', backdropFilter: 'blur(10px)', borderLeft: '1px solid rgba(255,255,255,0.1)', zIndex: 10, padding: 24, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 20, boxShadow: '-10px 0 30px rgba(0,0,0,0.5)' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <h3 style={{ fontSize: 16, fontWeight: 700, color: 'var(--accent)' }}>Phase {selectedPhaseIndex + 1} Details</h3>
                        <button onClick={() => setSelectedPhaseIndex(null)} style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: 20 }}>&times;</button>
                      </div>

                      <div className="form-group">
                        <label>Phase Name</label>
                        <input
                          type="text"
                          value={editPhases[selectedPhaseIndex]?.name || ''}
                          onChange={(e) => updatePhaseField(selectedPhaseIndex, 'name', e.target.value)}
                        />
                      </div>

                      <div className="form-group">
                        <label>Goal / Objective</label>
                        <textarea
                          rows={3}
                          value={editPhases[selectedPhaseIndex]?.goal || ''}
                          onChange={(e) => updatePhaseField(selectedPhaseIndex, 'goal', e.target.value)}
                          style={{ width: '100%', padding: '10px 12px', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border)', borderRadius: 8, color: 'white', fontSize: 13, outline: 'none' }}
                        />
                      </div>

                      <div className="form-group">
                        <label>Assigned Agents</label>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: 6, maxHeight: 150, overflowY: 'auto', padding: 10, background: 'rgba(0,0,0,0.2)', borderRadius: 8 }}>
                          {agents.map(a => (
                            <label key={a.id} style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 12, cursor: 'pointer', padding: '4px 0' }}>
                              <input
                                type="checkbox"
                                checked={(editPhases[selectedPhaseIndex]?.agents || []).includes(a.id)}
                                onChange={(e) => {
                                  const current = editPhases[selectedPhaseIndex]?.agents || []
                                  const next = e.target.checked ? [...current, a.id] : current.filter(id => id !== a.id)
                                  updatePhaseField(selectedPhaseIndex, 'agents', next)
                                }}
                              />
                              <span style={{ color: 'white' }}>👤 {a.name}</span>
                            </label>
                          ))}
                        </div>
                      </div>

                      <div className="form-group">
                        <label>Required Skills</label>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: 6, maxHeight: 200, overflowY: 'auto', padding: 10, background: 'rgba(0,0,0,0.2)', borderRadius: 8 }}>
                          {skills.map(s => (
                            <label key={s.id} style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 12, cursor: 'pointer' }}>
                              <input
                                type="checkbox"
                                checked={(editPhases[selectedPhaseIndex]?.skills || []).includes(s.id)}
                                onChange={(e) => {
                                  const current = editPhases[selectedPhaseIndex]?.skills || []
                                  const next = e.target.checked ? [...current, s.id] : current.filter(id => id !== s.id)
                                  updatePhaseField(selectedPhaseIndex, 'skills', next)
                                }}
                              />
                              {s.name}
                            </label>
                          ))}
                        </div>
                      </div>

                      <div style={{ marginTop: 'auto', display: 'flex', gap: 10 }}>
                        <button className="btn btn-secondary btn-sm" style={{ flex: 1 }} onClick={() => {
                          const updated = editPhases.filter((_, i) => i !== selectedPhaseIndex)
                          setEditPhases(updated)
                          setNodes(nds => nds.filter(n => n.data.index !== selectedPhaseIndex).map((n, i) => ({ ...n, data: { ...n.data, index: i } })))
                          setSelectedPhaseIndex(null)
                        }}>🗑️ Delete Phase</button>
                      </div>
                    </div>
                  )}
                </div>
              ) : activeTab === 'source' ? (
                <textarea
                  value={rawText}
                  onChange={e => setRawText(e.target.value)}
                  style={{ width: '100%', height: '100%', background: 'transparent', color: '#a5d6ff', border: 'none', fontFamily: 'monospace', fontSize: 13, padding: 20, resize: 'none', outline: 'none' }}
                />
              ) : (
                <div style={{ padding: 24, height: '100%', display: 'flex', flexDirection: 'column' }}>
                  <p style={{ fontSize: 13, color: 'var(--text-muted)', marginBottom: 12 }}>Draft your workflow logic here before committing to formal phases.</p>
                  <textarea
                    value={draft}
                    onChange={e => setDraft(e.target.value)}
                    style={{ flex: 1, width: '100%', background: 'rgba(0,0,0,0.15)', color: 'var(--text-secondary)', padding: 24, borderRadius: 8, border: '1px dashed var(--border)', fontFamily: 'monospace', outline: 'none', resize: 'none' }}
                  />
                </div>
              )}
            </div>
          </>
        ) : (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-muted)' }}>
            <p>Select a workflow from the list or create a new one</p>
          </div>
        )}
      </div>

      {showNew && (
        <div className="modal-overlay" onClick={() => setShowNew(false)} style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.8)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
          <div className="modal card" onClick={e => e.stopPropagation()} style={{ width: 400, padding: 24 }}>
            <h3 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Create New Workflow</h3>
            <div style={{ marginBottom: 20 }}>
              <label style={{ fontSize: 12, color: 'var(--text-muted)', display: 'block', marginBottom: 6 }}>Workflow Name</label>
              <input type="text" value={newName} onChange={e => setNewName(e.target.value)} placeholder="e.g. My Custom Pipeline" autoFocus style={{ width: '100%' }} />
            </div>
            <div style={{ display: 'flex', gap: 12, justifyContent: 'flex-end' }}>
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
