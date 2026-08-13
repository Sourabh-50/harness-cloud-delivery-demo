# Platform Architecture & Design Principles

## 1. Zero-Cost Infrastructure Model
To ensure predictable operational costs ($0 billable risk), this architecture eliminates cloud VM runtimes (EC2, ECS Fargate) in favor of **Harness Cloud CI Hosted Runners** and **Docker Hub Free Registry**.

## 2. Shift-Left Quality & Security Gates
* **Stage 1: Unit Test Gate**: `pytest` validates REST endpoints prior to build.
* **Stage 2: Software Supply Chain Gate**: `pip-audit` checks Python dependencies against known CVE databases.
* **Stage 3: Container Security Gate**: `Trivy` scans the compiled container layer for OS-level vulnerabilities and embedded secrets.

## 3. Artifact Immutability Standard
Image tags are strictly mapped to `$DRONE_COMMIT_SHA` (or Git commit hash). Re-using `:latest` in production introduces non-deterministic deployments and breaks automated rollbacks.
