# Next.js Fullstack Development

> **Stack:** Next.js 14+ | **Level:** Intermediate | **Duration:** 2.5 hours

## Overview

**Workshop ID:** `L10_nextjs_fullstack`

**Technology:** TypeScript with Next.js 14+ (Next.js 14+)

## Prerequisites

**Required Workshops:**
- L9_react_modern

**Required Knowledge:**
- React fundamentals and hooks
- TypeScript basics
- REST API concepts
- HTTP methods and status codes

**Required Tools:**
- Node.js 18+
- npm or yarn
- VS Code or similar IDE
- Git

## Learning Objectives

By the end of this workshop, you will be able to:

1. **Understand Next.js App Router architecture and routing** (Understand)
2. **Build Server Components and understand when to use them** (Apply)
3. **Implement API routes and Server Actions** (Apply)
4. **Apply authentication patterns in Next.js** (Apply)
5. **Optimize Next.js applications with caching and ISR** (Analyze)

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

### Concept: Next.js App Router Fundamentals

*Understanding App Router, Server Components, and Next.js architecture*

**Topics Covered:**
- App Router vs Pages Router
- Server Components vs Client Components
- File-based routing and layouts
- Data fetching: Server Components, Server Actions, API Routes
- Caching strategies: request memoization, Data Cache, Full Route Cache
- Authentication patterns: middleware, server sessions

**Key Points:**
- Server Components render on server, reducing client bundle
- Use 'use client' directive only when needed
- Server Actions provide type-safe mutations
- Layouts enable shared UI across routes
- Caching improves performance but requires understanding

### Demo: Building a Blog with Next.js

*Live coding a fullstack blog application*

**Topics Covered:**
- Setting up Next.js project with TypeScript
- Creating Server Component for blog posts
- Implementing API route for comments
- Adding Server Action for comment submission
- Implementing authentication middleware
- Adding ISR for blog posts

**Key Points:**
- Server Components can be async
- API routes use standard Request/Response
- Server Actions are type-safe and secure
- Middleware runs before request completes

### Exercise: Server Component Data Fetching

*Create Server Components that fetch and display data*

**Topics Covered:**
- Create async Server Component
- Fetch data from external API
- Handle loading and error states
- Use generateStaticParams for dynamic routes

### Exercise: Server Actions and Forms

*Build forms with Server Actions*

**Topics Covered:**
- Create Server Action
- Build form component
- Handle form validation
- Implement optimistic updates
- Add error handling

### Challenge: E-Commerce Product Page

*Build a product page with Server Components, API routes, and authentication*

**Topics Covered:**
- Create product detail page with Server Component
- Implement add to cart Server Action
- Add protected checkout route
- Implement ISR for product pages
- Add search functionality

### Reflection: Key Takeaways and Production Considerations

*Consolidate learning and discuss deployment*

**Topics Covered:**
- Server vs Client Component decision tree
- Caching strategy guidelines
- Authentication best practices
- Performance optimization
- Deployment considerations

**Key Points:**
- Default to Server Components
- Use Client Components for interactivity
- Understand caching to avoid stale data
- Server Actions simplify form handling
- Middleware is powerful for auth

## Hands-On Exercises

### Exercise: Server Component Data Fetching

Create a Server Component that fetches and displays data

**Difficulty:** Medium | **Duration:** 20 minutes

**Hints:**
- Server Components can be async functions
- Use fetch with Next.js caching options
- Call notFound() for missing resources
- generateStaticParams enables static generation

**Common Mistakes to Avoid:**
- Forgetting 'use client' is not needed for Server Components
- Not handling loading/error states
- Missing generateStaticParams for dynamic routes
- Not using Next.js fetch caching options

### Exercise: Server Actions and Forms

Build a form with Server Actions for data mutation

**Difficulty:** Medium | **Duration:** 25 minutes

**Common Mistakes to Avoid:**
- Forgetting 'use server' directive
- Not handling form validation
- Missing error handling
- Not revalidating after mutation

## Challenges

### Challenge: E-Commerce Product Page

Build a complete product page with Server Components, API routes, and authentication

**Requirements:**
- Product detail page using Server Component
- Add to cart Server Action
- Protected checkout route with middleware
- ISR for product pages
- Search functionality with API route
- User authentication flow

**Evaluation Criteria:**
- Product page renders server-side
- Add to cart works correctly
- Checkout requires authentication
- Products are statically generated with ISR
- Search returns relevant results
- Auth flow is secure

**Stretch Goals:**
- Add product reviews with Server Actions
- Implement wishlist functionality
- Add real-time inventory updates
- Create admin dashboard for products

## Resources

**Official Documentation:**
- https://nextjs.org/docs
- https://nextjs.org/docs/app
- https://nextjs.org/docs/app/api-reference/server-actions

**Tutorials:**
- https://nextjs.org/learn
- Next.js App Router Course - Vercel

**Videos:**
- Next.js 14 App Router - Vercel YouTube
- Server Components Explained - React Conf

## Self-Assessment

Ask yourself these questions:

- [ ] Can I decide when to use Server vs Client Components?
- [ ] Do I understand how to implement Server Actions?
- [ ] Can I set up authentication with middleware?
- [ ] Do I know how to configure caching strategies?

## Next Steps

**Next Workshop:** `L11_fastapi_production`

**Practice Projects:**
- Build a SaaS application with Next.js
- Create a content management system
- Implement a social media platform

**Deeper Learning:**
- Next.js middleware advanced patterns
- Edge runtime and edge functions
- Next.js deployment and optimization

## Related Knowledge Files

- `nextjs-patterns.json`
- `react-patterns.json`

---

*Part of the Antigravity Agent Factory Learning Workshop Ecosystem*

**Workshop Definition:** `.agent/patterns/workshops/L10_nextjs_fullstack.json`