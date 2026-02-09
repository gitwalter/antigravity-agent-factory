---
description: tRPC router setup with Next.js App Router, procedures (query, mutation, subscription), input validation with Zod, middleware and context, React Query integration, error handling, and type inference.
---

# Trpc Api

tRPC router setup with Next.js App Router, procedures (query, mutation, subscription), input validation with Zod, middleware and context, React Query integration, error handling, and type inference.

## 
# tRPC API Skill

## 
# tRPC API Skill

## Overview
This skill provides comprehensive guidance for building type-safe APIs with tRPC in Next.js applications. It covers router setup, procedures, validation, middleware, React Query integration, and error handling.

## Process
1. **Set up tRPC server with Next.js**: Create tRPC context, initialize tRPC instance, and create API route handler
2. **Define routers and procedures**: Create routers with query, mutation, and subscription procedures
3. **Add input validation with Zod**: Define Zod schemas for procedure inputs with validation rules
4. **Implement middleware**: Create authentication, authorization, logging, and rate limiting middleware
5. **Integrate React Query client**: Set up tRPC React provider with React Query for client-side usage
6. **Add error handling**: Implement custom error classes, error formatting, and client-side error handling

## Setup with Next.js App Router
### Install Dependencies

```bash
npm install @trpc/server @trpc/client @trpc/react-query @trpc/next @tanstack/react-query zod
```

### Create tRPC Context

```typescript
// server/trpc/context.ts
import { inferAsyncReturnType } from '@trpc/server'
import { CreateNextContextOptions } from '@trpc/server/adapters/next'
import { prisma } from '@/lib/prisma'

export async function createContext(opts: CreateNextContextOptions) {
  const { req, res } = opts

  // Get user from session/cookie
  const user = await getUserFromRequest(req)

  return {
    req,
    res,
    prisma,
    user,
  }
}

export type Context = inferAsyncReturnType<typeof createContext>
```

### Initialize tRPC

```typescript
// server/trpc/trpc.ts
import { initTRPC, TRPCError } from '@trpc/server'
import { Context } from './context'
import superjson from 'superjson'

const t = initTRPC.context<Context>().create({
  transformer: superjson,
})

export const router = t.router
export const publicProcedure = t.procedure
```

### Create Protected Procedure

```typescript
// server/trpc/trpc.ts
const isAuthenticated = t.middleware(({ ctx, next }) => {
  if (!ctx.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' })
  }
  return next({
    ctx: {
      ...ctx,
      user: ctx.user, // Type narrowing
    },
  })
})

export const protectedProcedure = t.procedure.use(isAuthenticated)
```

```bash
npm install @trpc/server @trpc/client @trpc/react-query @trpc/next @tanstack/react-query zod
```

```typescript
// server/trpc/context.ts
import { inferAsyncReturnType } from '@trpc/server'
import { CreateNextContextOptions } from '@trpc/server/adapters/next'
import { prisma } from '@/lib/prisma'

export async function createContext(opts: CreateNextContextOptions) {
  const { req, res } = opts

  // Get user from session/cookie
  const user = await getUserFromRequest(req)

  return {
    req,
    res,
    prisma,
    user,
  }
}

export type Context = inferAsyncReturnType<typeof createContext>
```

```typescript
// server/trpc/trpc.ts
import { initTRPC, TRPCError } from '@trpc/server'
import { Context } from './context'
import superjson from 'superjson'

const t = initTRPC.context<Context>().create({
  transformer: superjson,
})

export const router = t.router
export const publicProcedure = t.procedure
```

```typescript
// server/trpc/trpc.ts
const isAuthenticated = t.middleware(({ ctx, next }) => {
  if (!ctx.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' })
  }
  return next({
    ctx: {
      ...ctx,
      user: ctx.user, // Type narrowing
    },
  })
})

export const protectedProcedure = t.procedure.use(isAuthenticated)
```

## Router Setup
### Basic Router

