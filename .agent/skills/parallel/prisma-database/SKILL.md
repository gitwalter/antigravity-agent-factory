---
description: Prisma schema design patterns, relations (1:1, 1:N, M:N), migrations
  workflow, Prisma Client queries (findMany, create, update, transactions), seeding,
  type-safe queries, and performance optimization.
name: prisma-database
type: skill
---
# Prisma Database

Prisma schema design patterns, relations (1:1, 1:N, M:N), migrations workflow, Prisma Client queries (findMany, create, update, transactions), seeding, type-safe queries, and performance optimization.

# Prisma Database Skill

## Overview

This skill provides comprehensive guidance for working with Prisma ORM, including schema design, relations, migrations, query patterns, transactions, seeding, and performance optimization.

## Process

1. **Define schema models and relations**: Create Prisma schema with models, fields, and relationships (1:1, 1:N, M:N)
2. **Run migrations**: Generate and apply migrations to create/update database schema
3. **Generate Prisma Client**: Generate type-safe Prisma Client from schema
4. **Write type-safe queries**: Use Prisma Client for queries, mutations, and transactions
5. **Add seeding**: Create seed scripts for development and testing data
6. **Optimize performance**: Use select, include efficiently, add indexes, and implement connection pooling

## Schema Design Patterns

### Basic Schema

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  posts     Post[]
}
```

### Enums

```prisma
enum Role {
  USER
  ADMIN
  MODERATOR
}

model User {
  id   String @id @default(cuid())
  role Role   @default(USER)
}
```

### Composite Types (MongoDB)

```prisma
type Address {
  street  String
  city    String
  zipCode String
  country String
}

model User {
  id      String   @id @default(cuid())
  address Address?
}
```

## Relations

### One-to-Many (1:N)

```prisma
model User {
  id    String @id @default(cuid())
  posts Post[]
}

model Post {
  id       String @id @default(cuid())
  title    String
  authorId String
  author   User   @relation(fields: [authorId], references: [id])
}
```

### Many-to-Many (M:N)

```prisma
model Post {
  id     String    @id @default(cuid())
  title  String
  tags   PostTag[]
}

model Tag {
  id    String    @id @default(cuid())
  name  String    @unique
  posts PostTag[]
}

model PostTag {
  postId String
  tagId  String
  post   Post @relation(fields: [postId], references: [id])
  tag    Tag  @relation(fields: [tagId], references: [id])

  @@id([postId, tagId])
}
```

### One-to-One (1:1)

```prisma
model User {
  id      String   @id @default(cuid())
  profile Profile?
}

model Profile {
  id     String @id @default(cuid())
  bio    String?
  userId String @unique
  user   User   @relation(fields: [userId], references: [id])
}
```

### Self-Relations

```prisma
model User {
  id          String   @id @default(cuid())
  name        String
  managerId   String?
  manager     User?    @relation("UserManager", fields: [managerId], references: [id])
  directReports User[] @relation("UserManager")
}
```

## Prisma Client Queries

### Basic Queries

```typescript
import { prisma } from '@/lib/prisma'

// Find many
const users = await prisma.user.findMany({
  where: { role: 'ADMIN' },
  orderBy: { createdAt: 'desc' },
})

// Find unique
const user = await prisma.user.findUnique({
  where: { email: 'user@example.com' },
})

// Find first
const firstUser = await prisma.user.findFirst({
  where: { name: { contains: 'John' } },
})
```

### Include Relations

```typescript
const userWithPosts = await prisma.user.findUnique({
  where: { id: 'user-id' },
  include: {
    posts: {
      where: { published: true },
      orderBy: { createdAt: 'desc' },
    },
  },
})
```

### Select Specific Fields

```typescript
const users = await prisma.user.findMany({
  select: {
    id: true,
    name: true,
    email: true,
    // Exclude posts
  },
})
```

### Filtering

```typescript
// AND conditions
const users = await prisma.user.findMany({
  where: {
    AND: [
      { role: 'ADMIN' },
      { createdAt: { gte: new Date('2024-01-01') } },
    ],
  },
})

// OR conditions
const users = await prisma.user.findMany({
  where: {
    OR: [
      { email: { contains: '@example.com' } },
      { name: { contains: 'Admin' } },
    ],
  },
})

// NOT conditions
const users = await prisma.user.findMany({
  where: {
    NOT: {
      role: 'ADMIN',
    },
  },
})
```

### Pagination

```typescript
// Offset pagination
const users = await prisma.user.findMany({
  skip: 10,
  take: 20,
  orderBy: { createdAt: 'desc' },
})

// Cursor pagination
const users = await prisma.user.findMany({
  take: 20,
  cursor: { id: 'last-user-id' },
  skip: 1,
  orderBy: { id: 'asc' },
})
```

## Mutations

### Create

```typescript
// Single create
const user = await prisma.user.create({
  data: {
    email: 'user@example.com',
    name: 'John Doe',
  },
})

// Create with relation
const post = await prisma.post.create({
  data: {
    title: 'My Post',
    author: {
      connect: { id: 'user-id' },
    },
  },
})

// Create many
const users = await prisma.user.createMany({
  data: [
    { email: 'user1@example.com', name: 'User 1' },
    { email: 'user2@example.com', name: 'User 2' },
  ],
  skipDuplicates: true,
})
```

### Update

```typescript
// Update single
const user = await prisma.user.update({
  where: { id: 'user-id' },
  data: {
    name: 'Updated Name',
  },
})

