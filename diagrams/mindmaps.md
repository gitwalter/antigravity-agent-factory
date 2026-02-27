# Antigravity Agent Factory Mindmaps

> Hierarchical visual navigation for all major concepts in the system.

This document contains 12 mindmaps providing conceptual overviews of the Antigravity Agent Factory. Use these for quick navigation and understanding relationships between components.

---

## Navigation

- [1. System Overview](#1-system-overview)
- [2. 5-Layer Architecture](#2-5-layer-architecture)
- [3. Axiom Derivation](#3-axiom-derivation)
- [4. Agent Ecosystem](#4-agent-ecosystem)
- [5. Skills Taxonomy](#5-skills-taxonomy)
- [6. Knowledge Files](#6-knowledge-files)
- [7. Blueprints](#7-blueprints)
- [8. Guardian System](#8-guardian-system)
- [9. Memory System](#9-memory-system)
- [10. Workflow System](#10-workflow-system)
- [11. Onboarding Paths](#11-onboarding-paths)
- [12. Verification Ecosystem](#12-verification-ecosystem)

---

## 1. System Overview

A high-level view of all major components in the Antigravity Agent Factory.

```mermaid
%%{init: {'theme': 'neutral'}}%%
mindmap
  root((Antigravity Agent Factory))
    Factory_Components
      Agents
        12_Factory_Agents
        4_PM_Agents
      Skills
        40+_Skills
        8_Categories
      Knowledge
        89_JSON_Files
        10_Categories
      Blueprints
        27_Blueprints
        8_Categories
      Templates
        Code_Templates
        Document_Templates
      Workflows
        21_Patterns
        5_Categories
    Generated_Projects
      .cursorrules
        5_Layer_Config
      PURPOSE.md
        Mission_Statement
      .cursor_agents
        Code_Reviewer
        Test_Generator
        Explorer
      .cursor_skills
        TDD
        Grounding
        Workflows
      knowledge
        Domain_Files
      templates
        Stack_Specific
    Key_Systems
      Guardian
        Layer_0_Protection
        5_Response_Levels
      Memory
        User_Validated_Learning
        Consent_Loop
      Verification
        Lean_4_Proofs
        Society_Runtime
      Workflows
        Orchestration
        Learning_Hooks
```

**Related Documentation**: [README.md](../README.md), **docs/COMPLETE_GUIDE.md**

---

## 2. 5-Layer Architecture

The hierarchical layer system from foundational axioms to technical implementation.

```mermaid
%%{init: {'theme': 'neutral'}}%%
mindmap
  root((5-Layer Architecture))
    L0_Integrity
      Axiom_Zero
        Love
        Truth
        Beauty
      Core_Axioms
        A1_Verifiability
        A2_User_Primacy
        A3_Transparency
        A4_Non_Harm
        A5_Consistency
      Derivation_Rules
        D1_to_D5
      Validation
        VC1_to_VC5
      Status_IMMUTABLE
    L1_Purpose
      Mission_Statement
      Stakeholders
      Success_Criteria
      Artifact_PURPOSE.md
      Status_IMMUTABLE
    L2_Principles
      Ethical_Boundaries
        EB1_No_Silent_Failures
        EB2_No_Destructive
        EB3_No_Ignoring_User
        EB4_No_Unverified
        EB5_No_Violations
      Quality_Standards
        QS1_to_QS5
      Failure_Handling
      Status_IMMUTABLE
    L3_Methodology
      Agile_Scrum
      Kanban
      R_and_D
      Enterprise
      Enforcement_Patterns
      Practice_Patterns
      Status_MUTABLE
    L4_Technical
      Stack_Config
      Agent_Definitions
      Skill_Patterns
      Knowledge_Files
      Templates
      MCP_Servers
      Status_MUTABLE
```

**Related Documentation**: **docs/LAYERED_ARCHITECTURE.md**, [diagrams/formal-verification.md](formal-verification.md)

---

## 3. Axiom Derivation

How the foundational axioms derive into principles and behaviors.

```mermaid
%%{init: {'theme': 'neutral'}}%%
mindmap
  root((Axiom System))
    A0_Love_Truth_Beauty
      Love
        Genuine_Care
        Grounds_A2_A4
      Truth
        Honesty_Verifiability
        Grounds_A1_A3_A5
      Beauty
        Harmony_Elegance
        Shapes_Expression
      Emergence
        Trust
        Flourishing
    A1_Verifiability
      From_Truth
      Code_Must_Have_Tests
      Claims_Cite_Sources
      Outputs_Reproducible
      Derives_QS1_EB4
    A2_User_Primacy
      From_Love
      Clarify_Ambiguous
      Prefer_User_Prefs
      Respect_Decisions
      Derives_EB3
      Memory_Consent
    A3_Transparency
      From_Truth
      Document_Rationale
      Explain_Reasoning
      No_Hidden_Logic
      Derives_EB1_QS2_QS3
    A4_Non_Harm
      From_Love
      Validate_Destructive
      Warn_Risky
      Refuse_Harmful
      Derives_EB2
      Guardian_Protection
    A5_Consistency
      From_Truth
      Rules_Trace_Axioms
      Conflicts_By_Precedence
      Invalid_Rejected
      Derives_EB5_VC2
```

**Related Documentation**: [proofs/Axioms.lean](../proofs/Axioms.lean), **docs/research/AXIOM_BASED_AGENT_ARCHITECTURE.md**

---

## 4. Agent Ecosystem

All 16 agents organized by role and their coordination patterns.

```mermaid
%%{init: {'theme': 'neutral'}}%%
mindmap
  root((Agent Ecosystem))
    Generation_Pipeline
      requirements_architect
        5_Phase_Gathering
      stack_builder
        Blueprint_Matching
      workflow_designer
        Workflow_Config
      knowledge_manager
        Domain_Knowledge
      template_generator
        Code_Generation
    Knowledge_Agents
      knowledge_extender
        Research_Synthesis
      knowledge_evolution
        Update_Coordination
      workflow_architect
        Complex_Workflows
    Onboarding_Agents
      onboarding_architect
        Repo_Integration
      workshop_facilitator
        Team_Workshops
    Protection_Agent
      integrity_guardian
        Layer_0_Protector
        Always_Active
        5_Response_Levels
    Debugging_Agent
      debug_conductor
        Autonomous_Debug
        6_Phase_Workflow
    PM_Agents
      product_owner
        Backlog_Management
      sprint_master
        Agile_Ceremonies
      task_manager
        Task_Creation
      reporting_agent
        Metrics_Generation
    Coordination_Patterns
      Sequential_Pipeline
      Embedded_Harmony
      Supervisor_Worker
      Hierarchical
      Verified_Communication
```

**Related Documentation**: **docs/reference/FACTORY_COMPONENTS.md**, [diagrams/agent-coordination.md](agent-coordination.md)

---

## 5. Skills Taxonomy

All 40+ skills organized by category.

```mermaid
%%{init: {'theme': 'neutral'}}%%
mindmap
  root((Skills Taxonomy))
    Requirements
      requirements_gathering
      purpose_definition
      axiom_selection
    Stack
      stack_configuration
      methodology_selection
    Generation
      agent_generation
      skill_generation
      knowledge_generation
      template_generation
      cursorrules_generation
      workflow_generation
    Practices
      practice_selection
      enforcement_selection
    Quality
      alignment_check
      pattern_feedback
      readme_validation
    Specialized
      onboarding_flow
      team_workshop
      team_huddle
      express_onboarding
      shell_platform
      commit_release
      ci_monitor
      pipeline_error_fix
      research_first
      wisdom_harvest
    Verification
      grounding_verification
      strawberry_verification
      verified_communication
    Knowledge_Extension
      extend_knowledge
      update_knowledge
      analyze_gaps
    Workflow_Extension
      extend_workflow
    PM_Skills
      create_epic
      create_story
      create_task
      estimate_task
      plan_sprint
      run_standup
      close_sprint
      generate_burndown
      health_check
```

**Related Documentation**: **.cursor/skills/**, **docs/reference/FACTORY_COMPONENTS.md**

---

## 6. Knowledge Files

89 knowledge files organized by category.

```mermaid
%%{init: {'theme': 'neutral'}}%%
mindmap
  root((Knowledge Files))
    Stack_Specific
      fastapi_patterns
      nextjs_patterns
      spring_patterns
      dotnet_patterns
      react_patterns
      streamlit_patterns
    AI_Agent
      langchain_patterns
      langgraph_workflows
      crewai_patterns
      autogen_patterns
      mcp_patterns
      agent_coordination
      prompt_engineering
      rag_patterns
    AI_ML
      pytorch_patterns
      huggingface_patterns
      deep_learning
      ml_workflow
      fine_tuning
      vector_database
    Blockchain
      solana_patterns
      anchor_patterns
      bitcoin_patterns
      ethereum_security
    Cloud_Native
      kubernetes_patterns
      docker_patterns
    Integration
      n8n_patterns
      cicd_patterns
      mcp_servers_catalog
    SAP_ABAP
      naming_conventions
      common_tables
      tadir_objects
      sap_cap_patterns
    Core
      design_patterns
      architecture_patterns
      tdd_patterns
      best_practices
      security_checklist
    Trading_Quant
      trading_patterns
      quantitative_finance
      risk_management
    Factory_Meta
      skill_catalog
      stack_capabilities
      guardian_protocol
      memory_config
      artifact_dependencies
      manifest
```

**Related Documentation**: **docs/reference/KNOWLEDGE_FILES.md**, [knowledge/](../knowledge/)

---

## 7. Blueprints

27 blueprints organized by category.

```mermaid
%%{init: {'theme': 'neutral'}}%%
mindmap
  root((Blueprints))
    Backend_API
      python_fastapi
      java_spring
      kotlin_spring
      csharp_dotnet
    Frontend_FullStack
      typescript_react
      nextjs_fullstack
      python_streamlit
    AI_Agent
      ai_agent_development
      multi_agent_systems
      python_multi_agent
      python_rag_system
    AI_ML
      python_ml_experimentation
      python_deep_learning
      python_fine_tuning
    AI_Starter
      starter_ml_classification
      starter_chatbot
      starter_rag
    Integration
      sap_abap
      sap_rap
      sap_cap
      sap_cpi_pi
      n8n_automation
    Blockchain
      solidity_ethereum
      defi_protocols
      solana_rust
    Financial_AI
      quantitative_trading
      financial_ai_agents
```

**Related Documentation**: [docs/reference/BLUEPRINTS.md](../docs/reference/BLUEPRINTS.md), [blueprints/](../docs/reference/BLUEPRINTS.md)

---

## 8. Guardian System

The Layer 0 protector with its response levels and operational states.

```mermaid
%%{init: {'theme': 'neutral'}}%%
mindmap
  root((Guardian System))
    Response_Levels
      Level_0_Flow
        Natural_Alignment
        Continue_Normally
      Level_1_Nudge
        Slight_Drift
        Subtle_Correction
      Level_2_Pause
        Approaching_Boundary
        Explain_and_Ask
      Level_3_Block
        Clear_Violation
        Stop_and_Offer_Alternatives
      Level_4_Protect
        Imminent_Harm
        Prevent_Then_Explain
    Operational_States
      Embedded
        Zero_Overhead
        Self_Monitoring
        Constitutional_Preamble
      Awakened
        Full_Tool_Access
        Full_Layer_Access
        Can_Pause_Block_Protect
    Harm_Patterns
      Critical_File_Deletion
      Secrets_Commit
      Destructive_Commands
      Deceptive_Output
      Runaway_Operations
    Water_Way_Resolution
      Detect_Tension
      Dont_Force
      Provide_Context
      Find_The_Path
      Resolve_With_Love
```

**Related Documentation**: [.cursor/agents/integrity-guardian.md](../.agent/agents/integrity-guardian.md), [diagrams/guardian-state-machine.md](guardian-state-machine.md)

---

## 9. Memory System

User-validated learning with consent loop and layer protection.

```mermaid
%%{init: {'theme': 'neutral'}}%%
mindmap
  root((Memory System))
    Memory_Types
      Semantic
        User_Approved
        Permanent
        Searchable
      Episodic
        Session_Based
        Cleared_On_End
      Pending
        Awaiting_Approval
        Until_Decision
      Rejected
        Tracks_Rejections
        Prevents_Reproposing
    Consent_Loop
      Observation
        Detect_Pattern
      Generalization
        Abstract_Proposal
      Confidence_Scoring
        Explicit_100_pct
        Correction_95_pct
        Preference_85_pct
        Error_80_pct
        Pattern_70_pct
      Proposal
        Present_With_Context
      Decision
        Approve
        Reject
        Edit
        Defer
      Storage
        Permanent_If_Approved
    Layer_Protection
      Immutable_L0_L2
        L0_Axioms
        L1_Purpose
        L2_Principles
      Mutable_L3_L4
        L3_Methodology
        L4_Technical
```

**Related Documentation**: **docs/MEMORY_SYSTEM.md**, [diagrams/memory-system.md](memory-system.md)

---

## 10. Workflow System

Declarative workflow definitions with triggers, phases, and learning hooks.

```mermaid
%%{init: {'theme': 'neutral'}}%%
mindmap
  root((Workflow System))
    Components
      Metadata
        ID
        Name
        Version
      Triggers
        Activation_Conditions
      Context
        Required_Inputs
      Phases
        Steps
        Actions
        Skills
        Outputs
      Escalations
      Learning_Hooks
    Trigger_Types
      Event
        CI_Failure_Webhook
      Schedule
        Time_Based
      Manual
        User_Invocation
      Watch
        File_State_Change
      Chain
        Workflow_Completes
    Lifecycle_States
      Idle
      Triggered
      Validating
      Initializing
      Executing
      StepComplete
      DecisionPoint
      PhaseComplete
      Verifying
      Learning
      Completed
      Failed
    Escalation_Patterns
      Confidence_80_plus
        Proceed_Autonomous
      Confidence_50_Reversible
        Proceed_With_Logging
      Confidence_70_plus
        Escalate_Confirmation
      Confidence_Below_70
        Escalate_Approval
```

**Related Documentation**: **docs/research/WORKFLOW_SYSTEM.md**, [diagrams/learning-loops.md](learning-loops.md)

---

## 11. Onboarding Paths

Three onboarding options for individuals and teams.

```mermaid
%%{init: {'theme': 'neutral'}}%%
mindmap
  root((Onboarding Paths))
    Express_Lane
      Duration_10_15_min
      Participants_Individual
      Approach
        Guided_Prompts
        Template_Based
      Output
        Basic_Agent_System
      Features
        3_Values_Capture
        1_Wisdom_Question
        Default_Methodology
    Team_Huddle
      Duration_1_2_hours
      Participants_2_5_people
      Approach
        Mini_Games
        Shared_Decisions
      Output
        Team_Aligned_System
      Features
        Team_Vote_Values
        Quick_Consensus
        Creative_Naming
    Workshop_Series
      Duration_11_15_hours
      Participants_6_plus
      Approach
        5_Workshops
        Games_Per_Session
      Workshops
        W1_Vision_Quest
          Future_Headlines
          Stakeholder_Safari
        W2_Ethics_Arena
          Dilemma_Duel
          Value_Auction
        W3_Stack_Safari
          Trade_Off_Tetris
          Architecture_Pictionary
        W4_Agent_Assembly
          Trading_Cards
          Skill_Bingo
        W5_Integration
          Demo_Derby
          Gratitude_Circle
```

**Related Documentation**: [docs/guides/getting-started.md](../docs/guides/getting-started.md), **docs/TEAM_WORKSHOP_GUIDE.md**

---

## 12. Verification Ecosystem

Static proofs (Lean 4) and runtime verification (Society).

```mermaid
%%{init: {'theme': 'neutral'}}%%
mindmap
  root((Verification Ecosystem))
    Lean_4_Proofs
      Axiom_Proofs
        A0_Love_Truth_Beauty
        A1_Transparency
        A2_User_Primacy
        A3_Derivability
        A4_Non_Harm
        A5_Consistency
      Guardian_Proofs
        escalation_preserves_state
        block_offers_alternatives
        protect_preserves_state
        pause_notifies
      Memory_Proofs
        approved_satisfies_consent
        cannot_modify_layer0
        cannot_modify_layer1
        cannot_modify_layer2
      Layer_Proofs
        layer0_blocked
        layer1_blocked
        layer2_blocked
        read_always_allowed
    Society_Verification
      Event_Sourcing
        Immutable_Chain
        Crypto_Signatures
        Hash_Linking
      Agent_Contracts
        Capabilities
        Obligations
        Prohibitions
      Trust_Reputation
        Identity_Ed25519
        Reputation_0_100
        Trust_Delegation
      Blockchain_Anchoring
        Merkle_Trees
        Batch_Submission
        Smart_Contracts
    Trust_Levels
      L0_Local
        Signed_Events
      L1_Attested
        Merkle_Anchored
      L2_Contracted
        Smart_Contract
      L3_Consensus
        Multi_Party
```

**Related Documentation**: **docs/VERIFICATION.md**, **docs/SOCIETY_USAGE.md**, [diagrams/formal-verification.md](formal-verification.md)

---

## Cross-Reference Guide

| Mindmap | Primary Docs | Related Diagrams |
|---------|--------------|------------------|
| System Overview | README, COMPLETE_GUIDE | All diagrams |
| 5-Layer Architecture | LAYERED_ARCHITECTURE | formal-verification.md |
| Axiom Derivation | proofs/Axioms.lean | formal-verification.md |
| Agent Ecosystem | FACTORY_COMPONENTS | agent-coordination.md |
| Skills Taxonomy | FACTORY_COMPONENTS | - |
| Knowledge Files | KNOWLEDGE_FILES | knowledge-management.md |
| Blueprints | BLUEPRINTS | - |
| Guardian System | GUARDIAN_COORDINATION | guardian-state-machine.md |
| Memory System | MEMORY_SYSTEM | memory-system.md |
| Workflow System | WORKFLOW_SYSTEM | learning-loops.md |
| Onboarding Paths | GETTING_STARTED | onboarding-flows.md |
| Verification | VERIFICATION, SOCIETY_USAGE | formal-verification.md |

---

*Generated by the Antigravity Agent Factory. Last updated: 2026-02-05*
