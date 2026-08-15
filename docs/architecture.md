# Enterprise Cloud Delivery Platform — System Architecture Specification

## Executive Summary
This document specifies the technical architecture for the **Enterprise Cloud Delivery Platform**, built using **Harness Platform**, **Harness Kubernetes/Docker Delegate**, **Docker Hub Registry**, **Render Web Service**, and **Python Flask Microservices**. 

The platform is designed around three core principles:
1. **Shift-Left Security & Quality**: Automated testing (`pytest`), supply chain auditing (`pip-audit`), and SAST scanning (`Bandit`) prior to artifact creation on the Harness Delegate.
2. **Artifact Immutability**: Strict tagging via Git Commit SHA (`sourabh5050/harness-demo:<git-sha>`).
3. **Enterprise Release Governance**: Environment promotion across DEV/PROD with real live HTTPS deployment verifications and executive approval gates.

---

## High-Level Architecture Diagram

```
[ Developer Commit ]
        │
        ▼
[ GitHub Repository (Sourabh-50/harness-cloud-delivery-demo) ]
        │
        ▼
[ Harness Delegate / GitHub Action Execution Runner ]
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│ STAGE 1: Continuous Integration (CI Stage)              │
├─────────────────────────────────────────────────────────┤
│ ├── 1. pytest Unit Testing (GET /, /health, /version)   │
│ ├── 2. pip-audit Software Supply Chain Audit             │
│ ├── 3. Bandit Static Application Security Testing (SAST)│
│ ├── 4. Immutable Docker Build & Push (sourabh5050)      │
│ └── 5. Non-Root Container Execution Hardening Audit     │
└──────────────────────────┬──────────────────────────────┘
                           │ (Artifact Published & Output Passed)
                           ▼
┌─────────────────────────────────────────────────────────┐
│ STAGE 2: Continuous Delivery (CD Stage - DEV)           │
├─────────────────────────────────────────────────────────┤
│ ├── Step 1: Pick up Container Tag & Deploy to DEV       │
│ └── Step 2: DEV Live Health & Version Verification      │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│ STAGE 3: Approval Gate                                  │
├─────────────────────────────────────────────────────────┤
│ └── HarnessApproval Gate (Governance Sign-off)          │
└──────────────────────────┬──────────────────────────────┘
                           │ (Approved)
                           ▼
┌─────────────────────────────────────────────────────────┐
│ STAGE 4: Continuous Delivery (CD Stage - PROD)          │
├─────────────────────────────────────────────────────────┤
│ ├── Step 1: Real HTTPS /health Verification Probe       │
│ └── Step 2: Real HTTPS /version Verification Probe      │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
       [ Render Production Web Service (Live HTTPS) ]
            https://harness-demo-dev.onrender.com
```

---

## Component Topology

### 1. Application Layer (`app/app.py`)
* **Framework**: Python 3.11 / Flask / Gunicorn WSGI.
* **Endpoints**:
  * `GET /`: Platform status API.
  * `GET /health`: Operational health probe returning `{"status": "healthy"}` for deployment verification steps.
  * `GET /version`: Metadata endpoint exposing application version and Git SHA commit tracking.

### 2. Containerization (`Dockerfile`)
* **Base Image**: `python:3.11-slim` (Debian-based glibc, minimal attack surface).
* **Security Hardening**: Non-root system execution (`useradd -u 10001 -g appgroup -m -s /bin/false appuser`), granting dedicated ownership over `/app` and `/home/appuser` so Gunicorn worker control sockets start cleanly.
* **Process Manager**: Gunicorn WSGI server running 2 worker processes bound to `0.0.0.0:5000`.

### 3. Continuous Integration Stage (CI)
* **Unit Testing**: `pytest` running automated REST API assertions.
* **Software Supply Chain Audit**: `pip-audit` scanning `requirements.txt` against OSV/PyPI CVE databases.
* **Static Application Security Testing**: `Bandit` scanning Python AST for security misconfigurations.
* **Immutable Builder & Push**: Static Docker CLI client building and pushing tagged images (`sourabh5050/harness-demo:${COMMIT_SHA}`) to Docker Hub using Harness Secret Manager (`account.docker_hub_pat`).
* **Container Hardening Audit**: `grep "USER appuser"` verifying non-root isolation posture.

### 4. Continuous Delivery & Approval Stages (CD)
* **Stage 2 (CD Stage - DEV)**: Instantly picks up the pushed image tag upon CI completion, deploys to Development environment, and executes verification probes.
* **Stage 3 (Approval Gate)**: Halts pipeline execution until authorized sign-off is granted in Harness UI (`account._account_all_users`) or GitHub environment approval.
* **Stage 4 (CD Stage - PROD)**: Promotes hardened container to Render Web Service (`https://harness-demo-dev.onrender.com`), validates live HTTPS `/health` and `/version` endpoints, and enforces automated rollback safeguards on failure.
