# Modern React Patterns

> **Stack:** React 18+ | **Level:** Intermediate | **Duration:** 2.5 hours

## Overview

**Workshop ID:** `L9_react_modern`

**Technology:** TypeScript with React 18+ (React 18+)

## Prerequisites

**Required Knowledge:**
- JavaScript/TypeScript fundamentals
- Basic React concepts (components, props, JSX)
- ES6+ features (arrow functions, destructuring, modules)

**Required Tools:**
- Node.js 18+
- npm or yarn
- VS Code or similar IDE
- React DevTools browser extension

## Learning Objectives

By the end of this workshop, you will be able to:

1. **Master React Hooks: useState, useEffect, useCallback, and useMemo** (Apply)
2. **Create custom hooks for reusable logic** (Create)
3. **Apply component composition patterns effectively** (Apply)
4. **Implement Context API for state management** (Apply)
5. **Optimize React performance using memoization and code splitting** (Analyze)

## Workshop Timeline

| Phase | Duration |
|-------|----------|
| Concept | 30 min |
| Demo | 30 min |
| Exercise | 45 min |
| Challenge | 30 min |
| Reflection | 15 min |
| **Total** | **2.5 hours** |

## Workshop Phases

### Concept: Modern React Patterns Overview

*Understanding hooks, composition, and performance patterns*

**Topics Covered:**
- React Hooks: useState, useEffect, useCallback, useMemo
- Custom hooks: extracting and sharing logic
- Component composition: children, render props, compound components
- Context API: when and how to use it
- Performance optimization: React.memo, useMemo, useCallback
- Code splitting with React.lazy and Suspense

**Key Points:**
- Hooks must be called at the top level, not conditionally
- useCallback and useMemo prevent unnecessary re-renders
- Composition over inheritance for React components
- Context should be used sparingly to avoid prop drilling
- Performance optimization requires measurement first

### Demo: Building a Reusable Form Component

*Live coding a form with custom hooks and composition*

**Topics Covered:**
- Creating custom useForm hook
- Building reusable Input component
- Using Context for form state
- Implementing validation with useMemo
- Optimizing with React.memo
- Adding error handling

**Key Points:**
- Custom hooks encapsulate complex logic
- Composition makes components flexible
- Memoization prevents unnecessary calculations
- Context reduces prop drilling

### Exercise: Custom Hook: useFetch

*Create a reusable data fetching hook*

**Topics Covered:**
- Implement useFetch with useState and useEffect
- Handle loading and error states
- Add caching with useMemo
- Support refetch functionality

### Exercise: Composed Modal Component

*Build a flexible modal using composition*

**Topics Covered:**
- Create Modal compound component
- Use Context for modal state
- Implement portal for rendering
- Add keyboard and click-outside handlers

### Challenge: Performance-Optimized Dashboard

*Build a dashboard with performance optimizations*

**Topics Covered:**
- Create dashboard with multiple data sources
- Implement memoization for expensive calculations
- Use code splitting for routes
- Optimize list rendering
- Add loading states and error boundaries

### Reflection: Key Takeaways and Best Practices

*Consolidate learning and discuss production patterns*

**Topics Covered:**
- When to use each hook pattern
- Composition vs Context trade-offs
- Performance optimization guidelines
- Testing hooks and composed components
- Resources for continued learning

**Key Points:**
- Measure before optimizing
- Composition provides flexibility
- Custom hooks promote reusability
- Context is powerful but use sparingly
- Always follow rules of hooks

## Hands-On Exercises

### Exercise: Custom useFetch Hook

Create a reusable hook for data fetching with loading and error states

**Difficulty:** Medium | **Duration:** 20 minutes

**Hints:**
- Use useState for data, loading, and error states
- Create an async function inside useEffect
- Use useCallback for refetch to memoize the function
- Handle cleanup if component unmounts during fetch

**Common Mistakes to Avoid:**
- Forgetting to set loading to false in error case
- Not handling component unmount during async operation
- Missing dependency array in useEffect
- Not memoizing refetch function

### Exercise: Composed Modal Component

Build a flexible modal using composition and Context API

**Difficulty:** Medium | **Duration:** 25 minutes

**Common Mistakes to Avoid:**
- Not using portal for modal rendering
- Forgetting to clean up event listeners
- Not preventing event bubbling on backdrop click
- Missing error handling for missing context

## Challenges

### Challenge: Performance-Optimized Dashboard

Build a dashboard component with multiple data sources and performance optimizations

**Requirements:**
- Display multiple data sources (users, posts, analytics)
- Use custom hooks for each data source
- Implement React.memo for expensive components
- Use useMemo for expensive calculations
- Add code splitting with React.lazy
- Implement error boundaries
- Add loading states and skeleton screens

**Evaluation Criteria:**
- All data sources load correctly
- No unnecessary re-renders (verify with React DevTools)
- Expensive calculations are memoized
- Code splitting works correctly
- Error boundaries catch errors gracefully
- Loading states provide good UX

**Stretch Goals:**
- Add virtual scrolling for long lists
- Implement optimistic updates
- Add real-time updates with WebSocket
- Create reusable skeleton components

## Resources

**Official Documentation:**
- https://react.dev/reference/react
- https://react.dev/learn/reusing-logic-with-custom-hooks
- https://react.dev/reference/react/useContext

**Tutorials:**
- https://react.dev/learn
- https://kentcdodds.com/blog/compound-components-with-react-hooks

**Videos:**
- React Hooks Deep Dive - React Conf
- Advanced React Patterns - Frontend Masters

## Self-Assessment

Ask yourself these questions:

- [ ] Can I create custom hooks for reusable logic?
- [ ] Do I understand when to use each optimization technique?
- [ ] Can I build flexible components using composition?
- [ ] Do I know when Context API is appropriate?

## Next Steps

**Next Workshop:** `L10_nextjs_fullstack`

**Practice Projects:**
- Build a component library with Storybook
- Create a data visualization dashboard
- Implement a complex form with validation

**Deeper Learning:**
- React Server Components
- Advanced state management (Zustand, Jotai)
- React performance profiling and optimization

## Related Knowledge Files

- `react-patterns.json`

---

*Part of the Antigravity Agent Factory Learning Workshop Ecosystem*

**Workshop Definition:** `.agent/patterns/workshops/L9_react_modern.json`