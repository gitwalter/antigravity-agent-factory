---
description: SQLAlchemy 2.0 patterns (mapped_column, Mapped types), Async engine and
  sessions, Relationship patterns, Alembic migrations, Repository pattern, Query optimization,
  Connection pooling
name: sqlalchemy-patterns
type: skill
---

# Sqlalchemy Patterns

SQLAlchemy 2.0 patterns (mapped_column, Mapped types), Async engine and sessions, Relationship patterns, Alembic migrations, Repository pattern, Query optimization, Connection pooling

## 
# SQLAlchemy Patterns Skill

Build production data access layers using SQLAlchemy 2.0 with async patterns, relationships, and migrations.

## 
# SQLAlchemy Patterns Skill

Build production data access layers using SQLAlchemy 2.0 with async patterns, relationships, and migrations.

## Process
### Step 1: SQLAlchemy 2.0 Models

Use modern SQLAlchemy 2.0 syntax with `Mapped` types and `mapped_column`:

```python
# src/core/database.py
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, Text, Boolean
from datetime import datetime
from typing import Optional, List

class Base(DeclarativeBase):
    pass

# src/domains/users/models.py
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, onupdate=datetime.utcnow)
    
    # Relationships
    posts: Mapped[List["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")

# src/domains/posts/models.py
class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    author: Mapped["User"] = relationship(back_populates="posts")
```

### Step 2: Async Engine and Sessions

Configure async engine and session factory:

```python
# src/core/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from .config import get_settings

settings = get_settings()

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # Log SQL queries in debug mode
    future=True,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit
    autocommit=False,
    autoflush=False,
)

async def get_async_session() -> AsyncSession:
    """Get async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

### Step 3: Relationship Patterns

Define relationships with proper loading strategies:

```python
# Eager loading with selectinload
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def get_user_with_posts(user_id: int, db: AsyncSession) -> User:
    """Get user with posts loaded."""
    result = await db.execute(
        select(User)
        .options(selectinload(User.posts))
        .where(User.id == user_id)
    )
    return result.scalar_one_or_none()

# Lazy loading (default, but async requires explicit loading)
async def get_user_posts(user_id: int, db: AsyncSession) -> List[Post]:
    """Get user's posts."""
    result = await db.execute(
        select(User)
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if user:
        # Load relationship explicitly
        await db.execute(
            select(Post)
            .where(Post.author_id == user_id)
        )
        return user.posts
    return []

# Joined loading for single query
async def get_user_with_posts_joined(user_id: int, db: AsyncSession) -> User:
    """Get user with posts using join."""
    result = await db.execute(
        select(User)
        .options(selectinload(User.posts))
        .where(User.id == user_id)
    )
    return result.scalar_one_or_none()
```

### Step 4: Alembic Migrations

Set up and use Alembic for database migrations:

```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from src.core.database import Base
from src.core.config import get_settings

settings = get_settings()

config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url.replace("+asyncpg", ""))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
```

Create migrations:

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Create named migration
alembic revision -m "Add user table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Step 5: Repository Pattern

Implement repository pattern for data access:

```python
# src/core/repository.py
from typing import Generic, TypeVar, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import DeclarativeBase

ModelType = TypeVar("ModelType", bound=DeclarativeBase)

