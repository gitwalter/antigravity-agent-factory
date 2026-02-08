/-
  Memory/Types.lean - Memory System Type Definitions
  
  Cursor Agent Factory - Formal Verification System
  
  This file defines the types for the Memory System, which enables
  user-validated learning from experience.
  
  Philosophy: The Memory System embodies A2 (User Primacy) - 
  users control what the agent learns. All memories require 
  explicit user approval.
-/

import Axioms

namespace CursorAgentFactory.Memory

/-!
  # Memory Types
  
  The Memory System has four categories:
  
  | Type     | Description                        | Persistence |
  |----------|------------------------------------| ------------|
  | Semantic | User-approved long-term knowledge  | Permanent   |
  | Episodic | Session-based observations         | Session     |
  | Pending  | Awaiting user approval             | Temporary   |
  | Rejected | Tracks rejected to avoid re-asking | Permanent   |
-/

/-- Memory type categories -/
inductive MemoryType where
  | semantic : MemoryType  -- Long-term user-approved knowledge
  | episodic : MemoryType  -- Session-based observations
  | pending  : MemoryType  -- Awaiting user approval
  | rejected : MemoryType  -- Previously rejected (don't re-ask)
  deriving Repr, DecidableEq, Inhabited

/-- Persistence level for memories -/
inductive Persistence where
  | permanent : Persistence  -- Survives sessions
  | session   : Persistence  -- Cleared when session ends
  | temporary : Persistence  -- Short-lived
  deriving Repr, DecidableEq

/-- Map memory types to persistence -/
def MemoryType.persistence : MemoryType → Persistence
  | .semantic => .permanent
  | .episodic => .session
  | .pending  => .temporary
  | .rejected => .permanent

/-!
  # Memory Sources
  
  How memories are created.
-/

/-- Sources of memory creation -/
inductive MemorySource where
  | userCorrection : MemorySource    -- User corrected the agent
  | explicitTeaching : MemorySource  -- User explicitly taught something
  | preferenceDetection : MemorySource  -- Pattern detected from behavior
  | errorResolution : MemorySource   -- User solved a problem
  | successfulPattern : MemorySource -- Repeated successful approach
  deriving Repr, DecidableEq

/-- Confidence levels by source -/
def MemorySource.confidenceLevel : MemorySource → Nat
  | .explicitTeaching    => 100
  | .userCorrection      => 95
  | .preferenceDetection => 85
  | .errorResolution     => 80
  | .successfulPattern   => 70

/-!
  # Memory Scope
  
  Where memories apply.
-/

/-- Scope of memory application -/
inductive MemoryScope where
  | global  : MemoryScope  -- Applies to all projects
  | project : MemoryScope  -- Applies to specific project
  deriving Repr, DecidableEq, Inhabited

/-!
  # Memory Record
  
  Complete memory structure.
-/

/-- A memory record -/
structure Memory where
  /-- Unique identifier -/
  id : String
  /-- Content of the memory -/
  content : String
  /-- Type of memory -/
  memoryType : MemoryType
  /-- How it was created -/
  source : MemorySource
  /-- Where it applies -/
  scope : MemoryScope
  /-- Confidence level (0-100) -/
  confidence : Nat
  /-- Has user explicitly approved? -/
  userApproved : Bool
  /-- Timestamp of creation -/
  createdAt : Nat
  deriving Repr, DecidableEq

/-- Create a pending memory proposal -/
def createProposal (id content : String) (source : MemorySource) 
    (scope : MemoryScope) (timestamp : Nat) : Memory := {
  id := id
  content := content
  memoryType := MemoryType.pending
  source := source
  scope := scope
  confidence := source.confidenceLevel
  userApproved := false
  createdAt := timestamp
}

/-- Approve a pending memory (convert to semantic) -/
def approveMemory (m : Memory) : Memory :=
  if m.memoryType = MemoryType.pending then
    { m with 
      memoryType := MemoryType.semantic
      userApproved := true 
    }
  else m

/-- Reject a pending memory -/
def rejectMemory (m : Memory) : Memory :=
  if m.memoryType = MemoryType.pending then
    { m with 
      memoryType := MemoryType.rejected
      userApproved := false 
    }
  else m

/-!
  # Memory State
  
  Overall state of the memory system.
-/

/-- Memory system state -/
structure MemoryState where
  /-- All semantic memories -/
  semanticMemories : List Memory
  /-- Current session episodic memories -/
  episodicMemories : List Memory
  /-- Pending proposals -/
  pendingProposals : List Memory
  /-- Rejected memory patterns (to avoid re-proposing) -/
  rejectedPatterns : List Memory
  deriving Repr

/-- Initial empty memory state -/
def initialMemoryState : MemoryState := {
  semanticMemories := []
  episodicMemories := []
  pendingProposals := []
  rejectedPatterns := []
}

/-!
  # Layer Protection
  
  The Memory System respects layer protection.
  Layers 0-2 are IMMUTABLE and cannot be modified by memories.
-/

/-- Check if a memory target is in a protected layer -/
def isProtectedLayer (layer : Layer) : Bool :=
  layer.isImmutable

/-- Memory cannot modify protected layers -/
structure MemoryLayerConstraint where
  memory : Memory
  targetLayer : Layer
  isAllowed : Bool := !isProtectedLayer targetLayer
  deriving Repr

/-- Theorem: Memory cannot modify Layer 0 -/
theorem memory_cannot_modify_layer0 (mlc : MemoryLayerConstraint) :
    mlc.targetLayer = Layer.axioms → mlc.isAllowed = false := by
  intro h
  unfold MemoryLayerConstraint.isAllowed isProtectedLayer Layer.isImmutable at *
  simp [h]

/-- Theorem: Memory cannot modify Layer 1 -/
theorem memory_cannot_modify_layer1 (mlc : MemoryLayerConstraint) :
    mlc.targetLayer = Layer.purpose → mlc.isAllowed = false := by
  intro h
  unfold MemoryLayerConstraint.isAllowed isProtectedLayer Layer.isImmutable at *
  simp [h]

/-- Theorem: Memory cannot modify Layer 2 -/
theorem memory_cannot_modify_layer2 (mlc : MemoryLayerConstraint) :
    mlc.targetLayer = Layer.principles → mlc.isAllowed = false := by
  intro h
  unfold MemoryLayerConstraint.isAllowed isProtectedLayer Layer.isImmutable at *
  simp [h]

end CursorAgentFactory.Memory
