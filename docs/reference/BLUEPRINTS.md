# Cursor Agent Factory Blueprints Reference

> **Philosophy:** All blueprints embody our [Culture and Values](../CULTURE_AND_VALUES.md)—love, wisdom, and care as foundations for technical decisions.

## 1. Introduction

Blueprints are pre-configured technology stacks that define the complete development environment, tooling, and AI agent system for a specific technology or domain. Each blueprint provides a standardized foundation for generating Cursor agent systems tailored to particular development needs.

All 27 blueprints share common foundations:
- **Axiom 0 (Love, Truth, and Beauty)** grounding all technical decisions
- **5-Layer Architecture** (Integrity → Purpose → Principles → Methodology → Technical)
- **Optional PM Integration** for project management support

### Blueprint JSON Schema Overview

Each blueprint follows a consistent JSON structure:

- **metadata**: Blueprint identification, version, description, and tags
- **stack**: Technology stack including primary language, frameworks, databases, and tools
- **agents**: Pre-configured AI agent patterns with customizations
- **skills**: Required and optional skills for the agent system
- **knowledge**: Reference knowledge files for domain-specific patterns
- **templates**: Code and document templates organized by category
- **workflows**: Workflow patterns for development processes
- **mcpServers**: Model Context Protocol (MCP) server integrations
- **projectStructure**: Directory and file structure definitions
- **cursorrules**: Rules and variables for agent behavior

### Blueprint Selection During Generation

During project generation, blueprints are selected based on:
1. **Technology preference**: Primary programming language and frameworks
2. **Project type**: API, web application, AI agents, or integration
3. **Team context**: Enterprise vs startup, experience level
4. **Domain requirements**: SAP, automation, data science, etc.

The factory analyzes requirements and matches them to the most appropriate blueprint, then customizes it based on additional specifications.

---

## 2. Blueprint Comparison Table

| Blueprint ID | Primary Language | Key Frameworks | Category | Complexity Level |
|--------------|------------------|----------------|----------|------------------|
| `python-fastapi` | Python | FastAPI 0.115+, SQLAlchemy 2.0+, Pydantic 2.0+ | Backend/API | Medium |
| `typescript-react` | TypeScript | React 19, Vite 5+, React Query 5+, Zustand 4+ | Frontend | Medium |
| `nextjs-fullstack` | TypeScript | Next.js 15, React 19, Prisma 5+, Tailwind CSS 3+ | Frontend/Full-Stack | High |
| `java-spring` | Java | Spring Boot 3.4, Spring Data JPA, Spring Security 6.4+ | Backend/API | High |
| `kotlin-spring` | Kotlin | Spring Boot 3.2+, Spring WebFlux 6.1+, Kotlin Coroutines 1.8+ | Backend/API | High |
| `csharp-dotnet` | C# | .NET 9, ASP.NET Core 9, EF Core 9, MediatR 12+ | Backend/API | High |
| `python-streamlit` | Python | Streamlit 1.28+, Pandas 2.0+, NumPy 1.24+ | Frontend/Full-Stack | Low-Medium |
| `ai-agent-development` | Python | LangChain 0.3+, LangGraph 0.2+, CrewAI 0.50+ | AI/Agent | High |
| `multi-agent-systems` | Python | LangGraph 0.1+, LangChain 0.2+, Multi-agent orchestration | AI/Agent | Very High |
| `python-ml-experimentation` | Python | PyTorch, scikit-learn, MLflow | AI/ML | Medium |
| `python-deep-learning` | Python | PyTorch, Transformers, PEFT | AI/ML | High |
| `python-rag-system` | Python | LangChain 0.3+, ChromaDB, OpenAI | AI/RAG | Medium-High |
| `python-multi-agent` | Python | CrewAI, AutoGen, LangGraph | AI/Agent | High |
| `python-fine-tuning` | Python | Transformers, PEFT, TRL | AI/ML | High |
| `starter-ml-classification` | Python | scikit-learn, pandas | AI/ML Starter | Low |
| `starter-chatbot` | Python | OpenAI, Streamlit | AI/LLM Starter | Low |
| `starter-rag` | Python | LangChain, ChromaDB, Streamlit | AI/RAG Starter | Low |
| `sap-abap` | ABAP | Clean ABAP, ABAP Cloud 2302+, Classic patterns | Integration | High |
| `sap-rap` | ABAP/CDS | RAP 2.x, CDS, Fiori Elements, ABAP Cloud | Integration | High |
| `sap-cap` | JavaScript/CDS | CAP 7.x, CDS, Node.js, BTP, Fiori Elements | Integration | High |
| `sap-cpi-pi` | Groovy | SAP CPI SDK 1.x, Groovy 4.0.x, Spock Framework 2.4+ | Integration | High |
| `n8n-automation` | JavaScript | n8n 1.0+, Node.js 18+, TypeScript 5+ (optional) | Integration/Automation | Medium |
| `solidity-ethereum` | Solidity | Hardhat 2.x, Foundry, OpenZeppelin 5.x | Blockchain | High |
| `defi-protocols` | Solidity | Hardhat, Foundry, Chainlink, OpenZeppelin | Blockchain/DeFi | Very High |
| `solana-rust` | Rust | Anchor 0.30+, Solana SDK 1.18+ | Blockchain | High |
| `quantitative-trading` | Python | pandas 2.x, vectorbt, backtrader, scikit-learn | Financial AI | High |
| `financial-ai-agents` | Python | LangChain 0.3+, vectorbt, pandas 2.x | Financial AI/Agent | Very High |

---

## 3. Blueprint Selection Guide

### By Language Preference

