# Enterprise Security & Compliance Specification

## Security Posture Overview
Security is integrated at every layer of the delivery lifecycle using open-source tooling and enterprise governance policies.

---

## 1. Container Hardening (`Dockerfile`)

* **Minimal Base Image**: Built on `python:3.11-slim` (Debian-based glibc), eliminating unnecessary compilers (`gcc`, `make`) to reduce attack surface.
* **Non-Root Execution**:
  ```dockerfile
  RUN groupadd -g 10001 appgroup && \
      useradd -u 10001 -g appgroup -s /bin/false appuser && \
      chown -R appuser:appgroup /app
  USER appuser
  ```
  Running as `appuser` (UID 10001) prevents host takeover in the event of a container breakout vulnerability.
* **Zero Secrets in Image**: Code ignores `.env` files via `.dockerignore`.

---

## 2. Shift-Left Security Scans

### A. Software Supply Chain Auditing (`pip-audit`)
* Audits Python packages in `requirements.txt` against PyPI and OSV vulnerability databases.
* Prevents vulnerable third-party dependencies from reaching build containers.

### B. Repository & Container Scanning (`Trivy`)
* Scans repository filesystem for exposed secrets, passwords, private keys, and high/critical OS CVEs.
* Outputs readable tabular reports directly into build logs.

---

## 3. Harness Governance & Segregation of Duties (SoD)

* **Approval Gate**: Requires explicit human signoff prior to PROD promotion.
* **Segregation of Duties**: Enforces policy preventing the engineer who triggered the build from approving their own release (`disallowPipelineExecutor: true`).
* **Auditability**: Every pipeline execution, approval log, and verification status is immutably logged in Harness Platform execution history.
