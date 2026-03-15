'use client'
import ArtifactPage from '@/lib/components/ArtifactPage'
import { api } from '@/lib/api'

export default function KnowledgePage() {
  return (
    <ArtifactPage
      title="Knowledge Assets"
      fetchList={api.knowledgeFiles}
      artifactType="Knowledge File"
      searchPlaceholder="Search knowledge patterns..."
    />
  )
}
