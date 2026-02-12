---
description: Comprehensive Next.js 16 App Router patterns, Server vs Client Components
  decision tree, route handlers, Server Actions, middleware, streaming with Suspense,
  parallel routes, intercepting routes, and advanced routing patterns.
name: nextjs-development
type: skill
---

# Nextjs Development

Comprehensive Next.js 16 App Router patterns, Server vs Client Components decision tree, route handlers, Server Actions, middleware, streaming with Suspense, parallel routes, intercepting routes, and advanced routing patterns.

## 
# Next.js Development Skill

## 
# Next.js Development Skill

## Overview
This skill provides comprehensive guidance for building production-ready Next.js 16 applications using the App Router. It covers Server Components, Client Components, routing patterns, data fetching, Server Actions, middleware, and advanced features like parallel routes and intercepting routes.

## Process
1. **Scaffold App Router structure**: Create app directory with route groups, layouts, and page components
2. **Choose Server vs Client Components**: Apply decision tree to determine component type based on requirements
3. **Implement data fetching patterns**: Use Server Components for data fetching with proper caching strategies
4. **Add Server Actions**: Create Server Actions for form submissions and mutations
5. **Configure middleware**: Set up middleware for authentication, redirects, and request modification
6. **Optimize with streaming**: Implement Suspense boundaries and streaming for better perceived performance

## Server vs Client Components Decision Tree
### Use Server Components When:
- Fetching data from databases or APIs
- Accessing backend resources (databases, file systems)
- Keeping sensitive information (API keys, tokens) on the server
- Reducing client-side JavaScript bundle size
- Improving initial page load performance

### Use Client Components When:
- Adding interactivity (onClick, onChange, etc.)
- Using browser-only APIs (localStorage, window, etc.)
- Using React hooks (useState, useEffect, etc.)
- Using third-party libraries that require client-side JavaScript
- Managing component state

### Example: Server Component

```tsx
// app/products/page.tsx
import { prisma } from '@/lib/prisma'

export default async function ProductsPage() {
  const products = await prisma.product.findMany({
    where: { published: true },
    orderBy: { createdAt: 'desc' },
  })

  return (
    <div>
      <h1>Products</h1>
      <ul>
        {products.map((product) => (
          <li key={product.id}>{product.name}</li>
        ))}
      </ul>
    </div>
  )
}
```

### Example: Client Component

```tsx
'use client'

import { useState } from 'react'

export function ProductSearch() {
  const [query, setQuery] = useState('')

  return (
    <div>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search products..."
      />
    </div>
  )
}
```

```tsx
// app/products/page.tsx
import { prisma } from '@/lib/prisma'

export default async function ProductsPage() {
  const products = await prisma.product.findMany({
    where: { published: true },
    orderBy: { createdAt: 'desc' },
  })

  return (
    <div>
      <h1>Products</h1>
      <ul>
        {products.map((product) => (
          <li key={product.id}>{product.name}</li>
        ))}
      </ul>
    </div>
  )
}
```

```tsx
'use client'

import { useState } from 'react'

export function ProductSearch() {
  const [query, setQuery] = useState('')

  return (
    <div>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search products..."
      />
    </div>
  )
}
```

## Route Handlers
Route handlers allow you to create custom request handlers for specific routes using the Web Request and Response APIs.

### Basic Route Handler

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET(request: NextRequest) {
  const users = await prisma.user.findMany()
  return NextResponse.json(users)
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  const user = await prisma.user.create({
    data: body,
  })
  return NextResponse.json(user, { status: 201 })
}
```

### Dynamic Route Handlers

```typescript
// app/api/users/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const user = await prisma.user.findUnique({
    where: { id: params.id },
  })

  if (!user) {
    return NextResponse.json({ error: 'User not found' }, { status: 404 })
  }

  return NextResponse.json(user)
}
```

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET(request: NextRequest) {
  const users = await prisma.user.findMany()
  return NextResponse.json(users)
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  const user = await prisma.user.create({
    data: body,
  })
  return NextResponse.json(user, { status: 201 })
}
```

