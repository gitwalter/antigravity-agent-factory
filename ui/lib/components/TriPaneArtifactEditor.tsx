'use client'

import React, { useState, useEffect, useCallback, useMemo } from 'react'
import Form from '@rjsf/core'
import validator from '@rjsf/validator-ajv8'
import ReactFlow, {
  Node,
  Edge,
  Background,
  Controls,
  ConnectionMode,
  useNodesState,
  useEdgesState,
  addEdge,
  OnConnect,
  MarkerType
} from 'reactflow'
import 'reactflow/dist/style.css'
import Editor from '@monaco-editor/react'
import matter from 'gray-matter'
import yaml from 'js-yaml'

interface TriPaneArtifactEditorProps {
  content: string
  path: string
  onSave?: (newContent: string) => void
}

export const TriPaneArtifactEditor: React.FC<TriPaneArtifactEditorProps> = ({
  content,
  path,
  onSave
}) => {
  const [rawContent, setRawContent] = useState(content)
  const [parsed, setParsed] = useState<any>({ data: {}, content: '' })
  const [schema, setSchema] = useState<any>(null)

  // ReactFlow state
  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])

  // Initialize and Sync
  useEffect(() => {
    try {
      const { data, content: body } = matter(content)
      setParsed({ data, content: body })
      setRawContent(content)

      // Determine artifact type and fetch schema
      const type = data.type || (path.includes('agents') ? 'agent' : path.includes('workflows') ? 'workflow' : path.includes('rules') ? 'rule' : 'skill')
      fetchSchema(type)

      // Initialize graph
      initGraph(data, type)
    } catch (e) {
      console.error("Error parsing artifact", e)
    }
  }, [content, path])

  const fetchSchema = async (type: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/schemas/${type}`)
      if (response.ok) {
        const s = await response.json()
        setSchema(s)
      }
    } catch (e) {
      console.warn("Could not load schema for", type)
    }
  }

  const initGraph = (data: any, type: string) => {
    if (type === 'workflow' && data.phases) {
      const newNodes: Node[] = data.phases.map((p: any, i: number) => ({
        id: `phase-${i}`,
        data: { name: p.name, goal: p.goal, index: i },
        position: { x: 50, y: i * 200 },
        type: 'default',
        style: {
            background: 'rgba(30, 35, 45, 0.95)',
            color: 'white',
            border: '2px solid #8b6eff',
            borderRadius: 16,
            padding: '16px 20px',
            width: 240,
            boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
            backdropFilter: 'blur(10px)'
        }
      }))

      setNodes(newNodes.map(node => ({
        ...node,
        data: {
            ...node.data,
            label: (
                <div style={{ textAlign: 'left' }}>
                    <div style={{ fontSize: 9, color: '#8b6eff', fontWeight: 800, textTransform: 'uppercase', marginBottom: 4 }}>Phase {node.data.index + 1}</div>
                    <div style={{ fontSize: 13, fontWeight: 700, marginBottom: 6 }}>{node.data.name}</div>
                    {node.data.goal && <div style={{ fontSize: 10, color: '#7878a0', fontStyle: 'italic', lineHeight: 1.4, marginBottom: 8 }}>"{node.data.goal}"</div>}
                    <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
                        {node.data.agents?.map((a: string) => <span key={a} style={{ background: 'rgba(139, 110, 255, 0.2)', border: '1px solid #8b6eff', borderRadius: 4, padding: '2px 4px', fontSize: 8 }}>👤 {a}</span>)}
                    </div>
                </div>
            )
        }
      })))
    } else if (type === 'agent') {
      // Show agent in center, skills around it
      const newNodes: Node[] = [
        {
          id: 'agent-root',
          data: { label: data.name || 'Agent' },
          position: { x: 250, y: 100 },
          type: 'default',
          style: { background: '#1a1a2f', color: 'white', border: '2px solid #8b6eff', borderRadius: 12, padding: 20, width: 200, textAlign: 'center', fontWeight: 'bold' }
        }
      ]

      const skills = data.skills || []
      const newEdges: Edge[] = []

      skills.forEach((skill: string, i: number) => {
        const radius = 200
        const angle = (i / skills.length) * 2 * Math.PI
        const x = 250 + radius * Math.cos(angle)
        const y = 100 + radius * Math.sin(angle)

        newNodes.push({
          id: `skill-${i}`,
          data: { label: skill },
          position: { x: x - 75, y: y - 25 },
          style: { background: 'rgba(139, 110, 255, 0.1)', color: '#8b6eff', border: '1px solid #8b6eff', borderRadius: 6, padding: 8, width: 150, fontSize: 11 }
        })

        newEdges.push({
          id: `e-agent-skill-${i}`,
          source: 'agent-root',
          target: `skill-${i}`,
          animated: true,
          style: { stroke: '#8b6eff', opacity: 0.5 }
        })
      })

      setNodes(newNodes)
      setEdges(newEdges)
    } else if (type === 'rule') {
        const newNodes: Node[] = [
            {
                id: 'rule-root',
                data: { label: data.title || 'Rule' },
                position: { x: 250, y: 50 },
                style: { background: '#1a1a2f', color: 'white', border: '2px solid #f87171', borderRadius: 12, padding: 16, width: 200, fontWeight: 'bold', textAlign: 'center' }
            },
            {
                id: 'context',
                data: { label: 'Context' },
                position: { x: 50, y: 150 },
                style: { background: 'rgba(255,255,255,0.05)', color: '#94a3b8', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8, padding: 12, width: 180, fontSize: 11 }
            }
        ]
        const newEdges: Edge[] = [
            { id: 'e-root-context', source: 'rule-root', target: 'context', animated: true, style: { stroke: '#f87171' } }
        ]

        if (data.requirements?.length > 0) {
            newNodes.push({
                id: 'requirements',
                data: { label: 'Requirements' },
                position: { x: 250, y: 250 },
                style: { background: 'rgba(248, 113, 113, 0.1)', color: '#f87171', border: '1px solid #f87171', borderRadius: 8, padding: 12, width: 200, fontSize: 11 }
            })
            newEdges.push({ id: 'e-root-reqs', source: 'rule-root', target: 'requirements', animated: true, style: { stroke: '#f87171' } })
        }

        if (data.process?.length > 0) {
            newNodes.push({
                id: 'process',
                data: { label: 'Process Protocol' },
                position: { x: 450, y: 150 },
                style: { background: 'rgba(56, 189, 248, 0.1)', color: '#38bdf8', border: '1px solid #38bdf8', borderRadius: 8, padding: 12, width: 180, fontSize: 11 }
            })
            newEdges.push({ id: 'e-root-process', source: 'rule-root', target: 'process', animated: true, style: { stroke: '#38bdf8' } })
        }

        setNodes(newNodes)
        setEdges(newEdges)
    } else if (type === 'skill') {
        // Simple representation for skill
        setNodes([{
            id: 'skill-root',
            data: { label: data.name || 'Skill' },
            position: { x: 250, y: 150 },
            style: { background: '#1a1a2f', color: 'white', border: '2px solid #8b6eff', borderRadius: 12, padding: 20, width: 200, textAlign: 'center' }
        }])
        setEdges([])
    }
  }

  // Bidirectional Synchronization
  const stripUndefined = (obj: any): any => {
    if (Array.isArray(obj)) {
      return obj.map(v => v === undefined ? null : stripUndefined(v));
    } else if (obj !== null && typeof obj === 'object') {
      return Object.fromEntries(
        Object.entries(obj)
          .filter(([_, v]) => v !== undefined)
          .map(([k, v]) => [k, stripUndefined(v)])
      );
    }
    return obj;
  }

  const handleFormChange = ({ formData }: any) => {
    try {
      const sanitizedData = stripUndefined(formData);
      const newParsed = { ...parsed, data: sanitizedData }
      setParsed(newParsed)

      const newContent = matter.stringify(newParsed.content || '', sanitizedData)
      setRawContent(newContent)

      // Sync graph
      const type = path.includes('agents') ? 'agent' : path.includes('workflows') ? 'workflow' : path.includes('rules') ? 'rule' : 'skill'
      initGraph(sanitizedData, type)
    } catch (err) {
      console.error("Failed to stringify YAML content:", err)
    }
  }

  const handleCodeChange = (value: string | undefined) => {
    if (!value) return
    setRawContent(value)
    try {
      const { data, content: body } = matter(value)
      setParsed({ data, content: body })
      const type = path.includes('agents') ? 'agent' : path.includes('workflows') ? 'workflow' : path.includes('rules') ? 'rule' : 'skill'
      initGraph(data, type)
    } catch (e) {
      // Validating YAML might fail while typing
    }
  }

  const onConnect: OnConnect = useCallback((params) => {
    setEdges((eds) => addEdge({ ...params, animated: true, style: { stroke: '#8b6eff' } }, eds))
  }, [setEdges])

  return (
    <div className="tri-pane-editor" style={{
      display: 'grid',
      gridTemplateColumns: 'minmax(350px, 1fr) minmax(400px, 1.5fr) minmax(400px, 1fr)',
      height: '100%',
      gap: 1,
      background: 'rgba(255,255,255,0.1)',
      overflow: 'hidden'
    }}>
      {/* Pane 1: Form Editor */}
      <div className="pane pane-form" style={{ background: '#0c0c14', padding: 20, overflowY: 'auto' }}>
        <h3 style={{ fontSize: 12, textTransform: 'uppercase', color: '#7878a0', marginBottom: 20 }}>Configuration</h3>
        {schema ? (
          <Form
            schema={schema}
            validator={validator}
            formData={parsed.data}
            onChange={handleFormChange}
            autoComplete="off"
          >
            <div style={{ display: 'none' }} /> {/* Hide default submit button */}
          </Form>
        ) : (
          <div style={{ color: '#7878a0', fontStyle: 'italic' }}>Loading schema...</div>
        )}
      </div>

      {/* Pane 2: Visual Graph */}
      <div className="pane pane-graph" style={{ background: '#050508', position: 'relative' }}>
        <h3 style={{ position: 'absolute', top: 12, left: 16, zIndex: 10, fontSize: 12, textTransform: 'uppercase', color: '#7878a0' }}>Visual Architecture</h3>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          connectionMode={ConnectionMode.Loose}
          fitView
          style={{ background: 'transparent' }}
        >
          <Background color="rgba(255,255,255,0.05)" gap={20} />
          <Controls />
        </ReactFlow>
      </div>

      {/* Pane 3: Code Editor */}
      <div className="pane pane-code" style={{ background: '#050508', display: 'flex', flexDirection: 'column' }}>
        <div style={{ padding: '8px 16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: '#0c0c14', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
          <h3 style={{ fontSize: 12, textTransform: 'uppercase', color: '#7878a0' }}>Source (YAML/Markdown)</h3>
          <button
            className="btn btn-primary btn-sm"
            onClick={() => onSave?.(rawContent)}
            style={{ padding: '2px 8px', fontSize: 11 }}
          >
            Save Changes
          </button>
        </div>
        <div style={{ flex: 1 }}>
          <Editor
            height="100%"
            defaultLanguage="markdown"
            theme="vs-dark"
            value={rawContent}
            onChange={handleCodeChange}
            options={{
              fontSize: 13,
              fontFamily: 'JetBrains Mono, Fira Code, monospace',
              minimap: { enabled: false },
              wordWrap: 'on',
              padding: { top: 16 }
            }}
          />
        </div>
      </div>

      <style jsx global>{`
        .pane-form .form-group {
          margin-bottom: 20px;
        }
        .pane-form label {
          display: block;
          font-size: 11px;
          color: #7878a0;
          margin-bottom: 6px;
          font-weight: 600;
          text-transform: uppercase;
        }
        .pane-form input, .pane-form select, .pane-form textarea {
          width: 100%;
          background: rgba(255,255,255,0.03);
          border: 1px solid rgba(255,255,255,0.1);
          border-radius: 4px;
          color: white;
          padding: 8px 10px;
          font-size: 13px;
        }
        .pane-form select option {
          background: #141424;
          color: white;
        }
        .pane-form fieldset {
          border: none;
          padding: 0;
          margin: 0;
        }
      `}</style>
    </div>
  )
}
