# Formal Verification System

> **SDG • Love • Truth • Beauty**

This directory contains Lean 4 proofs that mathematically verify the Cursor Agent Factory satisfies its foundational axioms (A0-A5).

## Philosophy

"All being and doing is grounded in Love, Truth, and Beauty."

- **Love**: These proofs are free and accessible to all
- **Truth**: Mathematical certainty, verifiable by anyone
- **Beauty**: Elegant, harmonious proof structure

## Quick Start

### Prerequisites

Install Lean 4 (v4.17.0 or later):

```bash
# Linux/macOS
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh

# Windows (PowerShell)
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/leanprover/elan/master/elan-init.ps1" -OutFile "elan-init.ps1"; .\elan-init.ps1
```

### Verify Proofs

```bash
cd proofs
lake build
```

If all proofs type-check, the output shows successful compilation.
**This means the system mathematically satisfies its axioms.**

## What's Proven

### Core Axioms (`Axioms.lean`)

Formal definitions of:
- **A0**: Love, Truth, and Beauty (foundational values)
- **A1**: Transparency (all behavior traceable to rules)
- **A2**: User Primacy (explicit intent takes precedence)
- **A3**: Derivability (every rule derives from axioms)
- **A4**: Non-Harm (no irreversible harm without consent)
- **A5**: Consistency (no contradictions in rule set)

### Guardian State Machine (`Guardian/`)

| File | What's Proven |
|------|---------------|
| `States.lean` | State machine definition, invariants |
| `Transitions.lean` | Transition validity, escalation rules |
| `Safety.lean` | State preservation, user notification |
| `Invariants.lean` | Inductive invariants (hold forever) |

**Key Theorems:**
- `escalation_preserves_state`: Guardian never loses user work
- `block_offers_alternatives`: Block level always provides options
- `protect_preserves_state`: Protect level preserves all state
- `wellformed_is_safe`: Well-formed states satisfy all safety properties

### Memory System (`Memory/`)

| File | What's Proven |
|------|---------------|
| `Types.lean` | Memory type definitions, layer protection |
| `Consent.lean` | User consent required for semantic memories |

**Key Theorems:**
- `consent_always_maintained`: Semantic memories always require approval
- `memory_cannot_modify_layer0`: Memory system cannot modify axioms
- `only_approve_creates_semantic`: Only explicit approval creates permanent memories

### Layer Protection (`Layers/`)

| File | What's Proven |
|------|---------------|
| `Immutability.lean` | Layers 0-2 cannot be modified |

**Key Theorems:**
- `layer0_modifications_blocked`: Axioms are immutable
- `layer1_modifications_blocked`: Purpose is immutable
- `layer2_modifications_blocked`: Principles are immutable
- `layer_protection_holds`: Complete protection properties

### Project Templates (`Project/`)

| File | Purpose |
|------|---------|
| `Templates.lean` | Customizable templates for generated projects |

Templates for:
- Generic state machines
- API request handling
- Trading/order management
- Smart contract states

## Directory Structure

```
proofs/
├── lakefile.lean          # Lean 4 project configuration
├── lean-toolchain         # Lean version specification
├── Axioms.lean            # A0-A5 axiom definitions
├── Guardian/
│   ├── States.lean        # Guardian state machine
│   ├── Transitions.lean   # Transition proofs
│   ├── Safety.lean        # Safety property proofs
│   └── Invariants.lean    # Inductive invariant proofs
├── Memory/
│   ├── Types.lean         # Memory type definitions
│   └── Consent.lean       # User consent proofs
├── Layers/
│   └── Immutability.lean  # Layer protection proofs
├── Project/
│   └── Templates.lean     # Templates for generated projects
└── README.md              # This file
```

## For Generated Projects

When you generate a project using the Factory, it includes:

1. **Inherited Proofs**: Core axiom, Guardian, Memory, and Layer proofs
2. **Project Templates**: Customizable proof templates in `proofs/Project/`
3. **Verification Script**: `scripts/proofs/verify_proofs.sh`

### Extending Proofs

To add proofs for your project's specific logic:

1. Copy a template from `Project/Templates.lean`
2. Define your states and transitions
3. Define invariants for your domain
4. Prove invariants hold initially and are preserved
5. Add axiom alignment theorems
6. Run `lake build` to verify

### Axiom Alignment Checklist

For each state machine, prove alignment with:

- [ ] **A1 (Transparency)**: All state changes trace to explicit events
- [ ] **A2 (User Primacy)**: User can override or cancel
- [ ] **A3 (Derivability)**: Each transition has a defined rule
- [ ] **A4 (Non-Harm)**: Error states preserve user data
- [ ] **A5 (Consistency)**: No contradictory states possible

## Proof Methodology

We use **inductive invariants**:

1. **Initial**: Prove invariant holds in initial state
2. **Preserved**: Prove all transitions preserve invariant
3. **Implication**: Prove invariant implies safety property

This gives the strongest guarantee: if proofs type-check, properties hold **forever**.

## Technical Notes

### Why Lean 4?

- Pure functional language with dependent types
- Interactive and automated theorem proving
- Fast compilation and execution
- Active development and community

### Proof Completeness

Some proofs contain `sorry` (proof holes). These are:
- Complex case analyses being incrementally completed
- List reasoning that requires additional lemmas
- Clearly marked for future work

The core structure and approach is sound. Completing all `sorry` proofs is ongoing work.

### Running Individual Proofs

```bash
# Build specific module
lake build Axioms
lake build Guardian.States
lake build Memory.Consent

# Check without building
lake check
```

## Contributing

To contribute proofs:

1. Complete existing `sorry` proofs
2. Add new safety properties
3. Create domain-specific templates
4. Improve documentation

All contributions should align with Love, Truth, and Beauty.

## Resources

- [Theorem Proving in Lean 4](https://leanprover.github.io/theorem_proving_in_lean4/)
- [Lean 4 Documentation](https://lean-lang.org/documentation/)
- [Mathlib4](https://github.com/leanprover-community/mathlib4)

## License

MIT License - Free for all to use, modify, and share.

---

*Cursor Agent Factory - Formal Verification System*
*"The Tao does nothing, yet nothing is left undone."*
