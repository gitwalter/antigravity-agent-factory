---
agents:
- none
category: parallel
description: REST API design (resource naming, HTTP methods, status codes), OpenAPI/Swagger
  documentation, API versioning strategies (URL, header, query), GraphQL schema design,
  gRPC proto definitions, Pagination patterns, Error response format, Rate limiting
  headers
knowledge:
- none
name: designing-apis
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Api Design

REST API design (resource naming, HTTP methods, status codes), OpenAPI/Swagger documentation, API versioning strategies (URL, header, query), GraphQL schema design, gRPC proto definitions, Pagination patterns, Error response format, Rate limiting headers

Design production-ready APIs following RESTful principles, OpenAPI standards, and best practices for versioning, pagination, and error handling.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: REST Resource Naming

Follow RESTful naming conventions:

```python
# Good: Nouns, plural, lowercase, hyphens
GET    /api/v1/users
GET    /api/v1/users/123
POST   /api/v1/users
PUT    /api/v1/users/123
DELETE /api/v1/users/123

GET    /api/v1/users/123/orders
POST   /api/v1/users/123/orders

# Bad: Verbs, mixed case, underscores
GET    /api/v1/getUsers
GET    /api/v1/GetUserById
POST   /api/v1/create_user
```

### Step 2: HTTP Methods and Status Codes

Use appropriate HTTP methods and status codes:

```python
# GET - Retrieve resources
GET /api/v1/users/123
# 200 OK - Success
# 404 Not Found - Resource doesn't exist

# POST - Create resources
POST /api/v1/users
# 201 Created - Resource created
# 400 Bad Request - Invalid input
# 409 Conflict - Resource already exists

# PUT - Update/replace resource
PUT /api/v1/users/123
# 200 OK - Updated
# 204 No Content - Updated (no body)
# 404 Not Found - Resource doesn't exist

# PATCH - Partial update
PATCH /api/v1/users/123
# 200 OK - Updated
# 404 Not Found

# DELETE - Delete resource
DELETE /api/v1/users/123
# 204 No Content - Deleted
# 404 Not Found
```

### Step 3: OpenAPI/Swagger Documentation

Document APIs with OpenAPI:

```python
# FastAPI example
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="My API",
    version="1.0.0",
    description="API documentation",
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

class UserCreate(BaseModel):
    email: str
    name: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

@app.post("/api/v1/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    """Create a new user.

    - **email**: User email address
    - **name**: User full name
    """
    return UserResponse(id=1, email=user.email, name=user.name)
```

```yaml
# OpenAPI YAML
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
paths:
  /api/v1/users:
    post:
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreate'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
components:
  schemas:
    UserCreate:
      type: object
      required:
        - email
        - name
      properties:
        email:
          type: string
          format: email
        name:
          type: string
```

### Step 4: API Versioning Strategies

Implement API versioning:

```python
# URL Versioning (Recommended)
GET /api/v1/users
GET /api/v2/users

# Header Versioning
GET /api/users
Headers: API-Version: 1.0

# Query Parameter Versioning
GET /api/users?version=1.0

# FastAPI example
from fastapi import APIRouter

v1_router = APIRouter(prefix="/api/v1", tags=["v1"])
v2_router = APIRouter(prefix="/api/v2", tags=["v2"])

@v1_router.get("/users")
async def get_users_v1():
    return {"version": "v1", "users": []}

@v2_router.get("/users")
async def get_users_v2():
    return {"version": "v2", "users": []}
```

### Step 5: Pagination Patterns

Implement pagination:

```python
# Offset-based pagination
GET /api/v1/users?page=1&limit=20

# Cursor-based pagination (better for large datasets)
GET /api/v1/users?cursor=eyJpZCI6MTIzfQ&limit=20

# Response format
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "total_pages": 5,
    "has_next": true,
    "has_prev": false
  }
}

# FastAPI example
from fastapi import Query
from typing import Optional

@app.get("/api/v1/users")
async def get_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    cursor: Optional[str] = None
):
    skip = (page - 1) * limit
    # Fetch users with skip/limit or cursor
    return {
        "data": users,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total_count,
            "has_next": skip + limit < total_count
        }
    }
```

