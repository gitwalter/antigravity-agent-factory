---
description: Vitest setup and configuration, React Testing Library patterns, component
  testing (render, fireEvent, waitFor), mock patterns (MSW for API mocking), Playwright
  E2E testing, snapshot testing strategy, and coverage configuration.
name: frontend-testing
type: skill
---
# Frontend Testing

Vitest setup and configuration, React Testing Library patterns, component testing (render, fireEvent, waitFor), mock patterns (MSW for API mocking), Playwright E2E testing, snapshot testing strategy, and coverage configuration.

# Frontend Testing Skill

## Overview

This skill provides comprehensive guidance for testing React applications, including unit testing with Vitest, component testing with React Testing Library, API mocking with MSW, E2E testing with Playwright, and coverage configuration.

## Process

1. **Configure Vitest**: Set up Vitest configuration with jsdom environment, coverage settings, and path aliases
2. **Set up React Testing Library**: Configure test setup file with jest-dom matchers and cleanup utilities
3. **Write component tests**: Create tests for components using render, screen queries, and user interactions
4. **Add MSW for API mocking**: Set up Mock Service Worker server and handlers for API mocking in tests
5. **Configure Playwright for E2E**: Set up Playwright configuration with browser projects and web server
6. **Set coverage thresholds**: Configure coverage thresholds and reporting for test quality metrics

## Vitest Setup

### Installation

```bash
npm install -D vitest @vitest/ui @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

### Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/mockData',
      ],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

### Setup File

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom'
import { cleanup } from '@testing-library/react'
import { afterEach } from 'vitest'

afterEach(() => {
  cleanup()
})
```

## React Testing Library Patterns

### Basic Component Test

```typescript
// src/components/Button.test.tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Button } from './Button'

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument()
  })

  it('calls onClick when clicked', async () => {
    const handleClick = vi.fn()
    const user = userEvent.setup()

    render(<Button onClick={handleClick}>Click me</Button>)
    await user.click(screen.getByRole('button'))

    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })
})
```

### Testing Form Components

```typescript
// src/components/LoginForm.test.tsx
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { LoginForm } from './LoginForm'

describe('LoginForm', () => {
  it('submits form with valid data', async () => {
    const onSubmit = vi.fn()
    const user = userEvent.setup()

    render(<LoginForm onSubmit={onSubmit} />)

    await user.type(screen.getByLabelText(/email/i), 'user@example.com')
    await user.type(screen.getByLabelText(/password/i), 'password123')
    await user.click(screen.getByRole('button', { name: /sign in/i }))

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        email: 'user@example.com',
        password: 'password123',
      })
    })
  })

  it('shows validation errors for invalid input', async () => {
    const user = userEvent.setup()
    render(<LoginForm onSubmit={vi.fn()} />)

    await user.click(screen.getByRole('button', { name: /sign in/i }))

    await waitFor(() => {
      expect(screen.getByText(/email is required/i)).toBeInTheDocument()
      expect(screen.getByText(/password is required/i)).toBeInTheDocument()
    })
  })
})
```

### Testing Async Components

```typescript
// src/components/UserList.test.tsx
import { render, screen, waitFor } from '@testing-library/react'
import { UserList } from './UserList'
import { server } from '@/test/server'
import { rest } from 'msw'

describe('UserList', () => {
  it('displays users after loading', async () => {
    server.use(
      rest.get('/api/users', (req, res, ctx) => {
        return res(
          ctx.json([
            { id: '1', name: 'John Doe', email: 'john@example.com' },
            { id: '2', name: 'Jane Smith', email: 'jane@example.com' },
          ])
        )
      })
    )

    render(<UserList />)

    expect(screen.getByText(/loading/i)).toBeInTheDocument()

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument()
      expect(screen.getByText('Jane Smith')).toBeInTheDocument()
    })
  })

  it('displays error message on fetch failure', async () => {
    server.use(
      rest.get('/api/users', (req, res, ctx) => {
        return res(ctx.status(500), ctx.json({ error: 'Server error' }))
      })
    )

    render(<UserList />)

    await waitFor(() => {
      expect(screen.getByText(/error loading users/i)).toBeInTheDocument()
    })
  })
})
```

### Testing Custom Hooks

```typescript
// src/hooks/useCounter.test.ts
import { renderHook, act } from '@testing-library/react'
import { useCounter } from './useCounter'

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter())
    expect(result.current.count).toBe(0)
  })

  it('increments count', () => {
    const { result } = renderHook(() => useCounter())
    
    act(() => {
      result.current.increment()
    })

    expect(result.current.count).toBe(1)
  })

  it('decrements count', () => {
    const { result } = renderHook(() => useCounter({ initialValue: 5 }))
    
    act(() => {
      result.current.decrement()
    })

    expect(result.current.count).toBe(4)
  })

  it('resets count', () => {
    const { result } = renderHook(() => useCounter({ initialValue: 10 }))
    
    act(() => {
      result.current.increment()
      result.current.reset()
    })

    expect(result.current.count).toBe(10)
  })
})
```

## Mock Service Worker (MSW) Setup

### Server Setup