**Python Projects:**
- **REST APIs**: `python-fastapi` - Modern async API development with FastAPI
- **Quantitative Trading**: `quantitative-trading` - Algorithmic trading with backtesting
- **Financial AI Agents**: `financial-ai-agents` - AI agents for investment and trading
- **Data Applications**: `python-streamlit` - Interactive dashboards and data apps
- **AI Agents**: `ai-agent-development` - Single agent systems with LangChain
- **Multi-Agent**: `multi-agent-systems` - Coordinated multi-agent orchestration
- **ML Research**: `python-ml-experimentation` - ML experimentation with PyTorch/sklearn
- **Deep Learning**: `python-deep-learning` - Deep learning with Transformers/PEFT
- **RAG Systems**: `python-rag-system` - Production RAG with LangChain
- **Fine-Tuning**: `python-fine-tuning` - LLM fine-tuning with LoRA/PEFT
- **ML Starter**: `starter-ml-classification` - Beginner ML classification
- **Chatbot Starter**: `starter-chatbot` - Beginner LLM chatbot
- **RAG Starter**: `starter-rag` - Beginner RAG application

**TypeScript/JavaScript Projects:**
- **Frontend Only**: `typescript-react` - React 19 with modern tooling
- **Full-Stack Apps**: `nextjs-fullstack` - Next.js 15 with App Router and Server Actions
- **Automation**: `n8n-automation` - Workflow automation with n8n

**JVM Languages:**
- **Java Enterprise**: `java-spring` - Spring Boot 3.4 with Spring Modulith
- **Kotlin Reactive**: `kotlin-spring` - Reactive microservices with Spring WebFlux

**C#/.NET Projects:**
- **Enterprise APIs**: `csharp-dotnet` - .NET 9 with Clean Architecture and CQRS

**SAP Ecosystem:**
- **ABAP Development**: `sap-abap` - Clean ABAP, ABAP Cloud, classic patterns
- **RAP Development**: `sap-rap` - RESTful ABAP Programming, CDS, Fiori Elements
- **CAP Development**: `sap-cap` - Cloud Application Programming Model, Node.js/Java, BTP
- **Integration Flows**: `sap-cpi-pi` - CPI/PI iFlows with Groovy scripting

### By Project Type

**REST APIs**: `python-fastapi`, `java-spring`, `kotlin-spring`, `csharp-dotnet`

**Web Applications**: `typescript-react`, `nextjs-fullstack`, `python-streamlit`

**AI Agent Systems**: `ai-agent-development`, `multi-agent-systems`, `financial-ai-agents`

**Blockchain**: `solidity-ethereum`, `defi-protocols`, `solana-rust`

**Financial AI/Trading**: `quantitative-trading`, `financial-ai-agents`

**Integration/Automation**: `sap-abap`, `sap-cpi-pi`, `n8n-automation`

### By Team Experience Level

**Beginner-Friendly**: `python-streamlit`, `python-fastapi`, `typescript-react`

**Intermediate**: `nextjs-fullstack`, `n8n-automation`, `ai-agent-development`

**Advanced**: `java-spring`, `kotlin-spring`, `csharp-dotnet`, `multi-agent-systems`, `sap-abap`, `sap-cpi-pi`

### By Enterprise vs Startup Context

**Enterprise**: `java-spring`, `csharp-dotnet`, `sap-abap`, `sap-cpi-pi`

**Startup/Modern**: `python-fastapi`, `nextjs-fullstack`, `typescript-react`, `ai-agent-development`

---

## 4. Blueprint Categories

### Backend/API Blueprints
- **python-fastapi**: REST API development with Python and FastAPI
- **java-spring**: Enterprise applications with Java and Spring Boot 3.4
- **kotlin-spring**: Reactive microservices with Kotlin and Spring WebFlux
- **csharp-dotnet**: Enterprise APIs with .NET 9 and Clean Architecture

### Frontend/Full-Stack Blueprints
- **typescript-react**: Web applications with TypeScript and React 19
- **nextjs-fullstack**: Full-stack TypeScript with Next.js 15 App Router
- **python-streamlit**: Data applications and dashboards with Streamlit

### AI/Agent Blueprints
- **ai-agent-development**: AI agent systems with LangChain, LangGraph, and CrewAI
- **multi-agent-systems**: Orchestrated multi-agent systems with coordination patterns
- **python-multi-agent**: Multi-agent systems with CrewAI, AutoGen, and LangGraph
- **python-rag-system**: Production RAG systems with LangChain and vector databases

### AI/ML Blueprints
- **python-ml-experimentation**: ML research with PyTorch, scikit-learn, and MLflow
- **python-deep-learning**: Deep learning with Hugging Face Transformers and PEFT
- **python-fine-tuning**: LLM fine-tuning with LoRA, QLoRA, and TRL

### AI Starter Blueprints (Onboarding)
- **starter-ml-classification**: Beginner-friendly ML classification project
- **starter-chatbot**: Simple LLM chatbot with OpenAI and Streamlit
- **starter-rag**: Simple RAG application with LangChain and ChromaDB

### Integration/Automation Blueprints
- **sap-abap**: SAP ABAP development with RAP, CAP, and Fiori integration
- **sap-cpi-pi**: SAP CPI/PI integration flows with Groovy scripting
- **n8n-automation**: Workflow automation with n8n and AI integrations

### Blockchain Blueprints
- **solidity-ethereum**: Ethereum smart contract development with Hardhat and Foundry
- **defi-protocols**: DeFi protocol development (AMMs, lending, staking)
- **solana-rust**: Solana program development with Anchor framework

### Financial AI Blueprints
- **quantitative-trading**: Algorithmic trading with backtesting and risk management
- **financial-ai-agents**: AI agents for investment analysis and trading

---

## 5. Detailed Blueprint Sections

### 5.1 Python FastAPI Blueprint

**Blueprint ID**: `python-fastapi`  
**Version**: 1.0.0  
**Description**: REST API development with Python and FastAPI  
**Tags**: python, api, rest, fastapi, backend

#### Use Cases

**Ideal Scenarios:**
- Building modern REST APIs with async support
- Microservices architecture
- API-first development approach
- High-performance API endpoints

**Example Projects:**
- E-commerce API backends
- SaaS platform APIs
- Data processing APIs
- Integration service APIs

**When NOT to Use:**
- Simple CRUD applications (consider Django)
- Applications requiring heavy server-side rendering
- Projects requiring extensive admin interfaces

#### Technology Stack

