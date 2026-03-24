# AI-Guardrail Pipeline 

A GitHub Actions CI/CD pipeline for Android that uses GitHub's AI models to scan source code for security violations before building, and automatically sends AI-powered incident reports to Slack when builds fail.

---

##  Architecture ![Architecture](architecture/architecture-diagram.gif).
```



---

##  Features

- **AI Code Scanning** — automatically scans up to 20 source files before every build, checking for:
  - Hardcoded secrets or API keys
  - Insecure permissions
  - Sensitive PII in logs
  - Policy violations

- **Smart Caching** — five layers of caching to speed up pipelines:
  - pip dependencies
  - Scan results (skips re-scan if source files unchanged)
  - Gradle wrapper
  - Gradle dependencies
  - Android SDK packages
  - Android build outputs

- **Android Build** — compiles a debug APK using Gradle with parallel builds and build cache enabled

- **AI Incident Reports** — when a build fails, GPT-4o analyses the full build log and sends a Slack notification with:
  - Root cause in one sentence
  - Exact fix with commands
  - How to prevent it in future
  - Link to the failed run

---

##  Setup

### 1. Clone the repo
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
│       └── AI-Guardrail-Pipeline.yml  # Main CI/CD pipeline
├── app/
│   ├── build.gradle                   # App-level Gradle config
│   └── src/
│       └── main/
│           ├── AndroidManifest.xml
│           └── java/com/example/aiguardrail/
│               └── MainActivity.kt
├── build.gradle                       # Root Gradle config
├── settings.gradle                    # Gradle project settings
├── gradlew                            # Gradle wrapper (Unix)
├── gradlew.bat                        # Gradle wrapper (Windows)
└── README.md
```

---

##  Pipeline Jobs

### Job 1: `scan-text`
| Step | Description |
|------|-------------|
| Checkout | Clones the repository |
| Set up Python | Installs Python 3.11 |
| Cache pip | Caches openai package |
| Install dependencies | Installs openai SDK |
| Cache scan results | Skips scan if sources unchanged |
| AI guardrail scan | Sends code to GPT-4o for analysis |
| Enforce cached result | Blocks build if cached scan previously failed |

### Job 2: `build-android`
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

##  Slack Incident Report

When a build fails, the pipeline automatically sends a message to Slack:
```
 Android Build Failed – AI Incident Report

Repo:          Cloud-Architect-Emma/AI-Guardrail
Branch:        main
Triggered by:  Cloud-Architect-Emma
Run:           View logs

 AI Analysis & Fix:
Root cause: The assembleDebug task was not found because the app
module was not included in settings.gradle.

Fix: Add include ':app' to settings.gradle.

Prevention: Always verify settings.gradle includes all modules
before pushing. Add a Gradle validation step to your pipeline.
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

##  Security

- No API keys or secrets are hardcoded in the codebase
- All sensitive values are stored as GitHub Actions secrets
- The AI scan runs before every build to catch accidental secret commits
- `local.properties` is gitignored to prevent SDK paths leaking

---

##  Requirements

- Android SDK 34
- JDK 17
- Gradle 9.4.1
- Python 3.11 (CI only)
- Slack workspace with incoming webhooks enabled

---

##  Author

**Cloud-Architect-Emma**  
GitHub: [@Cloud-Architect-Emma](https://github.com/Cloud-Architect-Emma)