```typescript
// app/api/users/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const user = await prisma.user.findUnique({
    where: { id: params.id },
  })

  if (!user) {
    return NextResponse.json({ error: 'User not found' }, { status: 404 })
  }

  return NextResponse.json(user)
}
```

## Server Actions
Server Actions are async functions that run on the server. They can be called from Server Components, Client Components, or other Server Actions.

### Basic Server Action

```typescript
// app/actions/user.ts
'use server'

import { prisma } from '@/lib/prisma'
import { revalidatePath } from 'next/cache'

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string
  const email = formData.get('email') as string

  const user = await prisma.user.create({
    data: { name, email },
  })

  revalidatePath('/users')
  return user
}
```

### Using Server Actions in Forms

```tsx
// app/users/create/page.tsx
import { createUser } from '@/app/actions/user'

export default function CreateUserPage() {
  return (
    <form action={createUser}>
      <input name="name" type="text" required />
      <input name="email" type="email" required />
      <button type="submit">Create User</button>
    </form>
  )
}
```

### Server Actions with useTransition

```tsx
'use client'

import { useTransition } from 'react'
import { createUser } from '@/app/actions/user'

export function CreateUserForm() {
  const [isPending, startTransition] = useTransition()

  async function handleSubmit(formData: FormData) {
    startTransition(async () => {
      await createUser(formData)
    })
  }

  return (
    <form action={handleSubmit}>
      <input name="name" type="text" required />
      <input name="email" type="email" required />
      <button type="submit" disabled={isPending}>
        {isPending ? 'Creating...' : 'Create User'}
      </button>
    </form>
  )
}
```

```typescript
// app/actions/user.ts
'use server'

import { prisma } from '@/lib/prisma'
import { revalidatePath } from 'next/cache'

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string
  const email = formData.get('email') as string

  const user = await prisma.user.create({
    data: { name, email },
  })

  revalidatePath('/users')
  return user
}
```

```tsx
// app/users/create/page.tsx
import { createUser } from '@/app/actions/user'

export default function CreateUserPage() {
  return (
    <form action={createUser}>
      <input name="name" type="text" required />
      <input name="email" type="email" required />
      <button type="submit">Create User</button>
    </form>
  )
}
```

```tsx
'use client'

import { useTransition } from 'react'
import { createUser } from '@/app/actions/user'

export function CreateUserForm() {
  const [isPending, startTransition] = useTransition()

  async function handleSubmit(formData: FormData) {
    startTransition(async () => {
      await createUser(formData)
    })
  }

  return (
    <form action={handleSubmit}>
      <input name="name" type="text" required />
      <input name="email" type="email" required />
      <button type="submit" disabled={isPending}>
        {isPending ? 'Creating...' : 'Create User'}
      </button>
    </form>
  )
}
```

## Middleware
Middleware runs before a request is completed and can modify the response by rewriting, redirecting, modifying headers, or setting cookies.

### Authentication Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token')

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*'],
}
```

### Advanced Middleware with Headers

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const response = NextResponse.next()

  // Add custom header
  response.headers.set('x-custom-header', 'value')

  // Set cookie
  response.cookies.set('last-visited', new Date().toISOString())

  return response
}
```

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token')

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*'],
}
```

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const response = NextResponse.next()

  // Add custom header
  response.headers.set('x-custom-header', 'value')

  // Set cookie
  response.cookies.set('last-visited', new Date().toISOString())

  return response
}
```

## Streaming with Suspense
Streaming allows you to progressively render UI as data becomes available.

### Basic Streaming

```tsx
// app/products/page.tsx
import { Suspense } from 'react'
import { ProductList } from '@/components/ProductList'
import { ProductSkeleton } from '@/components/ProductSkeleton'

export default function ProductsPage() {
  return (
    <div>
      <h1>Products</h1>
      <Suspense fallback={<ProductSkeleton />}>
        <ProductList />
      </Suspense>
    </div>
  )
}
```

