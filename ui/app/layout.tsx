'use client'
import './globals.css'
import { useEffect, useState } from 'react'
import { api } from '@/lib/api'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const [wsStatus, setWsStatus] = useState<'connected' | 'reconnecting' | 'error'>('reconnecting')

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
        <div className="app-shell">
          {/* Top Bar */}
          <header className="topbar">
            <div className="topbar-logo">
              <span>◆</span>
              <span><span className="accent">Antigravity</span> IDX</span>
            </div>
            <div className="topbar-actions">
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
              <li><a href="/">⌂ Dashboard</a></li>
            </ul>
            <div className="sidebar-section">Build</div>
            <ul className="sidebar-nav">
              <li><a href="/workflows">⚙ Workflows</a></li>
              <li><a href="/agent-workflows">⚡ Agents (Gen)</a></li>
              <li><a href="/agents">🤖 Specialist Agents</a></li>
              <li><a href="/skills">🧩 Skills</a></li>
            </ul>
            <div className="sidebar-section">Factory Assets</div>
            <ul className="sidebar-nav">
              <li><a href="/blueprints">⚡ Blueprints</a></li>
              <li><a href="/rules">📜 Rules</a></li>
              <li><a href="/knowledge">🧠 Knowledge</a></li>
              <li><a href="/patterns">🧩 Patterns</a></li>
            </ul>
            <div className="sidebar-section">Tools</div>
            <ul className="sidebar-nav">
              <li><a href="/scripts">🐍 Python Scripts</a></li>
              <li><a href="/tools">🔧 Generic Tools</a></li>
              <li><a href="/mcp">◎ MCP Servers</a></li>
            </ul>
            <div className="sidebar-section">Settings</div>
            <ul className="sidebar-nav">
              <li><a href="/agent-config">⚙ .agent Config</a></li>
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