class Repository(Generic[ModelType]):
    def __init__(self, model: type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session
    
    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """Get entity by ID."""
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all entities with pagination."""
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def create(self, **kwargs) -> ModelType:
        """Create new entity."""
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance
    
    async def update(self, id: int, **kwargs) -> Optional[ModelType]:
        """Update entity."""
        await self.session.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**kwargs)
        )
        await self.session.flush()
        return await self.get_by_id(id)
    
    async def delete(self, id: int) -> bool:
        """Delete entity."""
        result = await self.session.execute(
            delete(self.model).where(self.model.id == id)
        )
        await self.session.flush()
        return result.rowcount > 0

# Usage
# src/domains/users/repository.py
from src.core.repository import Repository
from .models import User

class UserRepository(Repository[User]):
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_active_users(self) -> List[User]:
        """Get all active users."""
        result = await self.session.execute(
            select(User).where(User.is_active == True)
        )
        return list(result.scalars().all())
```

### Step 6: Query Optimization

Optimize queries to avoid N+1 problems:

```python
# Bad: N+1 query problem
async def get_users_with_posts_bad(db: AsyncSession) -> List[User]:
    """Bad: Causes N+1 queries."""
    result = await db.execute(select(User))
    users = list(result.scalars().all())
    # This will cause a query for each user's posts
    for user in users:
        _ = user.posts  # Separate query for each user
    return users

# Good: Eager loading
async def get_users_with_posts_good(db: AsyncSession) -> List[User]:
    """Good: Single query with join."""
    result = await db.execute(
        select(User)
        .options(selectinload(User.posts))
    )
    return list(result.scalars().all())

# Bulk operations
async def bulk_create_users(db: AsyncSession, users_data: List[dict]) -> List[User]:
    """Create multiple users efficiently."""
    users = [User(**data) for data in users_data]
    db.add_all(users)
    await db.flush()
    return users

# Bulk update
async def bulk_update_users(db: AsyncSession, updates: List[dict]) -> None:
    """Update multiple users efficiently."""
    await db.execute(
        update(User),
        updates  # List of dicts with id and fields to update
    )
    await db.flush()
```

### Step 7: Connection Pooling

Configure connection pooling for production:

```python
# src/core/database.py
engine = create_async_engine(
    settings.database_url,
    pool_size=20,           # Number of connections to maintain
    max_overflow=10,         # Additional connections beyond pool_size
    pool_pre_ping=True,      # Verify connections before using
    pool_recycle=3600,       # Recycle connections after 1 hour
    pool_timeout=30,         # Timeout for getting connection from pool
    echo_pool="debug",       # Log pool events
)
```

```python
# src/core/database.py
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, Text, Boolean
from datetime import datetime
from typing import Optional, List

class Base(DeclarativeBase):
    pass

# src/domains/users/models.py
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, onupdate=datetime.utcnow)
    
    # Relationships
    posts: Mapped[List["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")

# src/domains/posts/models.py
class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    author: Mapped["User"] = relationship(back_populates="posts")
```

```python
# src/core/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from .config import get_settings

settings = get_settings()

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # Log SQL queries in debug mode
    future=True,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit
    autocommit=False,
    autoflush=False,
)

async def get_async_session() -> AsyncSession:
    """Get async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

```python
# Eager loading with selectinload
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def get_user_with_posts(user_id: int, db: AsyncSession) -> User:
    """Get user with posts loaded."""
    result = await db.execute(
        select(User)
        .options(selectinload(User.posts))
        .where(User.id == user_id)
    )
    return result.scalar_one_or_none()

# Lazy loading (default, but async requires explicit loading)
async def get_user_posts(user_id: int, db: AsyncSession) -> List[Post]:
    """Get user's posts."""
    result = await db.execute(
        select(User)
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if user:
        # Load relationship explicitly
        await db.execute(
            select(Post)
            .where(Post.author_id == user_id)
        )
        return user.posts
    return []

# Joined loading for single query
async def get_user_with_posts_joined(user_id: int, db: AsyncSession) -> User:
    """Get user with posts using join."""
    result = await db.execute(
        select(User)
        .options(selectinload(User.posts))
        .where(User.id == user_id)
    )
    return result.scalar_one_or_none()
```

```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from src.core.database import Base
from src.core.config import get_settings

settings = get_settings()

config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url.replace("+asyncpg", ""))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
```

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Create named migration
alembic revision -m "Add user table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

```python
# src/core/repository.py
from typing import Generic, TypeVar, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import DeclarativeBase

ModelType = TypeVar("ModelType", bound=DeclarativeBase)

class Repository(Generic[ModelType]):
    def __init__(self, model: type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session
    
    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """Get entity by ID."""
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all entities with pagination."""
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def create(self, **kwargs) -> ModelType:
        """Create new entity."""
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance
    
    async def update(self, id: int, **kwargs) -> Optional[ModelType]:
        """Update entity."""
        await self.session.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**kwargs)
        )
        await self.session.flush()
        return await self.get_by_id(id)
    
    async def delete(self, id: int) -> bool:
        """Delete entity."""
        result = await self.session.execute(
            delete(self.model).where(self.model.id == id)
        )
        await self.session.flush()
        return result.rowcount > 0

# Usage
# src/domains/users/repository.py
from src.core.repository import Repository
from .models import User

class UserRepository(Repository[User]):
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_active_users(self) -> List[User]:
        """Get all active users."""
        result = await self.session.execute(
            select(User).where(User.is_active == True)
        )
        return list(result.scalars().all())
```

```python
# Bad: N+1 query problem
async def get_users_with_posts_bad(db: AsyncSession) -> List[User]:
    """Bad: Causes N+1 queries."""
    result = await db.execute(select(User))
    users = list(result.scalars().all())
    # This will cause a query for each user's posts
    for user in users:
        _ = user.posts  # Separate query for each user
    return users

# Good: Eager loading
async def get_users_with_posts_good(db: AsyncSession) -> List[User]:
    """Good: Single query with join."""
    result = await db.execute(
        select(User)
        .options(selectinload(User.posts))
    )
    return list(result.scalars().all())

# Bulk operations
async def bulk_create_users(db: AsyncSession, users_data: List[dict]) -> List[User]:
    """Create multiple users efficiently."""
    users = [User(**data) for data in users_data]
    db.add_all(users)
    await db.flush()
    return users

# Bulk update
async def bulk_update_users(db: AsyncSession, updates: List[dict]) -> None:
    """Update multiple users efficiently."""
    await db.execute(
        update(User),
        updates  # List of dicts with id and fields to update
    )
    await db.flush()
```

```python
# src/core/database.py
engine = create_async_engine(
    settings.database_url,
    pool_size=20,           # Number of connections to maintain
    max_overflow=10,         # Additional connections beyond pool_size
    pool_pre_ping=True,      # Verify connections before using
    pool_recycle=3600,       # Recycle connections after 1 hour
    pool_timeout=30,         # Timeout for getting connection from pool
    echo_pool="debug",       # Log pool events
)
```

## Best Practices
- Use SQLAlchemy 2.0 syntax (`Mapped`, `mapped_column`)
- Always use async sessions for async operations
- Use `selectinload` or `joinedload` to avoid N+1 queries
- Implement repository pattern for data access
- Use Alembic for all schema changes
- Configure connection pooling appropriately
- Use transactions properly (commit/rollback)
- Add indexes for frequently queried columns
- Use `expire_on_commit=False` for async sessions
- Handle exceptions and rollback transactions
- Use bulk operations for multiple inserts/updates
- Add proper type hints
- Use `scalar_one_or_none()` instead of `scalar()`

## Anti-Patterns
| Anti-Pattern | Fix |
|--------------|-----|
| N+1 query problems | Use eager loading (selectinload) |
| Synchronous database calls | Use async sessions |
| Missing transactions | Use commit/rollback properly |
| No connection pooling | Configure pool_size and max_overflow |
| Hardcoded queries | Use SQLAlchemy ORM |
| Missing indexes | Add indexes for foreign keys and frequently queried columns |

## Related
- Knowledge: `knowledge/sqlalchemy-advanced.json`
- Skill: `fastapi-development` for API integration
- Skill: `python-async` for async patterns

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Packages: sqlalchemy[asyncio], asyncpg, alembic, aiosqlite, for, SQLite
> - Knowledge: sqlalchemy-advanced.json