```typescript
// server/routers/user.ts
import { z } from 'zod'
import { router, publicProcedure, protectedProcedure } from '../trpc/trpc'
import { TRPCError } from '@trpc/server'

export const userRouter = router({
  getById: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ ctx, input }) => {
      const user = await ctx.prisma.user.findUnique({
        where: { id: input.id },
      })

      if (!user) {
        throw new TRPCError({
          code: 'NOT_FOUND',
          message: 'User not found',
        })
      }

      return user
    }),

  getAll: publicProcedure.query(async ({ ctx }) => {
    return ctx.prisma.user.findMany({
      orderBy: { createdAt: 'desc' },
    })
  }),

  create: publicProcedure
    .input(
      z.object({
        email: z.string().email(),
        name: z.string().min(1),
      })
    )
    .mutation(async ({ ctx, input }) => {
      const user = await ctx.prisma.user.create({
        data: input,
      })
      return user
    }),
})
```

### App Router

```typescript
// server/routers/_app.ts
import { router } from '../trpc/trpc'
import { userRouter } from './user'
import { postRouter } from './post'

export const appRouter = router({
  user: userRouter,
  post: postRouter,
})

export type AppRouter = typeof appRouter
```

```typescript
// server/routers/user.ts
import { z } from 'zod'
import { router, publicProcedure, protectedProcedure } from '../trpc/trpc'
import { TRPCError } from '@trpc/server'

export const userRouter = router({
  getById: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ ctx, input }) => {
      const user = await ctx.prisma.user.findUnique({
        where: { id: input.id },
      })

      if (!user) {
        throw new TRPCError({
          code: 'NOT_FOUND',
          message: 'User not found',
        })
      }

      return user
    }),

  getAll: publicProcedure.query(async ({ ctx }) => {
    return ctx.prisma.user.findMany({
      orderBy: { createdAt: 'desc' },
    })
  }),

  create: publicProcedure
    .input(
      z.object({
        email: z.string().email(),
        name: z.string().min(1),
      })
    )
    .mutation(async ({ ctx, input }) => {
      const user = await ctx.prisma.user.create({
        data: input,
      })
      return user
    }),
})
```

```typescript
// server/routers/_app.ts
import { router } from '../trpc/trpc'
import { userRouter } from './user'
import { postRouter } from './post'

export const appRouter = router({
  user: userRouter,
  post: postRouter,
})

export type AppRouter = typeof appRouter
```

## Procedures
### Query Procedure

```typescript
// server/routers/user.ts
export const userRouter = router({
  getById: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ ctx, input }) => {
      return ctx.prisma.user.findUnique({
        where: { id: input.id },
        include: { posts: true },
      })
    }),

  search: publicProcedure
    .input(
      z.object({
        query: z.string(),
        limit: z.number().min(1).max(100).default(10),
      })
    )
    .query(async ({ ctx, input }) => {
      return ctx.prisma.user.findMany({
        where: {
          OR: [
            { name: { contains: input.query } },
            { email: { contains: input.query } },
          ],
        },
        take: input.limit,
      })
    }),
})
```

### Mutation Procedure

```typescript
// server/routers/user.ts
export const userRouter = router({
  create: publicProcedure
    .input(
      z.object({
        email: z.string().email(),
        name: z.string().min(1).max(100),
      })
    )
    .mutation(async ({ ctx, input }) => {
      const existingUser = await ctx.prisma.user.findUnique({
        where: { email: input.email },
      })

      if (existingUser) {
        throw new TRPCError({
          code: 'CONFLICT',
          message: 'User with this email already exists',
        })
      }

      return ctx.prisma.user.create({
        data: input,
      })
    }),

  update: protectedProcedure
    .input(
      z.object({
        id: z.string(),
        name: z.string().min(1).optional(),
        email: z.string().email().optional(),
      })
    )
    .mutation(async ({ ctx, input }) => {
      const { id, ...data } = input

      // Ensure user can only update their own profile
      if (ctx.user.id !== id) {
        throw new TRPCError({
          code: 'FORBIDDEN',
          message: 'You can only update your own profile',
        })
      }

      return ctx.prisma.user.update({
        where: { id },
        data,
      })
    }),

  delete: protectedProcedure
    .input(z.object({ id: z.string() }))
    .mutation(async ({ ctx, input }) => {
      return ctx.prisma.user.delete({
        where: { id: input.id },
      })
    }),
})
```

### Subscription Procedure

```typescript
// server/routers/post.ts
import { observable } from '@trpc/server/observable'
import { EventEmitter } from 'events'

const postEventEmitter = new EventEmitter()

export const postRouter = router({
  onCreate: publicProcedure.subscription(() => {
    return observable<Post>((emit) => {
      const onPostCreate = (post: Post) => {
        emit.next(post)
      }

      postEventEmitter.on('create', onPostCreate)

      return () => {
        postEventEmitter.off('create', onPostCreate)
      }
    })
  }),
})
```

