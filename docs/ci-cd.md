# Continuous Integration & Continuous Delivery (CI/CD) Workflow

## Overview
This platform implements an enterprise software delivery lifecycle (SDLC) with explicit architectural separation between **Continuous Integration (CI)** and **Continuous Delivery (CD)** across Development and Production environments.

---

## 1. Multi-Stage Decoupled Pipeline Architecture

```yaml
Pipeline: harness-decoupled-ci-cd-pipeline / github-ci-cd-workflow
├── Stage 1: Continuous Integration (CI Stage)
│     ├── Step 1: Run Unit Tests (pytest -v)
│     ├── Step 2: Dependency Security Audit (pip-audit)
│     ├── Step 3: Repository Filesystem Scan (Bandit SAST / Trivy)
│     ├── Step 4: Build & Push Immutable Docker Image (sourabh5050/harness-demo:<git-sha>)
│     └── Step 5: Container Hardening Audit (grep "USER appuser" Dockerfile)
├── Stage 2: Continuous Delivery (CD Stage - DEV Environment)
│     ├── Step 1: Pick up Container Tag & Trigger DEV Deployment
│     └── Step 2: Execute DEV Live Health & Version Verification Probes
├── Stage 3: Approval Gate
│     └── Step: Production Promotion Sign-off (HarnessApproval / GitHub Environment Approval)
└── Stage 4: Continuous Delivery (CD Stage - PROD Environment)
      ├── Step 1: Execute Live Health Verification Probe (curl -f .../health)
      └── Step 2: Execute Live Version Verification Probe (curl -f .../version)
```

---

## 2. Stage Breakdown & Execution Details

### Stage 1: Continuous Integration (CI Stage)
- **Step 1 (`Run Unit Tests`)**: Executes `pytest -v` against API endpoints (`/`, `/health`, `/version`).
- **Step 2 (`Dependency Security Audit`)**: Executes `pip-audit` to detect CVE vulnerabilities in Python dependencies before container creation.
- **Step 3 (`Repository Security Scan`)**: Executes `Bandit` / `Trivy` SAST scanning Python source code AST for security misconfigurations.
- **Step 4 (`Build Docker Image`)**: Builds `sourabh5050/harness-demo:${COMMIT_SHA}` & `:latest`, authenticates with Docker Hub using Harness Secret Manager (`account.docker_hub_pat`), and pushes immutable tags to Docker Hub.
- **Step 5 (`Container Hardening Audit`)**: Audits `Dockerfile` verifying non-root system user posture (`USER appuser` UID 10001).

### Stage 2: Continuous Delivery (CD Stage - DEV)
- **Objective**: As soon as the CI stage completes and pushes the immutable image tag to the registry, Stage 2 automatically triggers to deploy to the **Development (DEV)** environment.
- **Verification**: Runs automated live `/health` and `/version` probes against DEV.

### Stage 3: Approval Gate
- **Type**: `HarnessApproval` Step inside an `Approval` Stage.
- **Objective**: Enforces release governance. Execution pauses after successful DEV deployment and verification, requiring sign-off before promoting to Production.

### Stage 4: Continuous Delivery (CD Stage - PROD)
- **Step 1 (`Execute Live Health Verification Probe`)**: Hits live production HTTPS endpoint (`https://harness-demo-dev.onrender.com/health`) with automated retries, asserting HTTP `200 OK` and `{"status": "healthy"}`.
- **Step 2 (`Execute Live Version Verification Probe`)**: Hits live production HTTPS endpoint (`https://harness-demo-dev.onrender.com/version`), asserting HTTP `200 OK` and Git commit metadata matching `"version":"1.0.0"`.