**Primary Language**: Python  
**Frameworks**:
- FastAPI 0.115+ - Modern async web framework
- SQLAlchemy 2.0+ - ORM for database operations
- Pydantic 2.0+ - Data validation and serialization
- Alembic 1.12+ - Database migrations

**Databases**: PostgreSQL (primary), SQLite (development/testing)

**Tools**: pytest (testing), ruff (linting), black (formatting), mypy (type checking)

**Style Guides**: PEP 8, Google Python Style

#### Cursor Agent System

**Included Agents**:
- `code-reviewer` (required) - Code review with clean-code-review and grounding skills
- `test-generator` (required) - Test generation with TDD skills
- `explorer` (optional) - Code exploration

**Included Skills**:
- bugfix-workflow, feature-workflow, grounding, tdd, code-templates

**Knowledge Files**:
- naming-conventions.json, fastapi-patterns.json, test-patterns.json, tdd-patterns.json

#### Project Structure

**Key Directories**: `.cursor/agents/`, `.cursor/skills/`, `knowledge/`, `src/`, `tests/`, `workflows/`

**Key Files**: `.cursorrules`, `README.md`, `pyproject.toml`, `requirements.txt`

#### Key Rules

- Always use type hints for function parameters and returns
- Use Google-style docstrings
- Write pytest tests with fixtures
- Follow PEP 8 or Google style guide

#### MCP Integrations

- **atlassian** (optional): Jira/Confluence integration
- **deepwiki** (optional): GitHub analysis

#### Layer Defaults

No specific axiom alignment defaults defined.

---

### 5.2 TypeScript React Blueprint

**Blueprint ID**: `typescript-react`  
**Version**: 1.0.0  
**Description**: Web application development with TypeScript and React  
**Tags**: typescript, react, frontend, web

#### Use Cases

**Ideal Scenarios:**
- Modern single-page applications
- Component-based UI development
- Applications requiring rich interactivity
- Progressive web applications

**Example Projects:**
- Admin dashboards
- Data visualization interfaces
- E-commerce frontends
- Content management interfaces

**When NOT to Use:**
- Server-side rendering requirements (use Next.js)
- Simple static sites (use plain HTML/CSS)
- Applications requiring SEO optimization

#### Technology Stack

**Primary Language**: TypeScript  
**Frameworks**:
- React 19 - UI framework with latest features
- Vite 5+ - Fast build tool
- React Query 5+ - Data fetching and caching
- Zustand 4+ - Lightweight state management

**Tools**: TypeScript 5.6+, vitest (testing), eslint (linting), prettier (formatting)

**Style Guides**: Airbnb JavaScript Style, React Best Practices

#### Cursor Agent System

**Included Agents**:
- `code-reviewer` (required)
- `test-generator` (required)
- `explorer` (optional)

**Included Skills**:
- bugfix-workflow, feature-workflow, tdd, code-templates

**Knowledge Files**:
- naming-conventions.json, component-patterns.json, test-patterns.json

#### Project Structure

**Key Directories**: `src/components/`, `src/hooks/`, `src/services/`, `src/types/`, `tests/`

**Key Files**: `.cursorrules`, `package.json`, `tsconfig.json`

#### Key Rules

- Use strict TypeScript mode with no any types
- Use React 19 features including Actions, useOptimistic, and useFormStatus
- Prefer functional components with hooks
- Write Vitest unit tests with React Testing Library

#### MCP Integrations

- **atlassian** (optional): Jira/Confluence
- **deepwiki** (optional): GitHub analysis

---

### 5.3 Next.js Full-Stack Blueprint

**Blueprint ID**: `nextjs-fullstack`  
**Version**: 1.0.0  
**Description**: Full-stack TypeScript development with Next.js 15 App Router, Server Actions, and React Server Components  
**Tags**: typescript, nextjs, react, fullstack, frontend, backend

#### Use Cases

**Ideal Scenarios:**
- Full-stack web applications requiring SEO
- Applications needing server-side rendering
- Projects requiring both frontend and backend
- Modern web applications with API routes

**Example Projects:**
- E-commerce platforms
- Content management systems
- SaaS applications
- Marketing websites with dynamic content

**When NOT to Use:**
- Pure API backends (use FastAPI or Express)
- Simple static sites
- Applications not requiring SSR

#### Technology Stack

**Primary Language**: TypeScript  
**Frameworks**:
- Next.js 15 - Full-stack framework with App Router
- React 19 - UI library
- Tailwind CSS 3+ - Utility-first styling
- Prisma 5+ - Next-generation ORM
- tRPC 11+ (optional) - Type-safe APIs
- Zod 3+ - Schema validation

**Databases**: PostgreSQL (primary), SQLite (development/testing)

**Tools**: TypeScript 5+, ESLint, Prettier, Vitest (unit testing), Playwright (E2E testing)

**Style Guides**: Airbnb JavaScript/TypeScript Style, Next.js Best Practices

#### Cursor Agent System

**Included Agents**:
- `code-reviewer` (required) - With clean-code-review and grounding
- `test-generator` (required) - With TDD skills
- `documentation-agent` (optional)
- `explorer` (optional)

**Included Skills**:
- bugfix-workflow, feature-workflow, grounding, tdd, code-templates, security-audit (optional), code-review (optional)

**Knowledge Files**:
- naming-conventions.json, component-patterns.json, nextjs-patterns.json, test-patterns.json

#### Project Structure

**Key Directories**: `src/app/` (App Router pages), `src/components/`, `src/lib/`, `src/server/`, `prisma/`, `tests/`

**Key Files**: `.cursorrules`, `package.json`, `tsconfig.json`, `next.config.js`, `tailwind.config.ts`, `prisma/schema.prisma`

#### Key Rules

- Use strict TypeScript mode with no any types
- Prefer React Server Components by default, use 'use client' only when needed
- Use Server Actions for mutations instead of API routes
- Use Next.js 15 App Router with route groups and parallel routes
- Validate all inputs with Zod schemas
- Write Vitest unit tests and Playwright E2E tests