```typescript
// server/routers/user.ts
export const userRouter = router({
  getById: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ ctx, input }) => {
      return ctx.prisma.user.findUnique({
        where: { id: input.id },
        include: { posts: true },
      })
    }),

  search: publicProcedure
    .input(
      z.object({
        query: z.string(),
        limit: z.number().min(1).max(100).default(10),
      })
    )
    .query(async ({ ctx, input }) => {
      return ctx.prisma.user.findMany({
        where: {
          OR: [
            { name: { contains: input.query } },
            { email: { contains: input.query } },
          ],
        },
        take: input.limit,
      })
    }),
})
```

```typescript
// server/routers/user.ts
export const userRouter = router({
  create: publicProcedure
    .input(
      z.object({
        email: z.string().email(),
        name: z.string().min(1).max(100),
      })
    )
    .mutation(async ({ ctx, input }) => {
      const existingUser = await ctx.prisma.user.findUnique({
        where: { email: input.email },
      })

      if (existingUser) {
        throw new TRPCError({
          code: 'CONFLICT',
          message: 'User with this email already exists',
        })
      }

      return ctx.prisma.user.create({
        data: input,
      })
    }),

  update: protectedProcedure
    .input(
      z.object({
        id: z.string(),
        name: z.string().min(1).optional(),
        email: z.string().email().optional(),
      })
    )
    .mutation(async ({ ctx, input }) => {
      const { id, ...data } = input

      // Ensure user can only update their own profile
      if (ctx.user.id !== id) {
        throw new TRPCError({
          code: 'FORBIDDEN',
          message: 'You can only update your own profile',
        })
      }

      return ctx.prisma.user.update({
        where: { id },
        data,
      })
    }),

  delete: protectedProcedure
    .input(z.object({ id: z.string() }))
    .mutation(async ({ ctx, input }) => {
      return ctx.prisma.user.delete({
        where: { id: input.id },
      })
    }),
})
```

```typescript
// server/routers/post.ts
import { observable } from '@trpc/server/observable'
import { EventEmitter } from 'events'

const postEventEmitter = new EventEmitter()

export const postRouter = router({
  onCreate: publicProcedure.subscription(() => {
    return observable<Post>((emit) => {
      const onPostCreate = (post: Post) => {
        emit.next(post)
      }

      postEventEmitter.on('create', onPostCreate)

      return () => {
        postEventEmitter.off('create', onPostCreate)
      }
    })
  }),
})
```

## Input Validation with Zod
### Basic Validation

```typescript
import { z } from 'zod'

export const userRouter = router({
  create: publicProcedure
    .input(
      z.object({
        email: z.string().email('Invalid email address'),
        name: z.string().min(1, 'Name is required').max(100),
        age: z.number().int().min(0).max(150).optional(),
      })
    )
    .mutation(async ({ ctx, input }) => {
      // input is fully typed and validated
      return ctx.prisma.user.create({ data: input })
    }),
})
```

### Advanced Validation

```typescript
const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1),
  password: z.string().min(8).regex(/[A-Z]/, 'Password must contain uppercase'),
  confirmPassword: z.string(),
  role: z.enum(['USER', 'ADMIN']).default('USER'),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
})

export const userRouter = router({
  create: publicProcedure
    .input(createUserSchema)
    .mutation(async ({ ctx, input }) => {
      const { confirmPassword, ...userData } = input
      return ctx.prisma.user.create({ data: userData })
    }),
})
```

### Transform Input

```typescript
export const userRouter = router({
  create: publicProcedure
    .input(
      z.object({
        email: z.string().email().transform((email) => email.toLowerCase()),
        name: z.string().transform((name) => name.trim()),
      })
    )
    .mutation(async ({ ctx, input }) => {
      // email and name are already transformed
      return ctx.prisma.user.create({ data: input })
    }),
})
```

```typescript
import { z } from 'zod'

export const userRouter = router({
  create: publicProcedure
    .input(
      z.object({
        email: z.string().email('Invalid email address'),
        name: z.string().min(1, 'Name is required').max(100),
        age: z.number().int().min(0).max(150).optional(),
      })
    )
    .mutation(async ({ ctx, input }) => {
      // input is fully typed and validated
      return ctx.prisma.user.create({ data: input })
    }),
})
```

