'use client'
import ArtifactPage from '@/lib/components/ArtifactPage'
import { api } from '@/lib/api'

export default function RulesPage() {
  return (
    <ArtifactPage
      title="Governance Rules"
      fetchList={api.rules}
      artifactType="Rule"
      searchPlaceholder="Search governance rules..."
    />
  )
}
