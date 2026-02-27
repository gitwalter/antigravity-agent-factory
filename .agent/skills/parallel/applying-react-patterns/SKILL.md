---
agents:
- none
category: parallel
description: React 19 component patterns, hooks, state management, and composition
knowledge:
- none
name: applying-react-patterns
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# React Patterns

React 19 component patterns, hooks, state management, and composition

Build modern React 19 applications using Server Components, hooks, state management, form handling, and component composition patterns.

## Process

1. **Scaffold** – Run `python scripts/scaffold.py --name <app> --output-dir .` or create structure manually.
2. **Server Components** – Use Server Components by default; async fetch in components.
3. **Server Actions** – Form submissions with `'use server'` and `useTransition`.
4. **Compound Components** – Context + child components for flexible APIs.
5. **Custom Hooks** – Extract reusable logic (useDebounce, useLocalStorage).
6. **State Management** – Zustand for global state with devtools and persist.
7. **Form Handling** – React Hook Form + Zod validation.
8. **Component Composition** – Card, CardHeader, CardBody patterns.

## Best Practices

- Use Server Components by default, Client Components only when needed
- Extract reusable logic into custom hooks
- Use Zustand or Jotai for global state, React state for local state
- Validate forms with Zod schemas
- Implement compound components for flexible APIs
- Use React.memo() and useMemo() for performance optimization
- Prefer composition over prop drilling
- Use TypeScript for type safety
- Implement error boundaries for error handling
- Use Suspense boundaries for loading states
- Optimize bundle size with code splitting
- Use React Query for server state management

## Bundled Resources

- **QUICKSTART.md** – 5-minute React 19 setup with Server Component example
- **scripts/scaffold.py** – Generate project structure (`--name`, `--output-dir`)
- **examples/counter/** – Simple client component with useState

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
