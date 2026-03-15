---
name: mobile-native-build
version: 1.0.0
type: skill
description: Skills for orchestrating native mobile builds for iOS and Android.
category: verification
agents:
- mobile-specialist
knowledge:
- mobile-patterns.json
tools:
- name: run_native_build
  type: factory
  description: Executes a native build (xcodebuild or gradle).
---

# Mobile Native Build Skill

## When to Use
Use this skill to automate the building of native iOS and Android applications, ensuring that environmental configurations and dependencies are correctly resolved.

## Prerequisites
- Native build environment (Xcode for iOS, Android Studio/SDK for Android).
- Validated `mobile-patterns.json` Knowledge Item.
- Access to the repository containing the mobile source code.

## Process
1. **Configure Environment**: Set the necessary environment variables and paths.
2. **Clean Project**: Run `clean` commands to ensure a fresh build.
3. **Trigger Build**: Use the `run_native_build` tool for the target platform.
4. **Collect Artifacts**: Safeguard the resulting `.ipa` or `.apk` files.

## Best Practices
- **Dependency Isolation**: Use dependency managers like CocoaPods or Gradle to manage external libraries.
- **Uniform Environments**: Use consistent build agents to avoid "works on my machine" issues.
- **Fast Fail**: Configure builds to stop immediately on the first error.