#### MCP Integrations

- **atlassian** (optional): Jira/Confluence
- **deepwiki** (optional): GitHub analysis
- **notion** (optional): Notion documentation

---

### 5.4 Java Spring Boot Blueprint

**Blueprint ID**: `java-spring`  
**Version**: 1.0.0  
**Description**: Enterprise application development with Java, Spring Boot 3.4, and Spring Modulith  
**Tags**: java, spring, backend, enterprise

#### Use Cases

**Ideal Scenarios:**
- Enterprise-grade applications
- Large-scale microservices
- Applications requiring Spring ecosystem
- Projects needing modular monolith architecture

**Example Projects:**
- Enterprise resource planning systems
- Financial services applications
- Healthcare information systems
- Government applications

**When NOT to Use:**
- Simple CRUD applications
- Rapid prototyping projects
- Applications not requiring enterprise features

#### Technology Stack

**Primary Language**: Java  
**Frameworks**:
- Spring Boot 3.4 - Application framework
- Spring Data JPA 3.4 - Data access layer
- Spring Security 6.4+ - Security framework
- Spring Web 6.1+ - REST API support
- Spring Modulith 1.2+ (optional) - Modular monolith architecture

**Databases**: PostgreSQL (primary), H2 (testing)

**Tools**: JUnit 5 (testing), Mockito (mocking), Maven/Gradle (build), Checkstyle (linting)

**Style Guides**: Google Java Style Guide

#### Cursor Agent System

**Included Agents**:
- `code-reviewer` (required)
- `test-generator` (required)
- `explorer` (optional)

**Included Skills**:
- bugfix-workflow, feature-workflow, grounding, tdd, code-templates

**Knowledge Files**:
- naming-conventions.json, spring-patterns.json, test-patterns.json

#### Project Structure

**Key Directories**: `src/main/java/`, `src/main/resources/`, `src/test/java/`

**Key Files**: `.cursorrules`, `pom.xml` (Maven) or `build.gradle` (Gradle)

#### Key Rules

- Use Spring Boot 3.4 with Java 21+ features
- Consider Spring Modulith for modular monolith architecture
- Use constructor injection, avoid field injection
- Use @RestController with @RequestMapping for REST APIs
- Business logic in @Service classes
- Use Spring Data JPA repositories
- Write JUnit 5 tests with @SpringBootTest for integration tests

#### MCP Integrations

- **atlassian** (optional): Jira/Confluence
- **deepwiki** (optional): GitHub analysis

---

### 5.5 Kotlin Spring Boot Blueprint

**Blueprint ID**: `kotlin-spring`  
**Version**: 1.0.0  
**Description**: Modern microservice development with Kotlin, Spring Boot 3, and reactive programming  
**Tags**: kotlin, spring, spring-boot, reactive, microservice, jvm, coroutines

#### Use Cases

**Ideal Scenarios:**
- High-performance reactive microservices
- Applications requiring non-blocking I/O
- Modern JVM development with Kotlin
- Event-driven architectures

**Example Projects:**
- Real-time data processing services
- High-throughput API gateways
- Event streaming applications
- IoT backend services

**When NOT to Use:**
- Traditional request-response applications
- Teams unfamiliar with reactive programming
- Simple CRUD applications

#### Technology Stack

**Primary Language**: Kotlin  
**Frameworks**:
- Spring Boot 3.2+ - Application framework
- Spring WebFlux 6.1+ - Reactive web framework
- Spring Data R2DBC 3.2+ - Reactive data access
- Kotlin 2.0 - Programming language
- Kotlin Coroutines 1.8+ - Async programming
- Arrow 1.2+ (optional) - Functional programming

**Databases**: PostgreSQL (primary, R2DBC), H2 (testing, R2DBC)

**Tools**: JUnit 5, Kotest (Kotlin-native testing), MockK (Kotlin mocking), ktlint (linting), Detekt (static analysis), Gradle Kotlin DSL

**Style Guides**: Kotlin Official Style Guide, Spring Kotlin Best Practices

#### Cursor Agent System

**Included Agents**:
- `code-reviewer` (required) - With kotlin-idioms and grounding
- `test-generator` (required) - With TDD and Kotest skills
- `documentation-agent` (optional)
- `explorer` (optional)

**Included Skills**:
- bugfix-workflow, feature-workflow, grounding, tdd, code-templates

**Knowledge Files**:
- kotlin-idioms.json, spring-kotlin-patterns.json, coroutines-patterns.json, reactive-patterns.json, kotest-patterns.json

#### Project Structure

**Key Directories**: `src/main/kotlin/` (with controller/, service/, repository/, model/, dto/, config/), `src/test/kotlin/`

**Key Files**: `.cursorrules`, `build.gradle.kts`, `settings.gradle.kts`, `application.yml`

#### Key Rules

- Use Kotlin 2.0 language features
- Leverage Kotlin null safety, avoid platform types
- Use data classes for DTOs and value objects
- Use extension functions for utility methods
- Use suspend functions and coroutines for async operations
- Prefer val over var, immutable collections
- Use expression bodies for simple functions
- Write Kotest tests with descriptive specs

#### MCP Integrations

- **deepwiki** (optional): GitHub analysis
- **atlassian** (optional): Jira/Confluence

---

### 5.6 C# .NET Blueprint

**Blueprint ID**: `csharp-dotnet`  
**Version**: 1.0.0  
**Description**: Enterprise API and web development with .NET 9, ASP.NET Core, Clean Architecture, CQRS, MediatR, and FluentValidation  
**Tags**: csharp, dotnet, aspnet, api, enterprise, backend

#### Use Cases

**Ideal Scenarios:**
- Enterprise .NET applications
- Applications requiring Clean Architecture
- CQRS pattern implementations
- Microsoft ecosystem integration

**Example Projects:**
- Enterprise APIs
- Microservices architectures
- Azure cloud applications
- Windows-based enterprise systems

**When NOT to Use:**
- Simple web applications
- Rapid prototyping
- Non-Microsoft environments

#### Technology Stack

