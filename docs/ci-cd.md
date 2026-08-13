# Continuous Integration & Continuous Delivery (CI/CD) Workflow

## Overview
This platform implements an enterprise software delivery lifecycle (SDLC) unified inside **Harness Platform** using a self-hosted **Kubernetes/Docker Delegate**, **Docker Hub Registry**, **Render Web Service**, and **Live HTTPS Verification Probes**.

---

## 1. Complete Harness CI/CD Pipeline Architecture

```yaml
Pipeline: harness-delegate-ci-pipeline
├── Stage 1: Shift-Left Quality Security and Build Stage (Custom Stage)
│     ├── Step 1: Run Unit Tests (pytest -v)
│     ├── Step 2: Dependency Security Audit (pip-audit)
│     ├── Step 3: Repository Filesystem Scan (Bandit SAST -s B104)
│     ├── Step 4: Build & Push Immutable Docker Image (sourabh5050/harness-demo:<git-sha>)
│     └── Step 5: Container Image Security Scan (grep "USER appuser" Dockerfile)
├── Stage 2: Executive Approval Gate (Approval Stage)
│     └── Step: Production Promotion Approval (HarnessApproval - account._account_all_users)
└── Stage 3: Continuous Delivery and Live Verification Stage (Custom Stage)
      ├── Step 6: Execute Live Health Verification Probe (curl -f .../health)
      └── Step 7: Execute Live Version Verification Probe (curl -f .../version)
```

---

## 2. Stage Breakdown & Execution Details

### Stage 1: Shift-Left Quality Security and Build Stage
- **Step 1 (`Run Unit Tests`)**: Executes `pytest -v` against API endpoints (`/`, `/health`, `/version`).
- **Step 2 (`Dependency Security Audit`)**: Executes `pip-audit` to detect CVE vulnerabilities in Python dependencies before container creation.
- **Step 3 (`Repository Filesystem Scan`)**: Executes `Bandit` SAST scanning Python source code AST for security misconfigurations.
- **Step 4 (`Build Docker Image`)**: Injects static Docker CLI (`docker-24.0.7`), builds `sourabh5050/harness-demo:${COMMIT_SHA}` & `:latest`, authenticates with Docker Hub using Harness Secret Manager (`account.docker_hub_pat`), and pushes immutable tags to Docker Hub.
- **Step 5 (`Container Image Security Scan`)**: Audits `Dockerfile` verifying non-root system user posture (`USER appuser` UID 10001).

### Stage 2: Executive Approval Gate
- **Type**: `HarnessApproval` Step inside an `Approval` Stage.
- **Objective**: Enforces SecOps & Executive Governance. The pipeline pauses execution after successful CI build, allowing DevOps Leads / Managers to review security audit logs in Harness UI before approving promotion to Production.

### Stage 3: Continuous Delivery and Live Verification Stage
- **Step 6 (`Execute Live Health Verification Probe`)**: Hits live production HTTPS endpoint (`https://harness-demo-dev.onrender.com/health`) with automated retries, asserting HTTP `200 OK` and `{"status": "healthy"}`.
- **Step 7 (`Execute Live Version Verification Probe`)**: Hits live production HTTPS endpoint (`https://harness-demo-dev.onrender.com/version`), asserting HTTP `200 OK` and Git commit metadata matching `"version":"1.0.0"`.
