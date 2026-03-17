---
agents:
- mobile-specialist
- '@Architect'
blueprints:
- universal
description: Antigravity workflow for mobile-native-development. Standardized for
  IDX Visual Editor.
domain: universal
name: mobile-native-development
steps:
- actions:
  - Run platform-specific init commands; configure `.gitignore`.
  agents:
  - mobile-specialist
  goal: ''
  name: Project Initialization
  skills: []
  tools: []
- actions:
  - Build features using MVVM/Coordinator patterns.
  agents:
  - '@Architect'
  goal: ''
  name: Implementation
  skills: []
  tools: []
- actions:
  - Execute `xctest` or `./gradlew test` and run static analysis tools.
  agents:
  - '@Architect'
  goal: ''
  name: Testing & Analysis
  skills: []
  tools: []
- actions:
  - '**Performance**: Monitor main thread usage and optimize image assets.'
  - '**Accessibility**: Support Dynamic Type and VoiceOver/TalkBack.'
  - '**Security**: Use Keychain or EncryptedSharedPreferences for sensitive data.'
  - '`fastapi-api-development.md` - Backend for mobile apps.'
  - '`committing-releases.md` - Global versioning and release.'
  - '"Execute mobile-native-development.md"'
  - Build `.ipa` or `.apk/.aab` files; verify provisioning/signing.
  agents:
  - '@Architect'
  goal: ''
  name: Release Preparation
  skills: []
  tools: []
tags: []
type: sequential
version: 2.0.0
---
# Mobile Native Development

**Version:** 1.0.0

## Overview
Antigravity workflow for native mobile application development (iOS/Android). Standardized for IDX Visual Editor.

## Trigger Conditions
- Requirement for a new native mobile application or a major feature update.
- Need for platform-specific UI/UX and hardware integrations.
- User request: `/mobile-native-development`.

**Trigger Examples:**
- "Initialize a new React Native project for the 'Warehouse Manager' app."
- "Implement the 'Offline Sync' feature for the Android inventory application."

## Phases

### 1. Project Initialization
- **Goal**: Initial project setup and environment configuration.
- **Agents**: `mobile-specialist`
- **Actions**:
- Run platform-specific init commands; configure `.gitignore`.

### 2. Implementation
- **Goal**: Build application features and UI components.
- **Agents**: `@Architect`
- **Actions**:
- Build features using MVVM/Coordinator patterns.

### 3. Testing & Analysis
- **Goal**: Verify code quality and application stability.
- **Agents**: `@Architect`
- **Actions**:
- Execute `xctest` or `./gradlew test` and run static analysis tools.

### 4. Release Preparation
- **Goal**: Prepare application for distribution and production.
- **Agents**: `@Architect`
- **Actions**:
- **Performance**: Monitor main thread usage and optimize image assets.
- **Accessibility**: Support Dynamic Type and VoiceOver/TalkBack.
- **Security**: Use Keychain or EncryptedSharedPreferences for sensitive data.
- `fastapi-api-development.md` - Backend for mobile apps.
- `committing-releases.md` - Global versioning and release.
- "Execute mobile-native-development.md"
- Build `.ipa` or `.apk/.aab` files; verify provisioning/signing.
