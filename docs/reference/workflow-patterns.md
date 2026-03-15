# Antigravity Workflow Patterns & Stack Catalog

This catalog provides a comprehensive mapping of all available execution workflows (`.agent/workflows/*.md`) powered by the Antigravity Agent Factory. Workflows are categorization by their target domain, tech stack, and their alignment with the 7-phase Meta-Orchestration SDLC.

---

## 1. Core Meta-Orchestration & System Design

These workflows manage the factory itself, overarching system design, and the high-level SDLC phases.

| Command | SDLC Phase | Description |
| :--- | :--- | :--- |
| `/sdlc-meta-orchestrator` | P1-P7 | Coordinating meta-workflow that sequentially orchestrates the 7 SDLC phases. |
| `/ai-system-design` | P3_Architecture | Comprehensive workflow for designing AI systems including requirements analysis and architecture. |
| `/antigravity-factory-building` | P3-P6 | Workflow for designing, building, and structuring the factory system itself. |
| `/multi-agent-orchestration` | P3_Architecture | Designing, implementing, and deploying multi-agent AI systems topology. |
| `/write-prd` | P2_Requirements | Comprehensive workflow for writing the Product Requirements Document (PRD). |
| `/elicit-nfr` | P2_Requirements | Structured Socratic elicitation session to surface all non-functional requirements. |
| `/review-requirements` | P2_Requirements | Adversarial review of requirements using 3 personas + a judge. |
| `/brief-prototype` | P1_Ideation | Formalizes a selected opportunity into a Prototype Brief. |

---

## 2. Standard Feature Delivery & QA

Agnostic workflows for building, documenting, and ensuring the quality of standard features.

| Command | SDLC Phase | Description |
| :--- | :--- | :--- |
| `/feature-development` | P4_Build | Standard Feature Delivery Cycle (SFDC) for developing new features. |
| `/tdd-cycle` | P4_Build | Test-Driven Development workflow implementing the Red-Green-Refactor cycle. |
| `/bdd-driven-development` | P4_Build | Behavior-Driven Development translating Gherkin scenarios into code. |
| `/code-review` | P5_Test_Eval | Comprehensive structured code reviews covering correctness, style, design. |
| `/quality-gate` | P5_Test_Eval | Automated quality gate that enforces code quality standards before merge. |
| `/security-audit` | P5_Test_Eval | Systematic review of code for vulnerabilities and dependency checks. |
| `/documentation-workflow` | P6_Deploy | SDLC workflow for generating and maintaining comprehensive project documentation. |

---

## 3. Tech Stack: AI, ML, & LLM Apps

Specialized workflows for building intelligent systems.

| Command | Category | Description |
| :--- | :--- | :--- |
| `/agent-development` | AI Agents | Multi-step workflow for developing AI agents from design through deployment. |
| `/build-langchain-agent` | AI Agents | Specific pipeline for building an AI agent with LangChain. |
| `/agent-testing` | AI Testing | Agent testing covering unit tests, integration tests, and LLM evaluation. |
| `/coordination-testing` | AI Testing | Multi-agent coordination testing and validation workflow. |
| `/llm-app-development` | LLM Apps | Developing production-ready LLM applications from prototype to production. |
| `/rag-pipeline-development` | LLM Apps | End-to-end workflow for developing RAG systems and vector ingestion. |
| `/prompt-iteration` | Prompting | Iterative prompt engineering and optimization cycle. |
| `/ml-experiment` | ML DevOps | ML experiment workflow from hypothesis formation through results analysis. |
| `/model-training-pipeline` | ML DevOps | Comprehensive workflow for training ML models (data prep to optimization). |
| `/model-evaluation` | ML DevOps | ML model evaluation covering metrics selection and model comparison. |
| `/ml-deployment-pipeline` | ML DevOps | Deploying ML models to production (containerization, serving). |

---

## 4. Tech Stack: Enterprise Backends & Web

Standard workflows for traditional software engineering stacks.

| Command | Stack | Description |
| :--- | :--- | :--- |
| `/fastapi-api-development` | Python | Production-ready FastAPI apps with SQLAlchemy async, Pydantic, etc. |
| `/spring-microservice-development` | Java | Spring Boot microservices with JPA, REST APIs, testing, security. |
| `/dotnet-api-development` | .NET / C# | ASP.NET Core APIs with Entity Framework Core, authentication. |
| `/dotnet-microservices-setup` | .NET / C# | Designing and implementing microservices architectures with .NET. |
| `/nextjs-feature-development` | TS / Node | Next.js application feature development from design to React codebase. |