### Multiple Suspense Boundaries

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react'
import { UserProfile } from '@/components/UserProfile'
import { RecentOrders } from '@/components/RecentOrders'
import { Stats } from '@/components/Stats'

export default function DashboardPage() {
  return (
    <div>
      <Suspense fallback={<div>Loading profile...</div>}>
        <UserProfile />
      </Suspense>
      <Suspense fallback={<div>Loading orders...</div>}>
        <RecentOrders />
      </Suspense>
      <Suspense fallback={<div>Loading stats...</div>}>
        <Stats />
      </Suspense>
    </div>
  )
}
```

```tsx
// app/products/page.tsx
import { Suspense } from 'react'
import { ProductList } from '@/components/ProductList'
import { ProductSkeleton } from '@/components/ProductSkeleton'

export default function ProductsPage() {
  return (
    <div>
      <h1>Products</h1>
      <Suspense fallback={<ProductSkeleton />}>
        <ProductList />
      </Suspense>
    </div>
  )
}
```

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react'
import { UserProfile } from '@/components/UserProfile'
import { RecentOrders } from '@/components/RecentOrders'
import { Stats } from '@/components/Stats'

export default function DashboardPage() {
  return (
    <div>
      <Suspense fallback={<div>Loading profile...</div>}>
        <UserProfile />
      </Suspense>
      <Suspense fallback={<div>Loading orders...</div>}>
        <RecentOrders />
      </Suspense>
      <Suspense fallback={<div>Loading stats...</div>}>
        <Stats />
      </Suspense>
    </div>
  )
}
```

## Parallel Routes
Parallel routes allow you to simultaneously render multiple pages in the same layout that can be navigated independently.

### Layout with Slots

```tsx
// app/dashboard/@analytics/page.tsx
export default function AnalyticsPage() {
  return <div>Analytics Content</div>
}

// app/dashboard/@team/page.tsx
export default function TeamPage() {
  return <div>Team Content</div>
}

// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
  analytics,
  team,
}: {
  children: React.ReactNode
  analytics: React.ReactNode
  team: React.ReactNode
}) {
  return (
    <div>
      {children}
      <div className="grid grid-cols-2">
        <div>{analytics}</div>
        <div>{team}</div>
      </div>
    </div>
  )
}
```

```tsx
// app/dashboard/@analytics/page.tsx
export default function AnalyticsPage() {
  return <div>Analytics Content</div>
}

// app/dashboard/@team/page.tsx
export default function TeamPage() {
  return <div>Team Content</div>
}

// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
  analytics,
  team,
}: {
  children: React.ReactNode
  analytics: React.ReactNode
  team: React.ReactNode
}) {
  return (
    <div>
      {children}
      <div className="grid grid-cols-2">
        <div>{analytics}</div>
        <div>{team}</div>
      </div>
    </div>
  )
}
```

## Intercepting Routes
Intercepting routes allow you to load a route while keeping the context of the current page in the background.

### Modal with Intercepting Route

```tsx
// app/@modal/(.)photo/[id]/page.tsx
import { Modal } from '@/components/Modal'
import { Photo } from '@/components/Photo'

export default function PhotoModal({
  params,
}: {
  params: { id: string }
}) {
  return (
    <Modal>
      <Photo id={params.id} />
    </Modal>
  )
}

// app/photo/[id]/page.tsx
import { Photo } from '@/components/Photo'

export default function PhotoPage({ params }: { params: { id: string } }) {
  return <Photo id={params.id} />
}
```

```tsx
// app/@modal/(.)photo/[id]/page.tsx
import { Modal } from '@/components/Modal'
import { Photo } from '@/components/Photo'

export default function PhotoModal({
  params,
}: {
  params: { id: string }
}) {
  return (
    <Modal>
      <Photo id={params.id} />
    </Modal>
  )
}

// app/photo/[id]/page.tsx
import { Photo } from '@/components/Photo'

export default function PhotoPage({ params }: { params: { id: string } }) {
  return <Photo id={params.id} />
}
```

