# Continuous Integration & Continuous Delivery (CI/CD) Workflow

## Overview
This platform implements an enterprise software delivery lifecycle (SDLC) split into **Shift-Left CI** and **Harness Release Governance CD**.

---

## 1. Shift-Left Continuous Integration (CI)

The CI pipeline runs automatically on every `git push` to `main` via GitHub Actions Cloud VM runners.

### Stage Breakdown

| Stage | Tool | Command / Action | Objective |
| :--- | :--- | :--- | :--- |
| **Unit Testing** | `pytest` | `python -m pytest -v` | Validates API endpoint contracts (`/`, `/health`, `/version`) |
| **Dependency Audit** | `pip-audit` | `pip-audit -r requirements.txt` | Audits third-party PyPI dependencies against known CVEs |
| **Security Scan** | `Trivy` | `aquasecurity/trivy-action` | Scans repository files for exposed secrets & critical vulnerabilities |
| **Immutable Build** | `docker` | `docker build -t harness-demo:<git-sha> .` | Generates immutable container artifact tagged with Git SHA |

---

## 2. Harness Continuous Delivery (CD) & Release Governance

Harness acts as the enterprise control plane orchestrating environment promotion and executive governance.

### Stage Breakdown

```yaml
Pipeline: harness-delegate-ci-pipeline
├── Stage 1: DEV Deployment Verification
│     └── Step: ShellScript (HTTP /health probe verification)
├── Stage 2: Executive Approval Gate
│     └── Step: HarnessApproval (Senior Director Signoff Required)
└── Stage 3: PROD Deployment Verification
      └── Step: ShellScript (HTTP /health & /version probe verification)
```

### Stage 1: DEV Deployment Verification
* **Type**: Custom / ShellScript execution
* **Objective**: Verifies that the deployed microservice in DEV responds with HTTP 200 OK and `{"status": "healthy"}`.

### Stage 2: Executive Approval Gate
* **Type**: `HarnessApproval` Step
* **Objective**: Enforces SecOps & Executive governance. The release pauses until an authorized approver reviews execution history and signs off inside Harness UI.
* **Security Controls**: Supports `disallowPipelineExecutor` to enforce Segregation of Duties (SoD).

### Stage 3: PROD Deployment Verification
* **Type**: Custom / ShellScript execution
* **Objective**: Verifies post-deployment operational health (`/health`) and version metadata (`/version`). Triggers automated rollback if health probes fail.