**Primary Language**: C#  
**Frameworks**:
- .NET 9 - Runtime and framework
- ASP.NET Core 9 - Web framework
- Entity Framework Core 9 - ORM
- FluentValidation 11+ - Validation framework
- MediatR 12+ - CQRS/Mediator pattern
- AutoMapper 12+ (optional) - Object mapping

**Databases**: SQL Server (primary), PostgreSQL (alternative), SQLite (development/testing)

**Tools**: xUnit (unit testing), NSubstitute (mocking), FluentAssertions (test assertions), dotnet-format (formatting), SonarAnalyzer (static analysis)

**Style Guides**: Microsoft C# Coding Conventions, Clean Architecture patterns

#### Cursor Agent System

**Included Agents**:
- `code-reviewer` (required) - With clean-code-review and grounding
- `test-generator` (required) - With TDD skills
- `documentation-agent` (optional)
- `explorer` (optional)

**Included Skills**:
- bugfix-workflow, feature-workflow, grounding, tdd, code-templates, security-audit (optional), code-review (optional)

**Knowledge Files**:
- naming-conventions.json, dotnet-patterns.json, test-patterns.json

#### Project Structure

**Key Directories**: `src/Api/`, `src/Application/`, `src/Domain/`, `src/Infrastructure/`, `tests/Unit/`, `tests/Integration/`

**Key Files**: `.cursorrules`, `Solution.sln`, `src/Api/Api.csproj`, `src/Api/Program.cs`, `src/Api/appsettings.json`

#### Key Rules

- Enable nullable reference types, no null warnings
- Follow Clean Architecture layers: Domain, Application, Infrastructure, WebApi
- Use CQRS with MediatR - separate Commands and Queries
- Validate all Commands and Queries with FluentValidation validators
- Use constructor injection, register services in Program.cs
- Use repository pattern in Infrastructure layer
- Write xUnit tests with NSubstitute mocks and FluentAssertions

#### MCP Integrations

- **atlassian** (optional): Jira/Confluence
- **deepwiki** (optional): GitHub analysis

---

### 5.7 Python Streamlit Blueprint

**Blueprint ID**: `python-streamlit`  
**Version**: 1.0.0  
**Description**: Data applications and dashboards with Python and Streamlit  
**Tags**: python, streamlit, data-science, dashboard, visualization, ml

#### Use Cases

**Ideal Scenarios:**
- Data science dashboards
- Interactive data visualization
- Machine learning model interfaces
- Rapid prototyping of data applications

**Example Projects**:
- Analytics dashboards
- ML model demos
- Data exploration tools
- Internal reporting tools

**When NOT to Use:**
- Production web applications requiring custom UI
- Applications needing complex routing
- High-traffic public-facing applications

#### Technology Stack

**Primary Language**: Python  
**Frameworks**:
- Streamlit 1.28+ - Web app framework
- Pandas 2.0+ - Data manipulation
- NumPy 1.24+ - Numerical computing
- Plotly 5.17+ (optional) - Interactive visualizations
- scikit-learn 1.3+ (optional) - Machine learning
- LangChain 0.1+ (optional) - AI agent integration

**Databases**: SQLite (local), PostgreSQL (production, optional), MongoDB (document storage, optional)

**Tools**: pytest (testing), ruff (linting), black (formatting), mypy (type checking), streamlit-authenticator (authentication, optional)

**Style Guides**: PEP 8, Google Python Style

#### Cursor Agent System

**Included Agents**:
- `code-reviewer` (required) - With clean-code-review and grounding
- `test-generator` (required) - With TDD skills

**Included Skills**:
- bugfix-workflow, feature-workflow, grounding, tdd, code-templates

**Knowledge Files**:
- naming-conventions.json, streamlit-patterns.json, test-patterns.json, tdd-patterns.json

#### Project Structure

**Key Directories**: `pages/` (multi-page apps), `components/` (reusable components), `utils/`, `data/`, `models/` (ML models, optional)

**Key Files**: `.cursorrules`, `app.py` (main entry point), `pyproject.toml`, `requirements.txt`, `.streamlit/config.toml` (optional)

#### Key Rules

- Always use type hints for function parameters and returns
- Use Google-style docstrings
- Initialize session state early and use descriptive keys
- Use @st.cache_data for data and @st.cache_resource for resources
- Organize code into pages/, components/, and utils/ directories
- Use pages/ directory for multi-page Streamlit applications
- Write pytest tests with fixtures for Streamlit components
- Handle errors gracefully with try-except blocks

#### MCP Integrations

- **atlassian** (optional): Jira/Confluence
- **deepwiki** (optional): GitHub analysis

---

### 5.8 AI Agent Development Blueprint

**Blueprint ID**: `ai-agent-development`  
**Version**: 1.0.0  
**Description**: Build AI agent systems with LangChain, LangGraph, and modern LLM frameworks  
**Tags**: python, ai, agents, langchain, langgraph, llm, ml  
**Purpose**: Enable developers to create intelligent, coordinated AI agent systems that serve users with integrity

#### Use Cases

**Ideal Scenarios:**
- Building single AI agents with tools
- RAG (Retrieval-Augmented Generation) applications
- Conversational AI systems
- Task automation with AI

**Example Projects**:
- Customer support chatbots
- Research assistants
- Code generation tools
- Document analysis agents

**When NOT to Use:**
- Simple prompt-based applications
- Applications not requiring agent coordination
- Projects without LLM integration needs

#### Technology Stack

**Primary Language**: Python  
**Frameworks**:
- LangChain 0.3+ - Agent framework and chains
- LangGraph 0.2+ - Stateful agent orchestration
- CrewAI 0.50+ - Multi-agent crew orchestration
- AutoGen 0.2+ - Conversational multi-agent systems
- Streamlit 1.30+ - Interactive UI
- FastAPI 0.100+ - API endpoints
- Pydantic 2.0+ - Data validation and structured outputs

**Databases**: ChromaDB/FAISS (vector stores), SQLite (prompt/state storage), PostgreSQL (production)

