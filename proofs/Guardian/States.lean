/-
  Guardian/States.lean - Integrity Guardian State Machine

  Cursor Agent Factory - Formal Verification System

  This file formalizes the Integrity Guardian's state machine,
  which protects Layer 0 axioms through graduated response levels.

  Philosophy (Wu Wei - The Way of Non-Action):
  "The best leader is hardly known to exist."
  "The supreme art is to subdue without fighting."

  The Guardian operates through presence, not force.
-/

import Axioms

namespace CursorAgentFactory.Guardian

/-!
  # Response Levels

  The Guardian has 5 response levels, following Wu Wei principles:

  | Level | Name    | Trigger              | Response              |
  |-------|---------|----------------------|-----------------------|
  | 0     | Flow    | Natural alignment    | Continue normally     |
  | 1     | Nudge   | Slight drift         | Self-correct subtly   |
  | 2     | Pause   | Boundary approached  | Explain, ask user     |
  | 3     | Block   | Clear violation      | Stop, explain, offer  |
  | 4     | Protect | Imminent harm        | Prevent, then explain |
-/

/-- Response levels as inductive type -/
inductive ResponseLevel where
  | flow    : ResponseLevel  -- Level 0: Natural alignment
  | nudge   : ResponseLevel  -- Level 1: Slight drift
  | pause   : ResponseLevel  -- Level 2: Boundary approached
  | block   : ResponseLevel  -- Level 3: Clear violation
  | protect : ResponseLevel  -- Level 4: Imminent harm
  deriving Repr, DecidableEq, Inhabited

/-- Convert response level to natural number for comparison -/
def ResponseLevel.toNat : ResponseLevel → Nat
  | .flow    => 0
  | .nudge   => 1
  | .pause   => 2
  | .block   => 3
  | .protect => 4

/-- Response level ordering -/
instance : LE ResponseLevel where
  le a b := a.toNat ≤ b.toNat

instance : LT ResponseLevel where
  lt a b := a.toNat < b.toNat

/-- Decidable equality for response levels -/
instance (a b : ResponseLevel) : Decidable (a ≤ b) :=
  inferInstanceAs (Decidable (a.toNat ≤ b.toNat))

/-!
  # Guardian States

  The Guardian can be in two operational states:
  - Embedded: Part of every agent's awareness (zero overhead)
  - Awakened: Full power when axiom boundaries are crossed
-/

/-- Operational state of the Guardian -/
inductive OperationalState where
  | embedded : OperationalState  -- Normal: zero overhead, agents self-monitor
  | awakened : OperationalState  -- Active: full tool access, full power
  deriving Repr, DecidableEq, Inhabited

/-!
  # Guardian State Machine

  Complete state of the Guardian at any point in time.
-/

/-- Full Guardian state -/
structure GuardianState where
  /-- Current response level (0-4) -/
  responseLevel : ResponseLevel
  /-- Operational state (embedded or awakened) -/
  operational : OperationalState
  /-- Has the user been notified of the current state? -/
  userNotified : Bool
  /-- Is the user's work state preserved? -/
  statePreserved : Bool
  /-- Have alternatives been offered (for Block level)? -/
  alternativesOffered : Bool
  /-- Is the explanation complete? -/
  explanationProvided : Bool
  deriving Repr, DecidableEq

/-- Initial Guardian state (embedded, flow, everything clear) -/
def initialState : GuardianState := {
  responseLevel := ResponseLevel.flow
  operational := OperationalState.embedded
  userNotified := false  -- No notification needed at flow
  statePreserved := true
  alternativesOffered := false  -- Not applicable at flow
  explanationProvided := false  -- Not applicable at flow
}

/-!
  # Trigger Events

  Events that can cause the Guardian to change state.
-/

/-- Events that trigger Guardian state changes -/
inductive TriggerEvent where
  | naturalAlignment : TriggerEvent    -- Everything is fine
  | slightDrift : TriggerEvent         -- Minor deviation detected
  | boundaryApproached : TriggerEvent  -- Getting close to violation
  | clearViolation : TriggerEvent      -- Axiom violated
  | imminentHarm : TriggerEvent        -- Irreversible harm imminent
  | userInvocation : TriggerEvent      -- User explicitly invoked Guardian
  | multiAgentConflict : TriggerEvent  -- Agents have conflicting approaches
  deriving Repr, DecidableEq

/-- Map trigger events to appropriate response levels -/
def TriggerEvent.toResponseLevel : TriggerEvent → ResponseLevel
  | .naturalAlignment   => .flow
  | .slightDrift        => .nudge
  | .boundaryApproached => .pause
  | .clearViolation     => .block
  | .imminentHarm       => .protect
  | .userInvocation     => .pause  -- User invocation triggers pause for review
  | .multiAgentConflict => .pause  -- Conflicts trigger pause for resolution

/-!
  # State Invariants

  Properties that must always hold for Guardian states.
-/

/-- Block level always offers alternatives -/
def blockOffersAlternatives (s : GuardianState) : Prop :=
  s.responseLevel = ResponseLevel.block → s.alternativesOffered = true

/-- Protect level always preserves state -/
def protectPreservesState (s : GuardianState) : Prop :=
  s.responseLevel = ResponseLevel.protect → s.statePreserved = true

/-- Pause and above always notify user -/
def pauseNotifiesUser (s : GuardianState) : Prop :=
  s.responseLevel.toNat ≥ ResponseLevel.pause.toNat → s.userNotified = true

/-- Block and above always explain -/
def blockExplains (s : GuardianState) : Prop :=
  s.responseLevel.toNat ≥ ResponseLevel.block.toNat → s.explanationProvided = true

/-- Guardian awakens at pause level or above -/
def awakensAtPause (s : GuardianState) : Prop :=
  s.responseLevel.toNat ≥ ResponseLevel.pause.toNat →
  s.operational = OperationalState.awakened

/-- Complete invariant: all properties must hold -/
def stateInvariant (s : GuardianState) : Prop :=
  blockOffersAlternatives s ∧
  protectPreservesState s ∧
  pauseNotifiesUser s ∧
  blockExplains s ∧
  awakensAtPause s

/-!
  # Well-Formed States

  A state is well-formed if it satisfies all invariants.
-/

/-- A well-formed Guardian state -/
structure WellFormedState where
  state : GuardianState
  invariantHolds : stateInvariant state

/-- Initial state is well-formed -/
theorem initialState_wellFormed : stateInvariant initialState := by
  unfold stateInvariant
  unfold blockOffersAlternatives protectPreservesState pauseNotifiesUser blockExplains awakensAtPause
  unfold initialState
  simp [ResponseLevel.toNat]

/-- Construct a well-formed initial state -/
def wellFormedInitial : WellFormedState := {
  state := initialState
  invariantHolds := initialState_wellFormed
}

end CursorAgentFactory.Guardian
