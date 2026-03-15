'use client'
import ArtifactPage from '@/lib/components/ArtifactPage'
import { api } from '@/lib/api'

export default function PatternsPage() {
  return (
    <ArtifactPage
      title="Interaction Patterns"
      fetchList={api.patterns}
      artifactType="Pattern"
      searchPlaceholder="Search interaction patterns..."
    />
  )
}
