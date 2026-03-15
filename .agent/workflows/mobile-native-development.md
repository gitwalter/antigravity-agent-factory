---
name: mobile-native-development
description: Comprehensive workflow for Mobile Native (iOS/Android) development from initialization to store deployment.
version: 1.0.0
type: pipeline
domain: universal
agents:
  - mobile-specialist
blueprints:
  - mobile-native-app
steps:
  - name: Initialization
    description: Initialize project using platform-specific CLI (e.g., xcodebuild or gradle init).
  - name: Configuration
    description: Configure mandatory ignore rules for build artifacts (.gitignore, .cursorignore).
  - name: Dependency Management
    description: Setup dependency management (CocoaPods/Swift Package Manager for iOS, Gradle for Android).
  - name: Implementation
    description: Implement core architecture (MVVM/Coordinator) and UI components.
  - name: Unit Testing
    description: Run unit tests using platform runner (xctest or ./gradlew test).
  - name: UI Testing
    description: Perform UI tests on simulator/emulator.
  - name: Static Analysis
    description: Execute linting and static analysis (swiftlint or ktlint).
  - name: Packaging
    description: Package for distribution (Archive .ipa or Build .apk/.aab).
  - name: Signing
    description: Verify signing and provisioning profiles.
  - name: Submission
    description: Submit to App Store Connect or Google Play Console via automated pipelines.
---

# Mobile Native Development Workflow

**Version:** 1.0.0

**Goal:** Guide the development of high-quality native applications for iOS and Android.

## Trigger Conditions
- New mobile application project initialized.
- Feature request for an existing mobile app.
- Preparation for a new App Store or Play Store release.

**Trigger Examples:**
- "Initialize a new iOS app using Swift and SwiftUI."
- "Implement the login screen for the Android application."
- "Run unit tests and linting for the mobile module."
- "Package and submit the latest version to App Store Connect."

## Phases

### 1. Project Initialization
Setup the base project and environment.
- **Agent**: `mobile-specialist`
- **Action**: Run platform-specific init commands; configure `.gitignore`.

### 2. Implementation
Develop functionality and UI components.
- **Action**: Build features using MVVM/Coordinator patterns.

### 3. Testing & Analysis
Verify code quality and performance.
- **Action**: Execute `xctest` or `./gradlew test` and run static analysis tools.

### 4. Release Preparation
Package and sign artifacts for distribution.
- **Action**: Build `.ipa` or `.apk/.aab` files; verify provisioning/signing.

## Best Practices
- **Performance**: Monitor main thread usage and optimize image assets.
- **Accessibility**: Support Dynamic Type and VoiceOver/TalkBack.
- **Security**: Use Keychain or EncryptedSharedPreferences for sensitive data.

## Related Workflows
- `fastapi-api-development.md` - Backend for mobile apps.
- `release-management.md` - Global versioning and release.
