# AI-Guardrail Pipeline 

![CI](https://github.com/Cloud-Architect-Emma/AI-Guardrail/actions/workflows/AI-Guardrail-Pipeline.yml/badge.svg)
![License](https://img.shields.io/github/license/Cloud-Architect-Emma/AI-Guardrail)
![Last Commit](https://img.shields.io/github/last-commit/Cloud-Architect-Emma/AI-Guardrail)
![Repo Size](https://img.shields.io/github/repo-size/Cloud-Architect-Emma/AI-Guardrail)

A **GitHub Actions CI/CD pipeline for Android** that integrates GitHub's AI models to scan source code for security violations **before building**, and automatically sends **AI-powered incident reports to Slack** when builds fail.

---

##  Architecture

![AI Guardrail Pipeline Architecture](architecture/architecture-diagram-(1).gif)
```
Developer Push
      │
      ▼
GitHub Repository
      │
      ▼
GitHub Actions Pipeline
      │
      ├──  AI Security Scan
      ├──  Policy Engine (Policy-as-Code)
      ├──  Build Android APK
      └──  Failure Analysis
                    │
                    ▼
             GPT-4o Analysis
                    │
                    ▼
               Slack Alert
```

---

##  Features

###  AI Security Guardrails
Automatically scans up to 20 source files before every build to detect:
- Hardcoded secrets or API keys
- Insecure permissions
- Sensitive PII in logs
- Policy violations (via `policies/` folder)

###  Smart Multi-Layer Caching
Six caching layers dramatically reduce CI runtime:
- pip dependencies
- Scan results (skips re-scan if sources unchanged)
- Gradle wrapper
- Gradle dependencies
- Android SDK packages
- Android build outputs

###  AI Incident Reporting
When a build fails, GPT-4o analyses the build logs and sends a Slack alert containing:
- Root cause in one sentence
- Exact fix with commands
- Prevention strategy
- Link to the failed workflow run

###  Android Build Automation
Compiles a debug APK using Gradle with:
- Parallel builds
- Gradle build cache
- Full dependency caching

---

##  Setup

### 1. Clone the repository
```bash
git clone https://github.com/Cloud-Architect-Emma/AI-Guardrail.git
cd AI-Guardrail
```

### 2. Add GitHub Secrets
Go to **Settings → Secrets and variables → Actions** and add:

| Secret | Description |
|--------|-------------|
| `SLACK_WEBHOOK_URL` | Slack incoming webhook URL for incident reports |

> `GITHUB_TOKEN` is automatic — no setup needed.

### 3. Set up Slack Webhook
1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
2. Create New App → From scratch
3. Enable **Incoming Webhooks**
4. Add New Webhook to Workspace → pick your channel
5. Copy the webhook URL and add it as `SLACK_WEBHOOK_URL` secret

### 4. Push to main
```bash
git push origin main
```

The pipeline triggers automatically on every push and pull request to `main`.

---

##  Project Structure
```
AI-Guardrail/
├── .github/
│   └── workflows/
│       └── AI-Guardrail-Pipeline.yml   # Main CI/CD pipeline
├── architecture/
│   └── architecture-diagram.gif        # Pipeline architecture diagram
├── app/
│   ├── build.gradle                    # App-level Gradle config
│   └── src/main/
│       ├── AndroidManifest.xml
│       └── java/com/example/aiguardrail/
│           └── MainActivity.kt
├── policies/
│   ├── secrets-policy.yaml             # Secrets detection rules
│   ├── logging-policy.yaml             # PII logging rules
│   ├── permissions-policy.yaml         # Android permission rules
│   └── android-security-policy.yaml    # General security rules
├── build.gradle                        # Root Gradle config
├── settings.gradle                     # Gradle project settings
├── gradlew                             # Gradle wrapper (Unix)
├── gradlew.bat                         # Gradle wrapper (Windows)
└── README.md
```

---

##  Pipeline Jobs

### Job 1: `scan-text` — AI Security Scan

| Step | Description |
|------|-------------|
| Checkout | Clones the repository |
| Set up Python | Installs Python 3.11 |
| Cache pip | Caches openai package |
| Install dependencies | Installs OpenAI SDK |
| Cache scan results | Skips scan if sources unchanged |
| AI guardrail scan | Sends code to GPT-4o for analysis |
| Policy enforcement | Blocks build if scan or policy fails |

### Job 2: `build-android` — Android Build

| Step | Description |
|------|-------------|
| Checkout | Clones the repository |
| Set up JDK 17 | Installs Temurin JDK 17 |
| Set up Android SDK | Installs Android SDK via android-actions |
| Cache Gradle wrapper | Caches Gradle wrapper JAR |
| Cache Gradle deps | Caches all Gradle dependencies |
| Cache Android SDK | Caches SDK platforms and build tools |
| Cache build outputs | Caches compiled intermediates |
| Build debug APK | Runs `./gradlew :app:assembleDebug` |
| AI Slack notification | Sends incident report to Slack on failure |
| Upload APK | Uploads APK as workflow artifact |

---

##  Slack Incident Report Example
```
 Android Build Failed — AI Incident Report
─────────────────────────────────────────────
Repository:    Cloud-Architect-Emma/AI-Guardrail
Branch:        main
Triggered by:  Cloud-Architect-Emma
Run:           View logs ↗
─────────────────────────────────────────────
 AI Analysis & Fix:

Root Cause:
The assembleDebug task was not found because the app module
was not included in settings.gradle.

Fix:
Add the following line to settings.gradle:
  include ':app'

Prevention:
Validate Gradle module configuration before pushing changes.
```

---

##  Local Development
```bash
# Build locally
./gradlew :app:assembleDebug

# Clean build
./gradlew clean :app:assembleDebug

# List available tasks
./gradlew tasks
```

---

##  Pipeline Performance

| Optimisation | Impact |
|-------------|--------|
| pip cache | ~40% faster dependency install |
| Scan cache | Avoids rescanning unchanged files |
| Gradle wrapper cache | Saves ~20 seconds |
| Gradle dependency cache | Saves ~60 seconds |
| Android SDK cache | Saves ~90 seconds |
| Build output cache | Faster incremental rebuilds |

> **Baseline pipeline time:** ~9 minutes  
> **Optimised pipeline time:** ~3.5 minutes (**61% faster**)

---

##  Security

- No API keys or secrets are hardcoded in the codebase
- All sensitive values stored as GitHub Actions secrets
- AI scan runs before every build to catch accidental secret commits
- `local.properties` is gitignored to prevent SDK paths leaking
- Least privilege permissions declared per job

---

##  Requirements

- Android SDK 34
- JDK 17
- Gradle 9.4.1
- Python 3.11 (CI only)
- Slack workspace with incoming webhooks enabled

---

##  Author

**Emmanuela Opurum**  
Solutions Architect | Cloud Engineer

[![GitHub](https://img.shields.io/badge/GitHub-Cloud--Architect--Emma-181717?logo=github)](https://github.com/Cloud-Architect-Emma)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?logo=linkedin)](https://www.linkedin.com/in/cloud-architect-emma/)