**LLM Providers**: OpenAI (GPT-4, GPT-4-turbo, GPT-4o), Anthropic (Claude 3), Google (Gemini), Ollama (local)

**Tools**: pytest, ruff, mypy, langsmith (agent tracing), poetry (dependency management)

**Style Guides**: PEP 8, Google Python Style

#### Cursor Agent System

**Included Agents**:
- `code-reviewer` (required) - With clean-code-review and grounding
- `test-generator` (required) - With TDD skills
- `documentation-agent` (required) - Focused on agent-documentation
- `explorer` (optional) - Focused on research-papers

**Included Skills**:
- prompt-engineering, agent-coordination, grounding, tdd, bugfix-workflow, feature-workflow

**Knowledge Files**:
- langchain-patterns.json, langgraph-workflows.json, crewai-patterns.json, autogen-patterns.json, mcp-patterns.json, agent-testing.json, prompt-engineering.json, agent-coordination.json, llm-providers.json

#### Project Structure

**Key Directories**: `agents/` (implementations), `agents/core/`, `agents/specialized/`, `prompts/` (templates and system prompts), `workflow/` (LangGraph workflows), `tools/`, `knowledge/`, `apps/` (Streamlit), `api/` (FastAPI), `tests/agents/`, `tests/prompts/`

**Key Files**: `.cursorrules`, `PURPOSE.md`, `pyproject.toml`, `workflows/methodology.yaml`

#### Key Rules

- Always use type hints for function parameters and returns
- Use Google-style docstrings for all public functions
- Use Pydantic models for LLM structured outputs
- Implement proper error handling with fallbacks
- Add LangSmith tracing to all agent operations

#### MCP Integrations

- **deepwiki** (required): GitHub analysis
- **atlassian** (optional): Jira/Confluence

#### Layer Defaults

**Layer 0**: Core axioms A1-A5, optional A10 (Learning)  
**Layer 1**: Purpose template for intelligent AI agents serving users with integrity  
**Layer 3**: Research-development methodology (70/30 exploration/exploitation)

**Axiom Alignment**:
- A1: All agent outputs include reasoning traces via LangSmith
- A2: Agents always confirm before taking consequential actions
- A3: Agent decisions are explainable through prompt inspection
- A4: Agents refuse harmful requests and validate safety constraints
- A5: Agent behavior derives from documented prompts and rules
- A10: Feedback loops improve agent performance over time

---

### 5.9 Multi-Agent Systems Blueprint

**Blueprint ID**: `multi-agent-systems`  
**Version**: 1.0.0  
**Description**: Build orchestrated multi-agent systems with LangGraph, supervisor patterns, and agent coordination  
**Tags**: python, ai, agents, multi-agent, langgraph, orchestration, coordination  
**Purpose**: Enable developers to create coordinated multi-agent systems that collaborate effectively with integrity

#### Use Cases

**Ideal Scenarios:**
- Complex tasks requiring multiple specialized agents
- Research and analysis workflows
- Multi-step problem solving
- Distributed agent coordination

**Example Projects**:
- Research assistant systems
- Code review and generation teams
- Content creation pipelines
- Complex decision-making systems

**When NOT to Use:**
- Simple single-agent tasks
- Applications not requiring coordination
- Projects with limited complexity

#### Technology Stack

**Primary Language**: Python  
**Frameworks**:
- LangGraph 0.1+ - Multi-agent orchestration and state machines
- LangChain 0.2+ - Agent framework and tools
- Streamlit 1.30+ - Interactive UI and debugging
- FastAPI 0.100+ - API endpoints for agent access
- Pydantic 2.0+ - Structured state and messages

**Databases**: ChromaDB (shared knowledge base), SQLite (agent state persistence), PostgreSQL (production state storage)

**LLM Providers**: OpenAI (GPT-4 for supervisor, GPT-3.5-turbo for workers), Anthropic (Claude 3 for long-context)

**Tools**: pytest, ruff, mypy, langsmith (multi-agent tracing), poetry

**Style Guides**: PEP 8, Google Python Style

#### Cursor Agent System

**Included Agents**:
- `code-reviewer` (required) - With agent-coordination and grounding
- `test-generator` (required) - With TDD skills
- `documentation-agent` (required) - Focused on multi-agent-architecture
- `explorer` (required) - Focused on multi-agent-patterns

**Included Skills**:
- agent-coordination, task-decomposition, consensus-building, prompt-engineering, grounding, tdd, bugfix-workflow (optional), feature-workflow (optional)

**Knowledge Files**:
- multi-agent-coordination.json, mcp-patterns.json, multi-agent-patterns.json, agent-handoffs.json, coordination-strategies.json, langgraph-workflows.json, langchain-patterns.json, crewai-patterns.json, autogen-patterns.json, agent-testing.json, prompt-engineering.json

#### Project Structure

**Key Directories**: `agents/supervisor/`, `agents/workers/`, `agents/shared/`, `graphs/` (LangGraph multi-agent graphs), `state/`, `prompts/supervisor/`, `prompts/workers/`, `tools/`, `coordination/`, `knowledge/`, `tests/graphs/`, `tests/coordination/`

**Key Files**: `.cursorrules`, `PURPOSE.md`, `pyproject.toml`, `workflows/methodology.yaml`, `enforcement.yaml`, `practices.yaml`

#### Key Rules

- Always use type hints for function parameters and returns
- Use Google-style docstrings for all agents and handlers
- All agent state must use Pydantic models
- Implement proper error handling with fallbacks
- Add LangSmith tracing to all agent operations
- All handoffs must include state and context

#### MCP Integrations

- **deepwiki** (required): Research multi-agent patterns
- **atlassian** (optional): Jira/Confluence

#### Multi-Agent Patterns

**Supervisor/Worker**: Central supervisor delegates tasks to specialized workers  
**Hierarchical**: Multi-level coordination with team leads and specialists  
**Collaborative**: Peer agents collaborate through consensus  
**Sequential**: Agents process in sequence, each building on previous output  
**Distributed**: Agents distributed across services with MCP-based communication

#### Layer Defaults

