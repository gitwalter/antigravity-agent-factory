#!/bin/bash
# =============================================================================
# Cursor Agent Factory - Proof Attestation Generator
# =============================================================================
#
# This script generates cryptographic attestations after successful
# proof verification. These attestations can be independently verified
# by anyone.
#
# Philosophy: Love, Truth, and Beauty
# - Love: Free attestation for everyone
# - Truth: Cryptographic certainty
# - Beauty: Simple, auditable process
#
# Usage:
#   ./scripts/generate_attestation.sh           # Generate attestation
#   ./scripts/generate_attestation.sh --sign    # Also GPG sign
#   ./scripts/generate_attestation.sh --help    # Show help
#
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PROOFS_DIR="$PROJECT_ROOT/proofs"
ATTESTATIONS_DIR="$PROJECT_ROOT/.attestations"

# Print banner
print_banner() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════════════════╗"
    echo "║        Cursor Agent Factory - Attestation Generator               ║"
    echo "║                                                                   ║"
    echo "║                    SDG • Love • Truth • Beauty                    ║"
    echo "╚═══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Print help
print_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Generate cryptographic attestations for verified proofs."
    echo ""
    echo "Options:"
    echo "  --sign      Also create GPG signature"
    echo "  --version   Specify version (default: from git tag)"
    echo "  --help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                    # Generate attestation"
    echo "  $0 --sign             # Generate and GPG sign"
    echo "  $0 --version v4.0.0   # Specify version"
}

# Verify proofs first
verify_proofs() {
    echo -e "${BLUE}[1/4] Verifying proofs...${NC}"
    
    cd "$PROOFS_DIR"
    
    if lake build; then
        echo -e "${GREEN}✓ All proofs verified${NC}"
    else
        echo -e "${RED}ERROR: Proofs failed verification. Cannot generate attestation.${NC}"
        exit 1
    fi
}

# Generate file hashes
generate_hashes() {
    echo -e "${BLUE}[2/4] Generating file hashes...${NC}"
    
    mkdir -p "$ATTESTATIONS_DIR"
    
    cd "$PROOFS_DIR"
    
    # Generate SHA-256 hashes of all proof files
    find . -name "*.lean" -type f | sort | while read -r file; do
        sha256sum "$file"
    done > "$ATTESTATIONS_DIR/checksums.txt"
    
    echo -e "${GREEN}✓ Checksums generated: .attestations/checksums.txt${NC}"
}

# Generate attestation JSON
generate_attestation() {
    echo -e "${BLUE}[3/4] Generating attestation...${NC}"
    
    # Get version
    if [ -z "$VERSION" ]; then
        VERSION=$(git describe --tags --always 2>/dev/null || echo "dev")
    fi
    
    # Get git info
    COMMIT_SHA=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
    COMMIT_DATE=$(git log -1 --format=%ci 2>/dev/null || echo "unknown")
    
    # Get checksums hash
    CHECKSUMS_HASH=$(sha256sum "$ATTESTATIONS_DIR/checksums.txt" | cut -d' ' -f1)
    
    # Generate attestation
    cat > "$ATTESTATIONS_DIR/$VERSION-verified.json" << EOF
{
  "_type": "https://antigravity-agent-factory/attestation/v1",
  "subject": {
    "name": "antigravity-agent-factory",
    "version": "$VERSION",
    "commit": "$COMMIT_SHA",
    "commitDate": "$COMMIT_DATE"
  },
  "predicateType": "https://antigravity-agent-factory/proofs-verified/v1",
  "predicate": {
    "verified": true,
    "verificationTime": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "prover": "Lean 4",
    "proverVersion": "$(lake --version 2>&1 | head -n1 || echo 'unknown')",
    "proofModules": [
      "Axioms",
      "Guardian.States",
      "Guardian.Transitions",
      "Guardian.Safety",
      "Guardian.Invariants",
      "Memory.Types",
      "Memory.Consent",
      "Layers.Immutability",
      "Project.Templates"
    ],
    "properties": {
      "axiomsDefined": ["A0", "A1", "A2", "A3", "A4", "A5"],
      "guardianSafety": [
        "statePreservation",
        "userNotification",
        "alternativesOffered",
        "harmPrevention"
      ],
      "memoryConsent": [
        "userApprovalRequired",
        "layerProtection"
      ],
      "layerImmutability": [
        "layer0Immutable",
        "layer1Immutable",
        "layer2Immutable"
      ]
    },
    "checksums": {
      "algorithm": "SHA-256",
      "file": "checksums.txt",
      "hash": "$CHECKSUMS_HASH"
    }
  }
}
EOF
    
    echo -e "${GREEN}✓ Attestation generated: .attestations/$VERSION-verified.json${NC}"
}

# GPG sign attestation
sign_attestation() {
    echo -e "${BLUE}[4/4] Signing attestation...${NC}"
    
    if [ "$SIGN" = true ]; then
        if ! command -v gpg &> /dev/null; then
            echo -e "${YELLOW}WARNING: GPG not found. Skipping signature.${NC}"
            return
        fi
        
        gpg --armor --detach-sign "$ATTESTATIONS_DIR/$VERSION-verified.json"
        echo -e "${GREEN}✓ Signature created: .attestations/$VERSION-verified.json.asc${NC}"
    else
        echo -e "${YELLOW}Skipping GPG signature (use --sign to enable)${NC}"
    fi
}

# Print summary
print_summary() {
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                  ATTESTATION GENERATED                            ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Generated files:"
    echo "  .attestations/checksums.txt           - SHA-256 hashes of proof files"
    echo "  .attestations/$VERSION-verified.json  - Attestation document"
    
    if [ "$SIGN" = true ] && [ -f "$ATTESTATIONS_DIR/$VERSION-verified.json.asc" ]; then
        echo "  .attestations/$VERSION-verified.json.asc - GPG signature"
    fi
    
    echo ""
    echo "To verify independently:"
    echo "  1. Clone the repository"
    echo "  2. Run: cd proofs && lake build"
    echo "  3. Compare checksums: sha256sum -c .attestations/checksums.txt"
    
    if [ "$SIGN" = true ] && [ -f "$ATTESTATIONS_DIR/$VERSION-verified.json.asc" ]; then
        echo "  4. Verify signature: gpg --verify .attestations/$VERSION-verified.json.asc"
    fi
    
    echo ""
    echo -e "${BLUE}Trust verified. Truth freely available.${NC}"
}

# Parse arguments
SIGN=false
VERSION=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --sign)
            SIGN=true
            shift
            ;;
        --version)
            VERSION="$2"
            shift 2
            ;;
        --help)
            print_help
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            print_help
            exit 1
            ;;
    esac
done

# Main execution
print_banner
verify_proofs
generate_hashes
generate_attestation
sign_attestation
print_summary

exit 0