---

## 5. Tech Stack: SAP Enterprise Suite

Highly specialized workflows for the SAP ecosystem.

| Command | Module | Description |
| :--- | :--- | :--- |
| `/cap-service-development` | SAP BTP | SAP Cloud Application Programming Model (CAP) service development. |
| `/fiori-app-development` | SAP UI | Fiori Elements applications in SAP S/4HANA (CDS data modeling). |
| `/rap-development` | S/4HANA | RESTful ABAP Programming Model (RAP) business objects. |
| `/rap-with-draft` | S/4HANA | RAP business objects with draft handling. |
| `/btp-service-deployment` | SAP BTP | Deploying SAP applications to SAP Business Technology Platform. |
| `/iflow-development` | SAP CPI | SAP Cloud Platform Integration (CPI) iFlow development. |
| `/mm-development` | SAP MM | Materials Management: procurement, inventory, movements (EKKO, EKPO). |
| `/sd-development` | SAP SD | Sales and Distribution: pricing, billing, delivery (VBAK, VBAP). |
| `/fi-development` | SAP FI | Financial Accounting: reports, enhancements, validations (BKPF, BSEG). |
| `/ewm-development` | SAP EWM | Extended Warehouse Management: warehouse structure, movements. |
| `/le-development` | SAP LE | Logistics Execution: shipping, transportation, delivery processing. |

---

## 6. DevOps, CI/CD, & Release

Workflows focused on Phase 6 (Deploy) and Phase 7 (Monitor).

| Command | Focus | Description |
| :--- | :--- | :--- |
| `/cicd-pipeline` | General | Managing continuous integration and deployment pipelines. |
| `/github-actions-ci` | GitHub | GitHub Actions CI/CD pipeline setup and maintenance. |
| `/java-cicd-pipeline` | Java | CI/CD for Java/Spring Boot using Maven/Gradle, Testcontainers, Docker. |
| `/sap-cicd-pipeline` | SAP | CI/CD pipelines for SAP applications (transports, automated checks). |
| `/azure-deployment` | .NET/Azure | Deploying .NET applications to Azure cloud services (App Service, ACA). |
| `/release-management` | Release | Version bumping, changelog generation, tagging, and deployment prep. |
| `/monitor` | Production | Comprehensive workflow for production monitoring and feedback loops. |
| `/incident-response` | Ops | Responding to production incidents (triage, mitigation, resolution). |
| `/debug-pipeline` | Ops | Systematic workflow for debugging CI/CD pipeline failures. |

---

## 7. Agile & Project Management

Workflows for backlog management and team coordination.

| Command | Focus | Description |
| :--- | :--- | :--- |
| `/sprint-planning` | Scrum | Backlog review, capacity calculation, story selection, sprint backlog. |
| `/sprint-closure` | Scrum | Status review, velocity calculation, incomplete item handling. |
| `/backlog-refinement` | Scrum | Prioritization, estimation, story refinement. |
| `/daily-standup` | Agile Ops | Automated workflow for facilitating daily standups and blockers. |
| `/plane-task-management` | Plane PMS | Systematic workflow for managing Plane PMS issues and states. |
| `/jira-bugfix` | Jira PMS | Jira-triggered bugfix workflow from ticket analysis through resolution. |
| `/bugfix-resolution` | General | Resolving bugs from ticket analysis through implementation and verification. |

---

## 8. Web3 & Blockchain

| Command | Ecosystem | Description |
| :--- | :--- | :--- |
| `/smart-contract-development` | EVM | Solidity/Ethereum design, implementation, testing, and audit prep. |
| `/smart-contract-audit` | EVM | Security audit for smart contracts (static analysis, gas optimization). |
| `/defi-development` | Finance | DeFi protocol development with AMM, lending, and staking patterns. |
| `/solana-development` | Solana | Solana program development with Anchor framework. |
| `/deployment-workflow` | DevOps | Blockchain deployment from testnet through mainnet. |

---

## Implemented Workflows Catalog

This section serves as the definitive reference for the Antigravity Agent Factory's workflow capabilities.
