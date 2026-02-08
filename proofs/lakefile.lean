/-
  Cursor Agent Factory - Formal Verification System
  
  This Lean 4 project provides mathematical proofs that the Cursor Agent Factory
  satisfies its foundational axioms (A0-A5).
  
  Philosophy:
  - Love: Free and accessible to all
  - Truth: Mathematical certainty, verifiable by anyone  
  - Beauty: Elegant, harmonious proofs
  
  To verify: `lake build`
  All proofs type-check → System satisfies axioms
-/

import Lake
open Lake DSL

package «cursor-agent-factory-proofs» where
  version := v!"1.0.0"
  description := "Formal verification of Cursor Agent Factory axiom compliance"
  keywords := #["formal-verification", "ai-safety", "axioms", "state-machines"]

-- No external dependencies needed for core proofs
-- Uses only Lean 4 standard library

@[default_target]
lean_lib «Axioms» where
  roots := #[`Axioms]

lean_lib «Guardian» where
  roots := #[`Guardian.States, `Guardian.Transitions, `Guardian.Safety, `Guardian.Invariants]

lean_lib «Memory» where
  roots := #[`Memory.Types, `Memory.Consent]

lean_lib «Layers» where
  roots := #[`Layers.Immutability]

lean_lib «Project» where
  roots := #[`Project.Templates]
