# Enterprise Security & Compliance Specification

## Security Posture Overview
Security is integrated at every layer of the delivery lifecycle using open-source tooling (`pip-audit`, `Bandit`, non-root container isolation) and Harness enterprise governance policies.

---

## 1. Container Hardening (`Dockerfile`)

* **Minimal Base Image**: Built on `python:3.11-slim` (Debian-based glibc), eliminating unnecessary compilers (`gcc`, `make`) to reduce attack surface.
* **Non-Root Execution & Home Directory Permission Isolation**:
  ```dockerfile
  RUN groupadd -g 10001 appgroup && \
      useradd -u 10001 -g appgroup -m -s /bin/false appuser && \
      chown -R appuser:appgroup /app /home/appuser
  USER appuser
  ```
  Running as `appuser` (UID 10001) with dedicated home directory ownership (`/home/appuser`) allows Gunicorn worker control servers to run cleanly without root privileges, preventing host takeover in the event of a container breakout vulnerability.
* **Zero Secrets in Image**: Code ignores `.env` files and caches via `.dockerignore`.

---

## 2. Shift-Left Security Scans

### A. Software Supply Chain Auditing (`pip-audit`)
* Audits Python packages in `requirements.txt` against PyPI and OSV vulnerability databases.
* Prevents vulnerable third-party dependencies from reaching build containers.

### B. Static Application Security Testing (`Bandit SAST`)
* Scans Python AST for security vulnerabilities, hardcoded IP bindings, insecure socket usage, and weak cryptography (`bandit -r app/ -s B104`).

---

## 3. Harness Governance & Segregation of Duties (SoD)

* **Approval Gate**: Requires explicit human sign-off (`account._account_all_users`) prior to PROD promotion.
* **Secret Management**: Passwords and Personal Access Tokens are injected securely via Harness Secret Manager (`account.docker_hub_pat`) and masked in build execution logs.
* **Auditability**: Every pipeline execution, approval log, and verification status is immutably logged in Harness Platform execution history.