// Update many
const result = await prisma.user.updateMany({
  where: { role: 'USER' },
  data: { role: 'ADMIN' },
})

// Upsert
const user = await prisma.user.upsert({
  where: { email: 'user@example.com' },
  update: { name: 'Updated Name' },
  create: {
    email: 'user@example.com',
    name: 'New User',
  },
})
```

### Delete

```typescript
// Delete single
const user = await prisma.user.delete({
  where: { id: 'user-id' },
})

// Delete many
const result = await prisma.user.deleteMany({
  where: { role: 'GUEST' },
})
```

## Transactions

### Sequential Operations

```typescript
const result = await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({
    data: {
      email: 'user@example.com',
      name: 'John Doe',
    },
  })

  const post = await tx.post.create({
    data: {
      title: 'First Post',
      authorId: user.id,
    },
  })

  return { user, post }
})
```

### Interactive Transactions

```typescript
const result = await prisma.$transaction(
  async (tx) => {
    const user = await tx.user.findUnique({
      where: { id: 'user-id' },
    })

    if (!user) {
      throw new Error('User not found')
    }

    const updatedUser = await tx.user.update({
      where: { id: user.id },
      data: { name: 'Updated Name' },
    })

    return updatedUser
  },
  {
    maxWait: 5000,
    timeout: 10000,
  }
)
```

### Batch Transactions

```typescript
const [users, posts] = await prisma.$transaction([
  prisma.user.findMany(),
  prisma.post.findMany(),
])
```

## Raw Queries

### Raw SQL

```typescript
const users = await prisma.$queryRaw`
  SELECT * FROM "User" WHERE "role" = ${'ADMIN'}
`

// With Prisma types
const users = await prisma.$queryRaw<User[]>`
  SELECT * FROM "User" WHERE "createdAt" > ${new Date('2024-01-01')}
`
```

### Raw Query with Parameters

```typescript
const users = await prisma.$queryRawUnsafe(
  'SELECT * FROM "User" WHERE "email" = $1',
  'user@example.com'
)
```

## Migrations

### Create Migration

```bash
npx prisma migrate dev --name add_user_role
```

### Apply Migrations

```bash
npx prisma migrate deploy
```

### Reset Database

```bash
npx prisma migrate reset
```

### Migration File Example

```prisma
// prisma/migrations/20240101000000_add_user_role/migration.sql
ALTER TABLE "User" ADD COLUMN "role" TEXT NOT NULL DEFAULT 'USER';
```

## Seeding

### Seed Script

```typescript
// prisma/seed.ts
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function main() {
  // Create users
  const user1 = await prisma.user.upsert({
    where: { email: 'alice@example.com' },
    update: {},
    create: {
      email: 'alice@example.com',
      name: 'Alice',
      posts: {
        create: {
          title: 'First Post',
          content: 'This is my first post',
        },
      },
    },
  })

  const user2 = await prisma.user.upsert({
    where: { email: 'bob@example.com' },
    update: {},
    create: {
      email: 'bob@example.com',
      name: 'Bob',
    },
  })

  console.log({ user1, user2 })
}

main()
  .catch((e) => {
    console.error(e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })
```

### Package.json Script

```json
{
  "prisma": {
    "seed": "ts-node prisma/seed.ts"
  }
}
```

## Performance Optimization

### Select Only Needed Fields

```typescript
// Bad: Fetches all fields
const users = await prisma.user.findMany()

// Good: Select only needed fields
const users = await prisma.user.findMany({
  select: {
    id: true,
    name: true,
    email: true,
  },
})
```

### Batch Operations

```typescript
// Bad: Multiple queries
for (const id of userIds) {
  await prisma.user.update({
    where: { id },
    data: { role: 'ADMIN' },
  })
}

// Good: Single batch update
await prisma.user.updateMany({
  where: { id: { in: userIds } },
  data: { role: 'ADMIN' },
})
```

### Use Indexes

```prisma
model User {
  id    String @id @default(cuid())
  email String @unique
  name  String

  @@index([name])
  @@index([email, name])
}
```

### Connection Pooling

```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
  })

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma
```

## Middleware

### Logging Middleware

```typescript
prisma.$use(async (params, next) => {
  const before = Date.now()
  const result = await next(params)
  const after = Date.now()
  console.log(`Query ${params.model}.${params.action} took ${after - before}ms`)
  return result
})
```

### Query Modification Middleware

```typescript
prisma.$use(async (params, next) => {
  if (params.action === 'findMany' && params.model === 'User') {
    params.args.where = {
      ...params.args.where,
      deletedAt: null,
    }
  }
  return next(params)
})
```

## Best Practices

1. **Use Transactions**: For operations that must succeed or fail together
2. **Select Specific Fields**: Only fetch what you need
3. **Use Indexes**: Add indexes for frequently queried fields
4. **Batch Operations**: Group multiple operations when possible
5. **Connection Pooling**: Reuse database connections
6. **Type Safety**: Leverage Prisma's generated types
7. **Migrations**: Always use migrations, never modify database directly
8. **Seeding**: Use seed scripts for development and testing data

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
