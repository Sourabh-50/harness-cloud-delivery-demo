# Enterprise Cloud Delivery Platform — System Architecture Specification

## Executive Summary
This document specifies the technical architecture for the **Enterprise Cloud Delivery Platform**, built using **Harness Platform**, **GitHub**, and **Python Microservices**. 

The platform is designed around three core principles:
1. **Shift-Left Security & Quality**: Automated testing and vulnerability scanning prior to artifact creation.
2. **Artifact Immutability**: Strict tagging via Git Commit SHA (`harness-demo:<git-sha>`).
3. **Enterprise Release Governance**: Environment promotion across DEV/PROD with deployment verifications and approval gates.

---

## High-Level Architecture Diagram

```
[ Developer Commit ]
        │
        ▼
[ GitHub Repository ] ──► (Webhook Trigger)
                                │
                                ▼
               [ Shift-Left CI Stage (GitHub Cloud VM) ]
                 ├── 1. pytest Unit Testing (GET /, /health, /version)
                 ├── 2. pip-audit Dependency CVE Audit
                 ├── 3. Trivy Container Vulnerability & Secret Scan
                 └── 4. Immutable Docker Build (harness-demo:<git-sha>)
                                │
                                ▼
               [ Harness CD Release Control Plane ]
                 ├── Stage 1: DEV Deployment & Health Probe Verification
                 ├── Stage 2: Executive Security & Governance Approval Gate
                 └── Stage 3: PROD Promotion & Post-Deployment Verification
```

---

## Component Topology

### 1. Application Layer (`app/app.py`)
* **Framework**: Python 3.11 / Flask / Gunicorn WSGI.
* **Endpoints**:
  * `GET /`: Platform welcome & status API.
  * `GET /health`: Operational health probe returning `{"status": "healthy"}` for deployment verification steps.
  * `GET /version`: Metadata endpoint exposing application version and Git SHA commit tracking.

### 2. Containerization (`Dockerfile`)
* **Base Image**: `python:3.11-slim` (Debian-based glibc, minimal attack surface).
* **Security Hardening**: Non-root system execution (`appuser`, UID 10001).
* **Process Manager**: Gunicorn WSGI server running 2 worker processes on port 5000.

### 3. Shift-Left CI Engine (`.github/workflows/ci.yml`)
* **Unit Testing**: `pytest` running automated REST API assertions.
* **Software Supply Chain Audit**: `pip-audit` scanning `requirements.txt` against OSV/PyPI CVE databases.
* **Container & Repo Scanner**: `Trivy` scanning filesystem layers for hardcoded secrets and OS-level vulnerabilities.
* **Immutable Builder**: `docker build` generating image tag `harness-demo:${GITHUB_SHA::7}`.

### 4. Harness CD Control Plane (`harness-delegate-ci-pipeline`)
* **Stage 1 (DEV Verification)**: Executes HTTP `/health` probe verification.
* **Stage 2 (Executive Approval Gate)**: Halts pipeline execution until authorized SecOps / Leadership sign-off is granted in Harness UI.
* **Stage 3 (PROD Verification)**: Promotes artifact to Production, validates `/health` and `/version` endpoints, and enforces automated rollback safeguards.