## Route Groups
Route groups organize routes without affecting the URL structure.

### Example Structure

```
app/
  (marketing)/
    about/
      page.tsx
    contact/
      page.tsx
  (shop)/
    products/
      page.tsx
    cart/
      page.tsx
```

### Layouts for Route Groups

```tsx
// app/(marketing)/layout.tsx
export default function MarketingLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="marketing-layout">
      <header>Marketing Header</header>
      {children}
      <footer>Marketing Footer</footer>
    </div>
  )
}
```

```
app/
  (marketing)/
    about/
      page.tsx
    contact/
      page.tsx
  (shop)/
    products/
      page.tsx
    cart/
      page.tsx
```

```tsx
// app/(marketing)/layout.tsx
export default function MarketingLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="marketing-layout">
      <header>Marketing Header</header>
      {children}
      <footer>Marketing Footer</footer>
    </div>
  )
}
```

## Data Fetching Patterns
### Server Component Data Fetching

```tsx
// app/products/page.tsx
import { prisma } from '@/lib/prisma'

export default async function ProductsPage() {
  const products = await prisma.product.findMany()

  return (
    <div>
      {products.map((product) => (
        <div key={product.id}>{product.name}</div>
      ))}
    </div>
  )
}
```

### Revalidation Strategies

```typescript
// app/products/page.tsx
import { prisma } from '@/lib/prisma'

export const revalidate = 3600 // Revalidate every hour

export default async function ProductsPage() {
  const products = await prisma.product.findMany()
  return <div>...</div>
}
```

### On-Demand Revalidation

```typescript
// app/api/revalidate/route.ts
import { revalidatePath } from 'next/cache'
import { NextRequest } from 'next/server'

export async function POST(request: NextRequest) {
  const path = request.nextUrl.searchParams.get('path')
  if (path) {
    revalidatePath(path)
    return Response.json({ revalidated: true })
  }
  return Response.json({ revalidated: false })
}
```

```tsx
// app/products/page.tsx
import { prisma } from '@/lib/prisma'

export default async function ProductsPage() {
  const products = await prisma.product.findMany()

  return (
    <div>
      {products.map((product) => (
        <div key={product.id}>{product.name}</div>
      ))}
    </div>
  )
}
```

```typescript
// app/products/page.tsx
import { prisma } from '@/lib/prisma'

export const revalidate = 3600 // Revalidate every hour

export default async function ProductsPage() {
  const products = await prisma.product.findMany()
  return <div>...</div>
}
```

```typescript
// app/api/revalidate/route.ts
import { revalidatePath } from 'next/cache'
import { NextRequest } from 'next/server'

export async function POST(request: NextRequest) {
  const path = request.nextUrl.searchParams.get('path')
  if (path) {
    revalidatePath(path)
    return Response.json({ revalidated: true })
  }
  return Response.json({ revalidated: false })
}
```

## Edge Runtime
Use Edge Runtime for routes that need low latency and can run at the edge.

```typescript
// app/api/hello/route.ts
export const runtime = 'edge'

export async function GET() {
  return Response.json({ message: 'Hello from Edge!' })
}
```

```typescript
// app/api/hello/route.ts
export const runtime = 'edge'

export async function GET() {
  return Response.json({ message: 'Hello from Edge!' })
}
```

## Best Practices
1. **Default to Server Components**: Use Server Components unless you need client-side features
2. **Streaming**: Use Suspense boundaries for better perceived performance
3. **Caching**: Leverage Next.js caching strategies (ISR, revalidation)
4. **Type Safety**: Use TypeScript for all routes and components
5. **Error Handling**: Implement error boundaries and proper error pages
6. **Performance**: Optimize images, fonts, and bundle size
7. **Security**: Validate all inputs, sanitize outputs, use Server Actions for mutations

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Knowledge: nextjs-patterns.json, nextjs-advanced.json
