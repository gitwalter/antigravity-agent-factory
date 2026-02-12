---
description: Core Web Vitals optimization, code splitting, and React performance patterns
name: frontend-performance
type: skill
---

# Frontend Performance

Core Web Vitals optimization, code splitting, and React performance patterns

## 
# Frontend Performance Optimization

## 
# Frontend Performance Optimization

## Process
### 1. Core Web Vitals Optimization

**Largest Contentful Paint (LCP)** - Optimize the largest element load time:

```tsx
// Optimize images with next/image
import Image from 'next/image';

export function HeroSection() {
  return (
    <Image
      src="/hero-image.jpg"
      alt="Hero"
      width={1200}
      height={600}
      priority // Preload above-the-fold images
      placeholder="blur" // Show blur placeholder while loading
      quality={85} // Optimize quality vs size
    />
  );
}
```

**First Input Delay (FID)** - Reduce JavaScript execution time:

```tsx
// Use React.memo for expensive components
import { memo } from 'react';

export const ExpensiveList = memo(({ items }: { items: Item[] }) => {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
}, (prevProps, nextProps) => {
  // Custom comparison function
  return prevProps.items.length === nextProps.items.length;
});
```

**Cumulative Layout Shift (CLS)** - Prevent layout shifts:

```tsx
// Reserve space for dynamic content
export function ProductCard({ product }: { product: Product }) {
  return (
    <div className="card" style={{ minHeight: '400px' }}>
      {product.image && (
        <img 
          src={product.image} 
          alt={product.name}
          width={300}
          height={300}
          style={{ display: 'block' }} // Prevent inline spacing
        />
      )}
    </div>
  );
}
```

### 2. React Performance Patterns

**useMemo and useCallback Strategy**:

```tsx
import { useMemo, useCallback, useState } from 'react';

export function ProductList({ products }: { products: Product[] }) {
  const [filter, setFilter] = useState('');
  
  // Memoize expensive computations
  const filteredProducts = useMemo(() => {
    return products.filter(p => 
      p.name.toLowerCase().includes(filter.toLowerCase())
    );
  }, [products, filter]);
  
  // Memoize callbacks to prevent child re-renders
  const handleClick = useCallback((id: string) => {
    console.log('Clicked:', id);
  }, []);
  
  return (
    <div>
      <input 
        value={filter} 
        onChange={(e) => setFilter(e.target.value)} 
      />
      {filteredProducts.map(product => (
        <ProductItem 
          key={product.id} 
          product={product}
          onClick={handleClick}
        />
      ))}
    </div>
  );
}
```

### 3. Code Splitting with Dynamic Imports

```tsx
// Lazy load heavy components
import { lazy, Suspense } from 'react';

const HeavyChart = lazy(() => import('./HeavyChart'));
const AdminPanel = lazy(() => import('./AdminPanel'));

export function Dashboard() {
  return (
    <div>
      <Suspense fallback={<div>Loading chart...</div>}>
        <HeavyChart />
      </Suspense>
      
      {isAdmin && (
        <Suspense fallback={<div>Loading admin...</div>}>
          <AdminPanel />
        </Suspense>
      )}
    </div>
  );
}
```

### 4. Font Optimization

```tsx
// next/font for automatic font optimization
import { Inter } from 'next/font/google';

const inter = Inter({ 
  subsets: ['latin'],
  display: 'swap', // Prevent invisible text during font load
  preload: true,
});

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html className={inter.className}>
      <body>{children}</body>
    </html>
  );
}
```

### 5. Bundle Analysis

```typescript
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  // Your Next.js config
  experimental: {
    optimizePackageImports: ['@mui/material', 'lodash'],
  },
});
```

### 6. Server Component Streaming

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react';

async function SlowData() {
  const data = await fetchData(); // Server component
  return <div>{data}</div>;
}

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<Skeleton />}>
        <SlowData />
      </Suspense>
    </div>
  );
}
```

### 7. Caching Strategies

```typescript
// Route segment config for Next.js App Router
export const revalidate = 3600; // ISR: revalidate every hour

// Or per-request caching
async function getData() {
  const res = await fetch('https://api.example.com/data', {
    next: { 
      revalidate: 60, // Cache for 60 seconds
      tags: ['products'] // Tag-based revalidation
    }
  });
  return res.json();
}
```

```tsx
// Optimize images with next/image
import Image from 'next/image';

