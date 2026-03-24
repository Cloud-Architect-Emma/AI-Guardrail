# AI-Guardrail Pipeline

![CI](https://github.com/Cloud-Architect-Emma/AI-Guardrail/actions/workflows/AI-Guardrail-Pipeline.yml/badge.svg)
![License](https://img.shields.io/github/license/Cloud-Architect-Emma/AI-Guardrail)
![Last Commit](https://img.shields.io/github/last-commit/Cloud-Architect-Emma/AI-Guardrail)
![Repo Size](https://img.shields.io/github/repo-size/Cloud-Architect-Emma/AI-Guardrail)

A **GitHub Actions CI/CD pipeline for Android** that integrates GitHub’s AI models to scan source code for security violations **before building**, and automatically sends **AI-powered incident reports to Slack** when builds fail.  

---

## Architecture

![AI Guardrail Pipeline Architecture](architecture/architecture-diagram.gif)

**Pipeline Overview:**

```text
Developer Push
      │
      ▼
GitHub Repository
      │
      ▼
GitHub Actions Pipeline
      │
      ├── AI Security Scan
      ├── Policy Engine (Policy-as-Code)
      ├── Build Android APK
      └── Failure Analysis
               │
               ▼
          GPT-4o Analysis
               │
               ▼
            Slack Alert
Features
AI Security Guardrails

Automatically scans up to 20 source files before every build to detect:

Hardcoded secrets or API keys
Insecure permissions
Sensitive PII in logs
Policy violations (via policies/ folder)
Smart Multi-Layer Caching

Six caching layers dramatically reduce CI runtime:

pip dependencies
scan results (skips re-scan if sources unchanged)
Gradle wrapper
Gradle dependencies
Android SDK packages
Android build outputs
Android Build Automation

Compiles a debug APK using Gradle with:

parallel builds
Gradle build cache
dependency caching
AI Incident Reporting

When a build fails, GPT-4o analyzes the build logs and sends a Slack alert containing:

root cause in one sentence
exact fix with commands
prevention strategy
link to the failed workflow
Setup
1. Clone the repository
git clone https://github.com/Cloud-Architect-Emma/AI-Guardrail.git
cd AI-Guardrail
2. Add GitHub Secrets

Go to Settings → Secrets and variables → Actions and add:

Secret	Description
SLACK_WEBHOOK_URL	Slack incoming webhook URL for incident reports

GITHUB_TOKEN is automatic — no setup needed.

3. Set up Slack Webhook
Go to Slack API Apps
Create New App → From scratch
Enable Incoming Webhooks
Add New Webhook to Workspace → pick your channel
Copy the webhook URL and add it as SLACK_WEBHOOK_URL secret
4. Push to main
git push origin main

The pipeline triggers automatically on every push and pull request to main.

Project Structure
AI-Guardrail/
├── .github/
│   └── workflows/
│       └── AI-Guardrail-Pipeline.yml
├── architecture/
│   └── architecture-diagram.gif
├── app/
│   ├── build.gradle
│   └── src/main/
│       ├── AndroidManifest.xml
│       └── java/com/example/aiguardrail/
│           └── MainActivity.kt
├── policies/
│   ├── secrets-policy.yaml
│   ├── logging-policy.yaml
│   ├── permissions-policy.yaml
│   └── android-security-policy.yaml
├── build.gradle
├── settings.gradle
├── gradlew
├── gradlew.bat
└── README.md

Pipeline Jobs
1. scan-text
Step	Description
Checkout	Clones the repository
Set up Python	Installs Python 3.11
Cache pip	Caches openai package
Install dependencies	Installs OpenAI SDK
Cache scan results	Skips scan if sources unchanged
AI guardrail scan	Sends code to GPT-4o for analysis
Policy enforcement	Blocks build if scan or policy fails

2. build-android
Step	Description
Checkout	Clones the repository
Set up JDK 17	Installs Temurin JDK 17
Set up Android SDK	Installs Android SDK via android-actions
Cache Gradle wrapper	Caches Gradle wrapper JAR
Cache Gradle deps	Caches all Gradle dependencies
Cache Android SDK	Caches SDK platforms and build tools
Cache build outputs	Caches compiled intermediates
Build debug APK	Runs ./gradlew :app:assembleDebug
AI Slack notification	Sends incident report to Slack on failure
Upload APK	Uploads APK as workflow artifact
Slack Incident Report Example
Android Build Failed — AI Incident Report

Repository: Cloud-Architect-Emma/AI-Guardrail
Branch: main
Triggered by: Cloud-Architect-Emma

AI Analysis
Root Cause:
The assembleDebug task was not found because the app module
was not included in settings.gradle.

Fix:
Add the following line to settings.gradle:
include ':app'

Prevention:
Validate Gradle module configuration before pushing changes.
Local Development
# Build locally
./gradlew :app:assembleDebug

# Clean build
./gradlew clean :app:assembleDebug

# List available tasks
./gradlew tasks
Pipeline Performance
Optimization	Impact
pip cache	40% faster dependency install
scan cache	avoids rescanning unchanged files
Gradle wrapper cache	saves ~20 seconds
Gradle dependency cache	saves ~60 seconds
Android SDK cache	saves ~90 seconds
build output cache	faster rebuilds

Baseline pipeline time: 9 minutes
Optimized pipeline time: 3.5 minutes (~61% faster)

Security
No API keys or secrets are hardcoded
All sensitive values stored as GitHub Actions secrets
AI scan runs before every build to catch accidental secret commits
local.properties is gitignored to prevent SDK paths leaking
Requirements
Android SDK 34
JDK 17
Gradle 9.4.1
Python 3.11 (CI only)
Slack workspace with incoming webhooks enabled
Author

Emmanuela Opurum
Solutions Architect | Cloud Engineer

GitHub: @Cloud-Architect-Emma
