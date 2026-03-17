'use client'
import './globals.css'
import { useEffect, useState } from 'react'
import { usePathname } from 'next/navigation'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()
  const [wsStatus, setWsStatus] = useState<'connected' | 'reconnecting' | 'error'>('reconnecting')

  // SDLC Phase mapping for context-awareness
  const getActivePhase = () => {
    if (pathname === '/') return 'Ideation'
    if (['/blueprints', '/rules', '/knowledge', '/patterns'].some(p => pathname.startsWith(p))) return 'Requirements'
    if (['/workflows', '/mcp'].some(p => pathname.startsWith(p))) return 'Architecture'
    if (['/agent-workflows', '/agents', '/skills'].some(p => pathname.startsWith(p))) return 'Build'
    if (['/scripts', '/tools'].some(p => pathname.startsWith(p))) return 'Test/Eval'
    return 'Ideation'
  }

  const activePhase = getActivePhase()

  useEffect(() => {
    let eventsWs: WebSocket | null = null
    let retryCount = 0

    const connect = () => {
      const eventsUrl = `ws://${window.location.hostname}:8000/ws/events`
      eventsWs = new WebSocket(eventsUrl)

      eventsWs.onopen = () => {
        setWsStatus('connected')
        retryCount = 0
      }

      eventsWs.onmessage = (e) => {
        const data = JSON.parse(e.data)
        if (data.type === 'file_change') {
          console.log('Artifact changed, hot reloading data...', data.file)
          if (window.location.pathname === '/' || window.location.pathname.includes('workflows')) {
             window.location.reload()
          }
        }
      }

      eventsWs.onclose = () => {
        setWsStatus('reconnecting')
        if (retryCount < 5) {
          retryCount++
          setTimeout(connect, 3000)
        } else {
          setWsStatus('error')
        }
      }
    }

    connect()
    return () => {
      eventsWs?.close()
    }
  }, [])

  return (
    <html lang="en">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>
        {/* Background Visuals */}
        <div className="bg-mesh">
          <div className="bg-blob bg-blob-1"></div>
          <div className="bg-blob bg-blob-2"></div>
          <div className="bg-blob bg-blob-3"></div>
        </div>

        <div className="app-shell">
          {/* Top Bar */}
          <header className="topbar">
            <div className="topbar-logo">
              <span className="glow-text">◆</span>
              <span><span className="accent">Antigravity</span> IDX</span>
            </div>

            <div className="topbar-actions">
              {/* Context Indicator */}
              <div className={`tag ${activePhase ? 'tag-primary' : ''}`} style={{ background: 'rgba(139, 110, 255, 0.1)', borderColor: 'rgba(139, 110, 255, 0.3)' }}>
                <span style={{ fontSize: '10px', opacity: 0.7, marginRight: '6px' }}>PHASE:</span>
                <span style={{ fontWeight: 700, letterSpacing: '0.05em' }}>{activePhase.toUpperCase()}</span>
              </div>

              <a
                href="https://smith.langchain.com"
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-secondary btn-sm"
              >
                ↗ LangSmith
              </a>
              <span className={`tag ${wsStatus === 'connected' ? 'tag-success' : 'tag-warning'}`}>
                {wsStatus === 'connected' ? '● Live' : '○ Syncing...'}
              </span>
            </div>
          </header>

          {/* Sidebar */}
          <nav className="sidebar">
            <div className="sidebar-section">Overview</div>
            <ul className="sidebar-nav">
              <li><a href="/" className={pathname === '/' ? 'active' : ''}>⌂ Dashboard</a></li>
            </ul>

            <div className="sidebar-section">Build & Architecture</div>
            <ul className="sidebar-nav">
              <li><a href="/workflows" className={pathname.startsWith('/workflows') ? 'active' : ''}>⚙ Workflows</a></li>
              <li><a href="/agent-workflows" className={pathname.startsWith('/agent-workflows') ? 'active' : ''}>⚡ Agents (Gen)</a></li>
              <li><a href="/agents" className={pathname.startsWith('/agents') ? 'active' : ''}>🤖 Specialist Agents</a></li>
              <li><a href="/skills" className={pathname.startsWith('/skills') ? 'active' : ''}>🧩 Skills</a></li>
            </ul>

            <div className="sidebar-section">Factory Assets</div>
            <ul className="sidebar-nav">
              <li><a href="/blueprints" className={pathname.startsWith('/blueprints') ? 'active' : ''}>⚡ Blueprints</a></li>
              <li><a href="/rules" className={pathname.startsWith('/rules') ? 'active' : ''}>📜 Rules</a></li>
              <li><a href="/knowledge" className={pathname.startsWith('/knowledge') ? 'active' : ''}>🧠 Knowledge</a></li>
              <li><a href="/patterns" className={pathname.startsWith('/patterns') ? 'active' : ''}>🧩 Patterns</a></li>
            </ul>

            <div className="sidebar-section">Quality & Ops</div>
            <ul className="sidebar-nav">
              <li><a href="/scripts" className={pathname.startsWith('/scripts') ? 'active' : ''}>🐍 Python Scripts</a></li>
              <li><a href="/tools" className={pathname.startsWith('/tools') ? 'active' : ''}>🔧 Generic Tools</a></li>
              <li><a href="/mcp" className={pathname.startsWith('/mcp') ? 'active' : ''}>◎ MCP Servers</a></li>
            </ul>

            <div className="sidebar-section">Configuration</div>
            <ul className="sidebar-nav">
              <li><a href="/agent-config" className={pathname.startsWith('/agent-config') ? 'active' : ''}>⚙ .agent Config</a></li>
            </ul>
          </nav>

          {/* Main Content */}
          <main className="main-content">
            {children}
          </main>
        </div>
      </body>
    </html>
  )
}
