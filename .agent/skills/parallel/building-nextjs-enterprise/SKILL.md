---
agents:
- none
category: parallel
description: Tactical Blueprint for production-grade Next.js 15+ applications. Focuses
  on procedural execution, tool-calling sequences, and idiomatic excellence.
knowledge:
- none
name: building-nextjs-enterprise
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Capability Manifest: Next.js Enterprise

This blueprint provides the **procedural truth** for engineering, testing, and deploying high-fidelity TypeScript web applications in the Antigravity Agent Factory.

## Operational Environment

- **Runtime**: Node.js 20+ (LTS).
- **Core Stack**: Next.js 15 (App Router), React 19, TypeScript 5+.
- **Observability**: Vercel Analytics/Speed Insights, OpenTelemetry.

## Process

Follow these procedures to implement the capability:

### Procedure 1: Scaffolding a Route Domain
Next.js applications in this factory follow a **Segment-Based Architecture**.
Execute these steps to add a new feature:
1.  **Create Segment**: `mkdir -p app/(features)/[feature-name]`.
2.  **Define Layout**: Create `layout.tsx` with shared UI and `Suspense` boundaries for slots.
3.  **Implement Page**: Create `page.tsx` as a **React Server Component (RSC)**.
4.  **Axiom Check**: Verify that `Loading.tsx` and `Error.tsx` are present in the segment.

### Procedure 2: Implementing a Data-Driven Feature (RSC + Actions)
1.  **Data Fetching**: Fetch data directly in the `page.tsx` (RSC) using `await` and appropriate `cache` or `revalidate` tags.
2.  **Stateful Interactivity**: If the feature requires state (e.g., a form), create a Client Component (`'use client'`) and pass data as props.
3.  **Mutation**: Use **Server Actions** (`'use server'`) for all POST/PUT/DELETE operations.
    - *Axiom Check*: Always wrap actions in `useActionState` (React 19) for pending and error truth.

### Procedure 3: Production Optimization & Hydration
1.  **Static/Dynamic Gate**: Run `next build` and audit the `.next/required-server-files.json`. Verify which routes are static (○) vs dynamic (λ).
2.  **Hydration Audit**: Scan for `useEffect` hooks used for initial rendering. If found, refactor to `use` or Server Components.
3.  **Image Beauty**: All images must use `next/image` with `placeholder="blur"` and specific `sizes`.

## Process (Fail-State & Recovery)

| Symptom | Probable Cause | Recovery Operation |
| :--- | :--- | :--- |
| **Hydration Error** | Client/Server HTML mismatch (e.g., `new Date()` or `window`). | Wrap the offending component in a `dynamic(() => ..., { ssr: false })` or use `useEffect` for the browser-only value. |
| **Infinite Re-render** | Dependency array violation in Client Hook. | Audit `useMemo` and `useCallback` dependencies. Move complex objects out of the component body or use `use` (React 19). |
| **Action Timeout** | Heavy server-side processing without streaming. | Subdivide the task; use `Suspense` for the UI and fire the Action; implement an "Optimistic UI" using `useOptimistic`. |

## Idiomatic Code Patterns (The Gold Standard)

### The "Truthful" Server Action
```typescript
'use server'

import { revalidatePath } from 'next/cache'
import { z } from 'zod'

const Schema = z.object({ name: z.string().min(3) })

export async function createItem(prevState: any, formData: FormData) {
  const validated = Schema.safeParse({ name: formData.get('name') })
  if (!validated.success) return { error: "Invalid name truth" }

  await db.item.create({ data: validated.data })
  revalidatePath('/items')
  return { success: true }
}
```

### The "Beautiful" Parallel Route Layout
```tsx
export default function Layout({ children, modal }: { children: ReactNode, modal: ReactNode }) {
  return (
    <div className="layout-grid">
      {children}
      <Suspense fallback={<ModalSkeleton />}>
        {modal}
      </Suspense>
    </div>
  )
}
```

## Prerequisites

| Action | Command |
| :--- | :--- |
| Build & TypeCheck | `next build` |
| Local Dev | `next dev --turbo` |
| Component Audit | `npm run lint` |
| Performance Audit | `npx lighthouse http://localhost:3000` |

## When to Use
Use this blueprint whenever building, refactoring, or debugging a Next.js application. It is the authoritative source for "How we build" vs "What Next.js is."


## Best Practices

- Follow the system axioms (A1-A5)
- Ensure all changes are verifiable
- Document complex logic for future maintenance