```typescript
const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1),
  password: z.string().min(8).regex(/[A-Z]/, 'Password must contain uppercase'),
  confirmPassword: z.string(),
  role: z.enum(['USER', 'ADMIN']).default('USER'),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
})

export const userRouter = router({
  create: publicProcedure
    .input(createUserSchema)
    .mutation(async ({ ctx, input }) => {
      const { confirmPassword, ...userData } = input
      return ctx.prisma.user.create({ data: userData })
    }),
})
```

```typescript
export const userRouter = router({
  create: publicProcedure
    .input(
      z.object({
        email: z.string().email().transform((email) => email.toLowerCase()),
        name: z.string().transform((name) => name.trim()),
      })
    )
    .mutation(async ({ ctx, input }) => {
      // email and name are already transformed
      return ctx.prisma.user.create({ data: input })
    }),
})
```

## Middleware
### Authentication Middleware

```typescript
// server/trpc/trpc.ts
const isAuthenticated = t.middleware(({ ctx, next }) => {
  if (!ctx.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' })
  }
  return next({
    ctx: {
      ...ctx,
      user: ctx.user,
    },
  })
})

export const protectedProcedure = t.procedure.use(isAuthenticated)
```

### Role-Based Middleware

```typescript
const isAdmin = t.middleware(({ ctx, next }) => {
  if (!ctx.user || ctx.user.role !== 'ADMIN') {
    throw new TRPCError({ code: 'FORBIDDEN' })
  }
  return next({
    ctx: {
      ...ctx,
      user: ctx.user,
    },
  })
})

export const adminProcedure = t.procedure.use(isAuthenticated).use(isAdmin)
```

### Logging Middleware

```typescript
const logger = t.middleware(async ({ path, type, next }) => {
  const start = Date.now()
  const result = await next()
  const duration = Date.now() - start

  console.log(`${type.toUpperCase()} ${path} - ${duration}ms`)

  return result
})

export const loggedProcedure = t.procedure.use(logger)
```

### Rate Limiting Middleware

```typescript
const rateLimiter = new Map<string, number[]>()

const rateLimit = t.middleware(async ({ ctx, next }) => {
  const ip = ctx.req.headers['x-forwarded-for'] || ctx.req.socket.remoteAddress
  const now = Date.now()
  const windowMs = 60000 // 1 minute
  const maxRequests = 10

  const requests = rateLimiter.get(ip as string) || []
  const recentRequests = requests.filter((time) => now - time < windowMs)

  if (recentRequests.length >= maxRequests) {
    throw new TRPCError({
      code: 'TOO_MANY_REQUESTS',
      message: 'Rate limit exceeded',
    })
  }

  recentRequests.push(now)
  rateLimiter.set(ip as string, recentRequests)

  return next()
})

export const rateLimitedProcedure = t.procedure.use(rateLimit)
```

```typescript
// server/trpc/trpc.ts
const isAuthenticated = t.middleware(({ ctx, next }) => {
  if (!ctx.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' })
  }
  return next({
    ctx: {
      ...ctx,
      user: ctx.user,
    },
  })
})

export const protectedProcedure = t.procedure.use(isAuthenticated)
```

```typescript
const isAdmin = t.middleware(({ ctx, next }) => {
  if (!ctx.user || ctx.user.role !== 'ADMIN') {
    throw new TRPCError({ code: 'FORBIDDEN' })
  }
  return next({
    ctx: {
      ...ctx,
      user: ctx.user,
    },
  })
})

export const adminProcedure = t.procedure.use(isAuthenticated).use(isAdmin)
```

```typescript
const logger = t.middleware(async ({ path, type, next }) => {
  const start = Date.now()
  const result = await next()
  const duration = Date.now() - start

  console.log(`${type.toUpperCase()} ${path} - ${duration}ms`)

  return result
})

export const loggedProcedure = t.procedure.use(logger)
```

