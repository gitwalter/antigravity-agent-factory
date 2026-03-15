'use client'
import ArtifactPage from '@/lib/components/ArtifactPage'
import { api } from '@/lib/api'

export default function BlueprintsPage() {
  return (
    <ArtifactPage
      title="Project Blueprints"
      fetchList={api.blueprints}
      artifactType="Blueprint"
      searchPlaceholder="Search blueprints..."
    />
  )
}