**Layer 0**: Core axioms A1-A5, optional A8 (Collaboration) and A10 (Learning)  
**Layer 1**: Purpose template for coordinated multi-agent systems  
**Layer 3**: Research-development methodology (70/30 exploration/exploitation)

**Axiom Alignment**:
- A1: All agent outputs include reasoning traces via LangSmith
- A2: Supervisor confirms before consequential actions
- A3: Agent coordination decisions are explainable
- A4: Agents refuse harmful requests and validate safety constraints
- A5: All agents follow documented prompts and coordination protocols
- A8: Agents work together effectively with clear handoff protocols
- A10: System improves through feedback and coordination refinement

---

### 5.10 SAP ABAP Blueprint

**Blueprint ID**: `sap-abap`  
**Version**: 2.0.0  
**Description**: SAP ABAP development with RAP, CAP, ABAP Cloud, and Fiori integration  
**Tags**: sap, abap, rap, cap, abap-cloud, fiori, btp, enterprise  
**Reference**: https://github.com/fielmann-ag/cursor-sap-development-workflow

#### Use Cases

**Ideal Scenarios:**
- SAP S/4HANA custom development
- Fiori application development
- RAP (RESTful Application Programming) applications
- CAP (Cloud Application Programming) projects
- ABAP Cloud development

**Example Projects**:
- Custom SAP business applications
- Fiori Elements applications
- RAP-based OData services
- CAP-based cloud applications

**When NOT to Use:**
- Non-SAP environments
- Applications not requiring SAP integration
- Projects outside SAP ecosystem

#### Technology Stack

**Primary Language**: ABAP  
**Secondary Languages**: CDS, JavaScript, TypeScript  
**Frameworks**:
- RAP 2.x - RESTful Application Programming
- CAP 7.x - Cloud Application Programming
- ABAP Cloud 2302+ - Cloud-compatible ABAP development
- Fiori Elements 1.x - UI5-based Fiori applications

**Tools**: ABAP Unit (testing), abaplint (linting), Eclipse ADT (IDE), SAP Business Application Studio, MTA Build Tool

**Style Guides**: SAP Clean ABAP (required), Hungarian Notation (optional)

#### Cursor Agent System

**Included Agents**:
- `code-reviewer` (required) - With clean-code-review and sap-grounding skills
- `test-generator` (required) - With tdd-abap skills
- `explorer` (required) - Named explorer-sap

**Included Skills**:
- sap-bugfix, sap-feature, sap-grounding, tdd-abap, code-templates, cap-development (optional)

**Knowledge Files**:
- sap-cap-patterns.json (required), naming-conventions.json, cdhdr-object-classes.json, common-table-patterns.json, tadir-object-types.json, service-class-catalog.json, sap-reference-repos.json

#### Project Structure

**Key Directories**: `templates/abap/clean-abap/`, `templates/abap/hungarian/`, `templates/cap/`, `templates/prompts/`, `src/`, `docs/`, `diagrams/`

**Key Files**: `.cursorrules`, `README.md`

#### Key Rules

- ALWAYS verify SAP table structures and CDS views before implementation using MCP SAP documentation
- Ask for style guide at project start, default to Clean ABAP
- Auto-fetch Jira/Confluence when mentioned, use SAP documentation MCP for ABAP/RAP/CAP/Fiori questions
- Follow RAP behavior definition patterns, use draft handling for complex scenarios
- Separate base views from projection views in CDS, use aspects for reusable fields
- When ABAP_CLOUD_MODE is enabled, only use released APIs
- Write ABAP Unit tests for all business logic using Given-When-Then pattern
- Always use exception classes, never use MESSAGE without exception

#### MCP Integrations

- **atlassian** (required): Jira/Confluence integration
- **sap-documentation** (required): SAP Help Portal, ABAP, RAP, CAP, Fiori documentation
- **deepwiki** (required): SAP sample repositories and documentation
- **sequentialthinking** (optional): Complex analysis and problem-solving

#### Enforcement Patterns

- clean-abap-enforcement (required)
- abap-cloud-compliance (optional)
- rap-pattern-compliance (required)
- cds-best-practices (required)
- abap-unit-coverage (required)

---

### 5.11 SAP CPI/PI Integration Blueprint

**Blueprint ID**: `sap-cpi-pi`  
**Version**: 2.0.0  
**Description**: SAP Cloud Platform Integration and Process Integration development with Groovy scripts, Java adapters, and iFlow patterns  
**Tags**: sap, cpi, pi, integration, groovy, java, iflow, b2b, edi  
**Purpose**: Enable SAP integration developers to build robust iFlows with proper patterns, error handling, and testing

#### Use Cases

**Ideal Scenarios:**
- SAP Integration Suite (Cloud) development
- SAP PI/PO (on-premise) integration flows
- B2B/EDI integrations
- API-based integrations
- Event-driven integrations

**Example Projects**:
- SAP to SAP integrations
- SAP to third-party system integrations
- EDI message processing
- IDoc processing
- SOAP/REST service integrations

**When NOT to Use:**
- Non-SAP integration scenarios
- Applications not requiring SAP Integration Suite
- Projects outside SAP integration ecosystem

#### Technology Stack

**Primary Language**: Groovy 4.0.x  
**Secondary Language**: Java  
**Frameworks**:
- SAP CPI Groovy SDK 1.x - Cloud Platform Integration scripting
- SAP PI Adapter Framework 7.5+ - On-premise adapter development
- Apache Camel (underlying) - Integration framework foundation
- Spock Framework 2.4+ - Groovy testing framework

**Platforms**: SAP Integration Suite (cloud), SAP CPI (cloud), SAP PI/PO (on-premise)

**Protocols**: REST/OData, SOAP, IDoc, SFTP/AS2, EDIFACT/X12, AMQP/Kafka

**Tools**: Eclipse (PI development), IntelliJ IDEA, SAP CPI Web IDE, Postman, SoapUI, Spock Framework

**Style Guides**: Groovy Style Guide, SAP CPI Best Practices

#### Cursor Agent System