```typescript
const rateLimiter = new Map<string, number[]>()

const rateLimit = t.middleware(async ({ ctx, next }) => {
  const ip = ctx.req.headers['x-forwarded-for'] || ctx.req.socket.remoteAddress
  const now = Date.now()
  const windowMs = 60000 // 1 minute
  const maxRequests = 10

  const requests = rateLimiter.get(ip as string) || []
  const recentRequests = requests.filter((time) => now - time < windowMs)

  if (recentRequests.length >= maxRequests) {
    throw new TRPCError({
      code: 'TOO_MANY_REQUESTS',
      message: 'Rate limit exceeded',
    })
  }

  recentRequests.push(now)
  rateLimiter.set(ip as string, recentRequests)

  return next()
})

export const rateLimitedProcedure = t.procedure.use(rateLimit)
```

## Next.js API Route Handler
### Create API Handler

```typescript
// app/api/trpc/[trpc]/route.ts
import { fetchRequestHandler } from '@trpc/server/adapters/fetch'
import { appRouter } from '@/server/routers/_app'
import { createContext } from '@/server/trpc/context'

const handler = (req: Request) =>
  fetchRequestHandler({
    endpoint: '/api/trpc',
    req,
    router: appRouter,
    createContext,
  })

export { handler as GET, handler as POST }
```

```typescript
// app/api/trpc/[trpc]/route.ts
import { fetchRequestHandler } from '@trpc/server/adapters/fetch'
import { appRouter } from '@/server/routers/_app'
import { createContext } from '@/server/trpc/context'

const handler = (req: Request) =>
  fetchRequestHandler({
    endpoint: '/api/trpc',
    req,
    router: appRouter,
    createContext,
  })

export { handler as GET, handler as POST }
```

## React Query Integration
### Setup Provider

```tsx
// app/providers.tsx
'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { httpBatchLink } from '@trpc/client'
import { createTRPCReact } from '@trpc/react-query'
import { useState } from 'react'
import type { AppRouter } from '@/server/routers/_app'

export const trpc = createTRPCReact<AppRouter>()

export function TRPCProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient())
  const [trpcClient] = useState(() =>
    trpc.createClient({
      links: [
        httpBatchLink({
          url: '/api/trpc',
        }),
      ],
    })
  )

  return (
    <trpc.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </trpc.Provider>
  )
}
```

### Use in Components

```tsx
'use client'

import { trpc } from '@/app/providers'

export function UserList() {
  const { data, isLoading, error } = trpc.user.getAll.useQuery()

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <ul>
      {data?.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}

export function CreateUserForm() {
  const utils = trpc.useUtils()
  const createUser = trpc.user.create.useMutation({
    onSuccess: () => {
      utils.user.getAll.invalidate()
    },
  })

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    createUser.mutate({
      email: formData.get('email') as string,
      name: formData.get('name') as string,
    })
  }

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" type="email" required />
      <input name="name" type="text" required />
      <button type="submit" disabled={createUser.isPending}>
        Create User
      </button>
    </form>
  )
}
```

```tsx
// app/providers.tsx
'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { httpBatchLink } from '@trpc/client'
import { createTRPCReact } from '@trpc/react-query'
import { useState } from 'react'
import type { AppRouter } from '@/server/routers/_app'

export const trpc = createTRPCReact<AppRouter>()

export function TRPCProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient())
  const [trpcClient] = useState(() =>
    trpc.createClient({
      links: [
        httpBatchLink({
          url: '/api/trpc',
        }),
      ],
    })
  )

  return (
    <trpc.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </trpc.Provider>
  )
}
```

```tsx
'use client'

import { trpc } from '@/app/providers'

export function UserList() {
  const { data, isLoading, error } = trpc.user.getAll.useQuery()

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <ul>
      {data?.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}

export function CreateUserForm() {
  const utils = trpc.useUtils()
  const createUser = trpc.user.create.useMutation({
    onSuccess: () => {
      utils.user.getAll.invalidate()
    },
  })

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    createUser.mutate({
      email: formData.get('email') as string,
      name: formData.get('name') as string,
    })
  }

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" type="email" required />
      <input name="name" type="text" required />
      <button type="submit" disabled={createUser.isPending}>
        Create User
      </button>
    </form>
  )
}
```

## Error Handling
### Custom Error Classes

```typescript
// server/trpc/errors.ts
import { TRPCError } from '@trpc/server'

export class UserNotFoundError extends TRPCError {
  constructor() {
    super({
      code: 'NOT_FOUND',
      message: 'User not found',
    })
  }
}

export class EmailAlreadyExistsError extends TRPCError {
  constructor(email: string) {
    super({
      code: 'CONFLICT',
      message: `User with email ${email} already exists`,
    })
  }
}
```