### Step 6: Error Response Format

Standardize error responses:

```python
# Error response format
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User with ID 123 not found",
    "details": {
      "user_id": 123
    },
    "request_id": "req-123-456"
  }
}

# FastAPI example
from fastapi import HTTPException

class APIError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "request_id": request.state.request_id
            }
        }
    )
```

### Step 7: GraphQL Schema Design

Design GraphQL schemas:

```graphql
# schema.graphql
type User {
  id: ID!
  email: String!
  name: String!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
}

type Query {
  user(id: ID!): User
  users(limit: Int, offset: Int): [User!]!
  posts(userId: ID): [Post!]!
}

type Mutation {
  createUser(input: UserInput!): User!
  updateUser(id: ID!, input: UserInput!): User!
  deleteUser(id: ID!): Boolean!
}

input UserInput {
  email: String!
  name: String!
}
```

### Step 8: gRPC Proto Definitions

Define gRPC services:

```protobuf
// user.proto
syntax = "proto3";

package api.v1;

service UserService {
  rpc GetUser(GetUserRequest) returns (User);
  rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
  rpc CreateUser(CreateUserRequest) returns (User);
  rpc UpdateUser(UpdateUserRequest) returns (User);
  rpc DeleteUser(DeleteUserRequest) returns (Empty);
}

message User {
  int64 id = 1;
  string email = 2;
  string name = 3;
}

message GetUserRequest {
  int64 id = 1;
}

message ListUsersRequest {
  int32 page = 1;
  int32 limit = 2;
}

message ListUsersResponse {
  repeated User users = 1;
  int32 total = 2;
}

message CreateUserRequest {
  string email = 1;
  string name = 2;
}

message UpdateUserRequest {
  int64 id = 1;
  string email = 2;
  string name = 3;
}

message DeleteUserRequest {
  int64 id = 1;
}

message Empty {}
```

### Step 9: Rate Limiting Headers

Implement rate limiting:

```python
# Rate limit headers
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
Retry-After: 60

# FastAPI example
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/v1/users")
@limiter.limit("100/minute")
async def get_users(request: Request):
    # Add rate limit headers
    return {
        "data": [],
        "rate_limit": {
            "limit": 100,
            "remaining": 95,
            "reset": 1640995200
        }
    }
```

### Step 10: Filtering and Sorting

Implement filtering and sorting:

```python
# Query parameters
GET /api/v1/users?status=active&role=admin&sort=name&order=asc

# FastAPI example
from fastapi import Query
from typing import Optional, List

@app.get("/api/v1/users")
async def get_users(
    status: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    sort: Optional[str] = Query("id"),
    order: Optional[str] = Query("asc", regex="^(asc|desc)$")
):
    # Apply filters and sorting
    return {"users": filtered_users}
```

## Best Practices

- Use nouns for resources, verbs for actions
- Use plural nouns for collections
- Use appropriate HTTP methods
- Return proper status codes
- Document APIs with OpenAPI
- Version APIs explicitly
- Implement pagination for lists
- Standardize error responses
- Add rate limiting
- Use HTTPS in production
- Validate all inputs
- Return consistent response formats
- Include request IDs in responses
- Support filtering and sorting
- Use appropriate content types

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Verbs in URLs | Use HTTP methods |
| Inconsistent naming | Follow REST conventions |
| No versioning | Implement versioning strategy |
| No pagination | Add pagination |
| Inconsistent errors | Standardize error format |
| No rate limiting | Implement rate limiting |
| Missing documentation | Add OpenAPI docs |

## Related

- Knowledge: `{directories.knowledge}/api-design-patterns.json`
- Skill: `developing-fastapi` for FastAPI implementation
- Skill: `building-dotnet-backend` for .NET implementation

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
