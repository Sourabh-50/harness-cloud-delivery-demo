# Enterprise Cloud Delivery Platform — Harness CI/CD

An enterprise-grade, production-verified DevSecOps continuous delivery platform built with **Harness Platform**, **Harness Delegate**, **Docker Hub Registry**, **Render Web Service**, and **Python Microservices**.

## Architecture Overview

```
[ Developer Push ] ──► [ GitHub Repo ] ──► [ Harness Delegate (In-Cluster) ]
                                                    │
    ┌───────────────────────────────────────────────┴───────────────────────────────┐
    │ STAGE 1: Shift-Left Quality Security and Build Stage (pytest, pip-audit,     │
    │          Bandit SAST, Docker Build & Push sourabh5050/harness-demo:<git-sha>, │
    │          Container Hardening Audit)                                           │
    └───────────────────────────────────────────────┬───────────────────────────────┘
                                                    │
                                                    ▼
    ┌───────────────────────────────────────────────────────────────────────────────┐
    │ STAGE 2: Executive Approval Gate (HarnessApproval Gate)                       │
    └───────────────────────────────────────────────┬───────────────────────────────┘
                                                    │
                                                    ▼
    ┌───────────────────────────────────────────────────────────────────────────────┐
    │ STAGE 3: Continuous Delivery and Live Verification Stage                      │
    │          (Real HTTPS /health & /version Probes against Render Production)     │
    └───────────────────────────────────────────────────────────────────────────────┘
```

## Core Features
* **Multi-Stage DevSecOps Pipeline**: 3-stage pipeline combining CI quality checks, manual approval governance, and continuous delivery live verification.
* **Shift-Left Security & SAST**: `pytest` unit testing, `pip-audit` software supply chain CVE scanning, and `Bandit` static application security analysis.
* **Immutable Artifact Registry**: Docker container tagged strictly with Git SHA (`sourabh5050/harness-demo:<git-sha>`) and pushed to Docker Hub via Harness Secret Manager (`account.docker_hub_pat`).
* **Non-Root Execution Hardening**: Non-root system user (`appuser` UID 10001) with dedicated `/home/appuser` home directory permission isolation for Gunicorn worker control sockets.
* **Live CD Deployment & Verification**: Hardened container running live on Render (`https://harness-demo-dev.onrender.com`), verified by real-time automated HTTPS cURL probes in Harness Stage 3.
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