**Included Agents**:
- `code-reviewer` (required) - With groovy-scripting and grounding, focus on CPI patterns and error handling
- `test-generator` (required) - With TDD, focus on Groovy script tests
- `documentation-agent` (optional) - Focus on iFlow documentation

**Included Skills**:
- iflow-development, groovy-scripting, error-handling, b2b-integration (optional), grounding, tdd, bugfix-workflow, feature-workflow

**Knowledge Files**:
- groovy-patterns.json (required), iflow-patterns.json (required), sap-cap-patterns.json (optional), cpi-error-handling.json, mapping-patterns.json, b2b-patterns.json, security-patterns.json

#### Project Structure

**Key Directories**: `src/main/groovy/scripts/`, `src/main/groovy/mappings/`, `src/main/java/adapters/`, `src/test/groovy/`, `iflows/`, `docs/`

**Key Files**: `.cursorrules`, `PURPOSE.md`, `build.gradle`

#### Key Rules

- Use Groovy 4.x features like sealed classes, switch expressions, and improved null safety
- Use Groovy safe navigation (?.) and elvis operator (?:) for null handling
- Use messageLog for CPI logging, never System.out.println
- Always use try-catch with proper exception routing, set error properties
- Use message properties/headers, not hardcoded values
- Write Spock tests for all scripts using Given-When-Then blocks
- Never hardcode credentials, use Secure Parameters
- Follow iFlow design patterns: exception subprocesses, retry logic, proper timeouts
- Use SAP documentation MCP server for CPI/PI questions
- Handle large messages efficiently, use streaming for large payloads

#### MCP Integrations

- **sap-documentation** (required): SAP Help Portal, CPI/PI documentation, Groovy patterns, iFlow best practices
- **atlassian** (optional): Jira/Confluence integration
- **deepwiki** (optional): SAP sample repositories

#### Groovy Patterns

- **messageAccess**: Accessing message body and properties
- **xmlParsing**: XML parsing with XmlSlurper
- **jsonParsing**: JSON parsing with JsonSlurper
- **logging**: Proper CPI logging patterns
- **errorHandling**: Exception handling patterns

#### Layer Defaults

**Layer 0**: Core axioms A1-A5, optional A6 (Minimalism) and A7 (Reversibility)  
**Layer 1**: Purpose template for reliable SAP integrations  
**Layer 3**: Kanban methodology (interrupt-driven integration support work)

---

### 5.12 n8n Automation Blueprint

**Blueprint ID**: `n8n-automation`  
**Version**: 1.0.0  
**Description**: Workflow automation with n8n, JavaScript/TypeScript, and AI agent integrations  
**Tags**: n8n, automation, workflow, javascript, typescript, ai, integration

#### Use Cases

**Ideal Scenarios:**
- Workflow automation
- Integration between multiple services
- Business process automation
- AI-powered workflows

**Example Projects**:
- Marketing automation workflows
- Data synchronization workflows
- Notification systems
- AI agent orchestration workflows

**When NOT to Use:**
- Complex application development
- Applications requiring custom UI
- Projects not requiring workflow automation

#### Technology Stack

**Primary Language**: JavaScript  
**Frameworks**:
- n8n 1.0+ - Workflow automation platform
- Node.js 18+ - Runtime environment
- TypeScript 5+ (optional) - Type system
- LangChain 0.1+ (optional) - AI agent orchestration

**Databases**: PostgreSQL (n8n workflow storage), SQLite (development/testing, optional)

**Tools**: ESLint (linting), Prettier (formatting), Jest (testing, optional), n8n-testing (workflow testing, optional)

**Style Guides**: Airbnb JavaScript Style, n8n Best Practices

#### Cursor Agent System

**Included Agents**:
- `code-reviewer` (required) - With clean-code-review and grounding
- `test-generator` (optional) - With TDD skills

**Included Skills**:
- bugfix-workflow, feature-workflow, grounding, code-templates

**Knowledge Files**:
- naming-conventions.json, n8n-patterns.json, langchain-patterns.json, workflow-patterns.json

#### Project Structure

**Key Directories**: `workflows/` (n8n workflow definitions), `nodes/` (custom n8n nodes, optional), `credentials/` (optional), `tests/`, `scripts/`

**Key Files**: `.cursorrules`, `package.json`, `tsconfig.json` (optional), `.n8n/config.json` (optional), `docker-compose.yml` (optional)

#### Key Rules

- Keep workflows focused and single-purpose, use descriptive node names
- Implement retry logic, error triggers, and fallback actions in all workflows
- Never hardcode credentials, use n8n credential store
- Validate webhook signatures and use HTTPS in production
- Use sub-workflows for reusable functionality
- Use JavaScript/TypeScript code nodes for custom logic, handle errors gracefully
- Process items in batches for large datasets and rate limit handling
- Document complex workflows and node configurations
- Test workflows thoroughly before deployment
- Use LangChain patterns for AI agent orchestration in workflows

#### MCP Integrations

- **atlassian** (optional): Jira/Confluence integration
- **deepwiki** (optional): GitHub analysis

---

## Summary

This reference document provides comprehensive information about all 27 technology blueprints available in the Cursor Agent Factory. Each blueprint is designed to provide a complete, production-ready foundation for developing applications in specific technology stacks, with pre-configured AI agents, skills, knowledge bases, and best practices.

**Blueprint Categories:**
- **Backend/API**: python-fastapi, java-spring, kotlin-spring, csharp-dotnet
- **Frontend/Full-Stack**: typescript-react, nextjs-fullstack, python-streamlit
- **AI/Agent**: ai-agent-development, multi-agent-systems, financial-ai-agents
- **Blockchain**: solidity-ethereum, defi-protocols, solana-rust
- **Financial AI**: quantitative-trading, financial-ai-agents
- **Integration**: sap-abap, sap-rap, sap-cap, sap-cpi-pi, n8n-automation

When selecting a blueprint, consider your team's language preferences, project type, experience level, and enterprise context. The factory will customize the selected blueprint based on your specific requirements during project generation.