```typescript
// src/test/server.ts
import { setupServer } from 'msw/node'
import { handlers } from './handlers'

export const server = setupServer(...handlers)
```

### Handlers

```typescript
// src/test/handlers.ts
import { rest } from 'msw'

export const handlers = [
  rest.get('/api/users', (req, res, ctx) => {
    return res(
      ctx.json([
        { id: '1', name: 'John Doe', email: 'john@example.com' },
        { id: '2', name: 'Jane Smith', email: 'jane@example.com' },
      ])
    )
  }),

  rest.post('/api/users', async (req, res, ctx) => {
    const body = await req.json()
    return res(
      ctx.json({
        id: '3',
        ...body,
      })
    )
  }),

  rest.get('/api/users/:id', (req, res, ctx) => {
    const { id } = req.params
    return res(
      ctx.json({
        id,
        name: 'John Doe',
        email: 'john@example.com',
      })
    )
  }),
]
```

### Setup in Tests

```typescript
// vitest.config.ts or setup file
import { beforeAll, afterEach, afterAll } from 'vitest'
import { server } from './src/test/server'

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

## Playwright E2E Testing

### Installation

```bash
npm install -D @playwright/test
npx playwright install
```

### Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

### E2E Test Example

```typescript
// e2e/user-flow.spec.ts
import { test, expect } from '@playwright/test'

test.describe('User Flow', () => {
  test('user can login and view dashboard', async ({ page }) => {
    await page.goto('/login')

    await page.fill('[name="email"]', 'user@example.com')
    await page.fill('[name="password"]', 'password123')
    await page.click('button[type="submit"]')

    await expect(page).toHaveURL('/dashboard')
    await expect(page.locator('h1')).toContainText('Dashboard')
  })

  test('user can create a new post', async ({ page }) => {
    await page.goto('/dashboard')
    
    await page.click('text=New Post')
    await page.fill('[name="title"]', 'My New Post')
    await page.fill('[name="content"]', 'This is the content')
    await page.click('button[type="submit"]')

    await expect(page.locator('text=My New Post')).toBeVisible()
  })

  test('user can search for posts', async ({ page }) => {
    await page.goto('/posts')
    
    await page.fill('[name="search"]', 'React')
    await page.press('[name="search"]', 'Enter')

    await expect(page.locator('.post-item')).toContainText('React')
  })
})
```

## Snapshot Testing

### Component Snapshot

```typescript
// src/components/Card.test.tsx
import { render } from '@testing-library/react'
import { Card } from './Card'

describe('Card', () => {
  it('matches snapshot', () => {
    const { container } = render(
      <Card title="Test Title">
        <p>Test content</p>
      </Card>
    )
    expect(container.firstChild).toMatchSnapshot()
  })
})
```

### Snapshot Update

```bash
# Update snapshots
npm test -- -u
```

## Coverage Configuration

### Coverage Thresholds

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },
  },
})
```

### Coverage Report

```bash
# Generate coverage report
npm test -- --coverage

# View HTML report
open coverage/index.html
```

## Testing Best Practices

### 1. Test User Behavior, Not Implementation

```typescript
// ❌ Bad: Testing implementation details
expect(component.state.count).toBe(1)

// ✅ Good: Testing user-visible behavior
expect(screen.getByText('Count: 1')).toBeInTheDocument()
```

### 2. Use Accessible Queries

```typescript
// Prefer in order:
// 1. getByRole
// 2. getByLabelText
// 3. getByText
// 4. getByTestId (last resort)

// ✅ Good
screen.getByRole('button', { name: /submit/i })
screen.getByLabelText(/email/i)

// ❌ Avoid
screen.getByTestId('submit-button')
```

### 3. Test Error States

```typescript
it('handles error state', async () => {
  server.use(
    rest.get('/api/users', (req, res, ctx) => {
      return res(ctx.status(500))
    })
  )

  render(<UserList />)

  await waitFor(() => {
    expect(screen.getByText(/error/i)).toBeInTheDocument()
  })
})
```

### 4. Clean Up After Tests

```typescript
afterEach(() => {
  cleanup()
  server.resetHandlers()
})
```

### 5. Use waitFor for Async Operations

```typescript
await waitFor(() => {
  expect(screen.getByText('Loaded content')).toBeInTheDocument()
})
```

## Test Utilities

### Custom Render Function

```typescript
// src/test/utils.tsx
import { render, RenderOptions } from '@testing-library/react'
import { ReactElement } from 'react'
import { TRPCProvider } from '@/app/providers'

const AllTheProviders = ({ children }: { children: React.ReactNode }) => {
  return <TRPCProvider>{children}</TRPCProvider>
}

const customRender = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) => render(ui, { wrapper: AllTheProviders, ...options })

export * from '@testing-library/react'
export { customRender as render }
```

## Best Practices

1. **Test User Behavior**: Focus on what users see and do, not implementation details
2. **Use MSW**: Mock API calls at the network level with MSW
3. **Accessible Queries**: Prefer queries that reflect how users interact
4. **Async Testing**: Always use waitFor for async operations
5. **Clean Tests**: Keep tests isolated and independent
6. **E2E Coverage**: Use Playwright for critical user flows
7. **Coverage Goals**: Aim for meaningful coverage, not 100%

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
