---
description: React 19 component patterns, hooks, state management, and composition
name: react-patterns
type: skill
---
# React Patterns

React 19 component patterns, hooks, state management, and composition

Build modern React 19 applications using Server Components, hooks, state management, form handling, and component composition patterns.

## Process

1. **Scaffold** – Run `python scripts/scaffold.py --name <app> --output-dir .` or create structure manually. See REFERENCE.md § Project Structure.
2. **Server Components** – Use Server Components by default; async fetch in components. See REFERENCE.md § Server Components and use() Hook.
3. **Server Actions** – Form submissions with `'use server'` and `useTransition`. See REFERENCE.md § Server Actions.
4. **Compound Components** – Context + child components for flexible APIs. See REFERENCE.md § Compound Components.
5. **Custom Hooks** – Extract reusable logic (useDebounce, useLocalStorage). See REFERENCE.md § Custom Hooks.
6. **State Management** – Zustand for global state with devtools and persist. See REFERENCE.md § State Management with Zustand.
7. **Form Handling** – React Hook Form + Zod validation. See REFERENCE.md § Form Handling.
8. **Component Composition** – Card, CardHeader, CardBody patterns. See REFERENCE.md § Component Composition.

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
- **REFERENCE.md** – Code examples (Server Components, Server Actions, Compound Components, Custom Hooks, Zustand, Form Handling, Component Composition)
- **scripts/scaffold.py** – Generate project structure (`--name`, `--output-dir`)
- **examples/counter/** – Simple client component with useState

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
