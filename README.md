# Enterprise Cloud Delivery Platform — Harness CI/CD

An enterprise-grade, production-verified DevSecOps continuous delivery platform built with **Harness Platform**, **Harness Delegate**, **Docker Hub Registry**, **Render Web Service**, and **Python Microservices**.

## Architecture Overview

```
[ Developer Push ] ──► [ GitHub Repo ] ──► [ Harness Delegate / GitHub Runner ]
                                                    │
    ┌───────────────────────────────────────────────┴───────────────────────────────┐
    │ STAGE 1: Continuous Integration (CI Stage)                                    │
    │          (pytest, pip-audit, Bandit SAST, Trivy Scan, Build & Push            │
    │          sourabh5050/harness-demo:<git-sha>, Non-Root Audit)                 │
    └───────────────────────────────┬───────────────────────────────────────────────┘
                                    │ (Artifact Published & Triggered)
                                    ▼
    ┌───────────────────────────────────────────────────────────────────────────────┐
    │ STAGE 2: Continuous Delivery (CD Stage - DEV Environment)                     │
    │          (Automated Deployment to DEV, Live Health & Version Verification)   │
    └───────────────────────────────┬───────────────────────────────────────────────┘
                                    │
                                    ▼
    ┌───────────────────────────────────────────────────────────────────────────────┐
    │ STAGE 3: Approval Gate                                                        │
    │          (Governance Review in Harness UI / GitHub Environment)               │
    └───────────────────────────────┬───────────────────────────────────────────────┘
                                    │ (Approved)
                                    ▼
    ┌───────────────────────────────────────────────────────────────────────────────┐
    │ STAGE 4: Continuous Delivery (CD Stage - PROD Environment)                    │
    │          (Real HTTPS /health & /version Probes against Render Production)     │
    └───────────────────────────────────────────────────────────────────────────────┘
```

## Core Features
* **Decoupled Multi-Stage CI/CD Pipeline**: Explicit architectural separation between Continuous Integration (CI) and Continuous Delivery (CD) across DEV and PROD environments.
* **Shift-Left Security & SAST**: `pytest` unit testing, `pip-audit` software supply chain CVE scanning, and `Bandit` static application security analysis.
* **Immutable Artifact Registry**: Docker container tagged strictly with Git SHA (`sourabh5050/harness-demo:<git-sha>`) and pushed to Docker Hub via Harness Secret Manager (`account.docker_hub_pat`).
* **Non-Root Execution Hardening**: Non-root system user (`appuser` UID 10001) with dedicated `/home/appuser` home directory permission isolation for Gunicorn worker control sockets.
* **Automated Dev Delivery & Production Verification**: Immediate DEV deployment upon CI build completion, followed by an Approval Gate before PROD release (`https://harness-demo-dev.onrender.com`).
* **Zero Cost Safeguard**: Designed and executed with zero billable cloud cost ($0 / ₹0).

## Production Microservice API Endpoints
* `GET /`: Platform status API (`https://harness-demo-dev.onrender.com/`)
* `GET /health`: Operational health check endpoint (`https://harness-demo-dev.onrender.com/health`)
* `GET /version`: Commit SHA and version metadata endpoint (`https://harness-demo-dev.onrender.com/version`)

## Documentation Index
* [Architecture Specification](docs/architecture.md)
* [CI/CD Workflow Guide](docs/ci-cd.md)
* [Security & Compliance](docs/security.md)
* [Troubleshooting & FDE Playbook](docs/troubleshooting.md)
