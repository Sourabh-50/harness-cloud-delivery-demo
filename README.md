# Enterprise Cloud Delivery Platform — Harness CI/CD

An enterprise-grade, zero-cost continuous delivery pipeline built with **Harness Cloud CI** and **GitHub**.

## Architecture Overview

```
Developer Push ──► GitHub ──► Harness Cloud CI ──► Security Gates ──► Docker Hub ──► Harness CD Promotion
```

## Features
* **100% Cloud-Executed Pipeline**: Runs natively on Harness Cloud hosted runners. Zero local footprint required.
* **Shift-Left Security**: Dependency scanning (`pip-audit`) and container image analysis (`Trivy`) before artifact promotion.
* **Immutable Container Builds**: Tagged strictly via Git Commit SHA (`harness-demo:<commit-sha>`).
* **Deployment Verification**: Health check endpoints (`/health`) designed for deployment verification.
* **Zero Cost**: Built entirely using free tiers and open-source tooling ($0 / ₹0).

## API Endpoints
* `GET /`: Platform status message
* `GET /health`: Health probe endpoint
* `GET /version`: Metadata and release version