### Error Formatting

```typescript
// server/trpc/trpc.ts
import { TRPCError } from '@trpc/server'

const t = initTRPC.context<Context>().create({
  errorFormatter({ shape, error }) {
    return {
      ...shape,
      data: {
        ...shape.data,
        zodError:
          error.cause instanceof ZodError ? error.cause.flatten() : null,
      },
    }
  },
})
```

### Client-Side Error Handling

```tsx
'use client'

import { trpc } from '@/app/providers'

export function UserForm() {
  const createUser = trpc.user.create.useMutation({
    onError: (error) => {
      if (error.data?.code === 'CONFLICT') {
        alert('Email already exists')
      } else if (error.data?.code === 'BAD_REQUEST') {
        alert('Invalid input')
      } else {
        alert('An error occurred')
      }
    },
  })

  // ...
}
```

```typescript
// server/trpc/errors.ts
import { TRPCError } from '@trpc/server'

export class UserNotFoundError extends TRPCError {
  constructor() {
    super({
      code: 'NOT_FOUND',
      message: 'User not found',
    })
  }
}

export class EmailAlreadyExistsError extends TRPCError {
  constructor(email: string) {
    super({
      code: 'CONFLICT',
      message: `User with email ${email} already exists`,
    })
  }
}
```

```typescript
// server/trpc/trpc.ts
import { TRPCError } from '@trpc/server'

const t = initTRPC.context<Context>().create({
  errorFormatter({ shape, error }) {
    return {
      ...shape,
      data: {
        ...shape.data,
        zodError:
          error.cause instanceof ZodError ? error.cause.flatten() : null,
      },
    }
  },
})
```

```tsx
'use client'

import { trpc } from '@/app/providers'

export function UserForm() {
  const createUser = trpc.user.create.useMutation({
    onError: (error) => {
      if (error.data?.code === 'CONFLICT') {
        alert('Email already exists')
      } else if (error.data?.code === 'BAD_REQUEST') {
        alert('Invalid input')
      } else {
        alert('An error occurred')
      }
    },
  })

  // ...
}
```

## Type Inference
### Infer Router Types

```typescript
import type { AppRouter } from '@/server/routers/_app'
import type { inferRouterInputs, inferRouterOutputs } from '@trpc/server'

type RouterInputs = inferRouterInputs<AppRouter>
type RouterOutputs = inferRouterOutputs<AppRouter>

type UserOutput = RouterOutputs['user']['getById']
type CreateUserInput = RouterInputs['user']['create']
```

### Use in Components

```tsx
'use client'

import { trpc } from '@/app/providers'
import type { RouterOutputs } from '@/server/routers/_app'

type User = RouterOutputs['user']['getById']

export function UserCard({ userId }: { userId: string }) {
  const { data: user } = trpc.user.getById.useQuery({ id: userId })

  if (!user) return null

  return (
    <div>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  )
}
```

```typescript
import type { AppRouter } from '@/server/routers/_app'
import type { inferRouterInputs, inferRouterOutputs } from '@trpc/server'

type RouterInputs = inferRouterInputs<AppRouter>
type RouterOutputs = inferRouterOutputs<AppRouter>

type UserOutput = RouterOutputs['user']['getById']
type CreateUserInput = RouterInputs['user']['create']
```

```tsx
'use client'

import { trpc } from '@/app/providers'
import type { RouterOutputs } from '@/server/routers/_app'

type User = RouterOutputs['user']['getById']

export function UserCard({ userId }: { userId: string }) {
  const { data: user } = trpc.user.getById.useQuery({ id: userId })

  if (!user) return null

  return (
    <div>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  )
}
```

## Best Practices
1. **Type Safety**: Leverage TypeScript and tRPC for end-to-end type safety
2. **Validation**: Always validate inputs with Zod
3. **Error Handling**: Use appropriate error codes and messages
4. **Middleware**: Create reusable middleware for common concerns
5. **Performance**: Use React Query caching and invalidation strategically
6. **Security**: Validate permissions in protected procedures
7. **Documentation**: Document complex procedures and schemas

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Knowledge: nextjs-advanced.json