export function HeroSection() {
  return (
    <Image
      src="/hero-image.jpg"
      alt="Hero"
      width={1200}
      height={600}
      priority // Preload above-the-fold images
      placeholder="blur" // Show blur placeholder while loading
      quality={85} // Optimize quality vs size
    />
  );
}
```

```tsx
// Use React.memo for expensive components
import { memo } from 'react';

export const ExpensiveList = memo(({ items }: { items: Item[] }) => {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
}, (prevProps, nextProps) => {
  // Custom comparison function
  return prevProps.items.length === nextProps.items.length;
});
```

```tsx
// Reserve space for dynamic content
export function ProductCard({ product }: { product: Product }) {
  return (
    <div className="card" style={{ minHeight: '400px' }}>
      {product.image && (
        <img 
          src={product.image} 
          alt={product.name}
          width={300}
          height={300}
          style={{ display: 'block' }} // Prevent inline spacing
        />
      )}
    </div>
  );
}
```

```tsx
import { useMemo, useCallback, useState } from 'react';

export function ProductList({ products }: { products: Product[] }) {
  const [filter, setFilter] = useState('');
  
  // Memoize expensive computations
  const filteredProducts = useMemo(() => {
    return products.filter(p => 
      p.name.toLowerCase().includes(filter.toLowerCase())
    );
  }, [products, filter]);
  
  // Memoize callbacks to prevent child re-renders
  const handleClick = useCallback((id: string) => {
    console.log('Clicked:', id);
  }, []);
  
  return (
    <div>
      <input 
        value={filter} 
        onChange={(e) => setFilter(e.target.value)} 
      />
      {filteredProducts.map(product => (
        <ProductItem 
          key={product.id} 
          product={product}
          onClick={handleClick}
        />
      ))}
    </div>
  );
}
```

```tsx
// Lazy load heavy components
import { lazy, Suspense } from 'react';

const HeavyChart = lazy(() => import('./HeavyChart'));
const AdminPanel = lazy(() => import('./AdminPanel'));

export function Dashboard() {
  return (
    <div>
      <Suspense fallback={<div>Loading chart...</div>}>
        <HeavyChart />
      </Suspense>
      
      {isAdmin && (
        <Suspense fallback={<div>Loading admin...</div>}>
          <AdminPanel />
        </Suspense>
      )}
    </div>
  );
}
```

```tsx
// next/font for automatic font optimization
import { Inter } from 'next/font/google';

const inter = Inter({ 
  subsets: ['latin'],
  display: 'swap', // Prevent invisible text during font load
  preload: true,
});

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html className={inter.className}>
      <body>{children}</body>
    </html>
  );
}
```

```typescript
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  // Your Next.js config
  experimental: {
    optimizePackageImports: ['@mui/material', 'lodash'],
  },
});
```

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react';

async function SlowData() {
  const data = await fetchData(); // Server component
  return <div>{data}</div>;
}

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<Skeleton />}>
        <SlowData />
      </Suspense>
    </div>
  );
}
```

```typescript
// Route segment config for Next.js App Router
export const revalidate = 3600; // ISR: revalidate every hour

// Or per-request caching
async function getData() {
  const res = await fetch('https://api.example.com/data', {
    next: { 
      revalidate: 60, // Cache for 60 seconds
      tags: ['products'] // Tag-based revalidation
    }
  });
  return res.json();
}
```

## Best Practices
- **Code Splitting**: Use dynamic imports and React.lazy to split code by route and component, reducing initial bundle size
- **Lazy Loading**: Lazy load images, components, and routes that aren't immediately visible to improve initial load time
- **Image Optimization**: Use Next.js Image component or similar with proper sizing, formats (WebP/AVIF), and lazy loading
- **Memoization**: Use React.memo, useMemo, and useCallback strategically to prevent unnecessary re-renders
- **Bundle Analysis**: Regularly analyze bundle size with webpack-bundle-analyzer to identify and eliminate large dependencies
- **Font Optimization**: Use next/font or font-display: swap to prevent invisible text during font load (FOIT)
- **Caching Strategies**: Implement proper caching (ISR, SSG, SWR) for static and dynamic content to reduce server load
- **Performance Monitoring**: Set up Core Web Vitals monitoring and performance budgets to track and maintain performance

## Output
- Optimized React components with memoization
- Code-split routes and components
- Optimized images and fonts
- Bundle analysis reports
- Core Web Vitals improvements (target: LCP < 2.5s, FID < 100ms, CLS < 0.1)
- Caching configuration for static and dynamic content
- Performance monitoring setup

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Knowledge: frontend-performance-patterns.json
