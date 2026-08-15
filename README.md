# 🚀 Enterprise Decoupled CI/CD Platform (Harness & Kubernetes)

[![Pipeline Status](https://img.shields.io/badge/Harness_CI%2FCD-Decoupled_Pipeline-blue.svg)](https://app.harness.io)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Delegate_v1.35-326CE5.svg)](https://kubernetes.io/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise-grade, multi-stage **CI/CD Platform** built using **Harness NextGen**, **Kubernetes (Minikube)**, and **Python (Flask)**. 

The pipeline strictly decouples **Continuous Integration (CI)** from **Continuous Delivery (CD)** across 4 governance-controlled stages with automated security audits, human approval gates, and live health verification probes.

---

## 🏗️ Decoupled Pipeline Architecture

```
[ Stage 1: CI ] ──► [ Stage 2: CD DEV ] ──► [ Stage 3: Approval Gate ] ──► [ Stage 4: CD PROD ]
  ├── Pytest          ├── Trigger DEV         ├── RBAC Sign-off         ├── Live /health Probe
  ├── Pip-Audit       └── Health Probe        └── User Group Audit       └── Live /version Probe
  ├── Bandit SAST
  ├── Image Build
  └── Hardening Audit
```

### Stage 1: Continuous Integration (CI Stage)
- **Automated Unit Tests**: Runs `pytest` suite across microservice endpoints.
- **Dependency Security Audit**: Scans dependencies with `pip-audit`.
- **SAST Security Scan**: Performs static application security testing using `bandit`.
- **Container Image Packaging**: Builds & verifies immutable Docker images (`sourabh5050/harness-demo:<sha>`).
- **Isolation Compliance**: Audits `Dockerfile` non-root `appuser` security boundary.

### Stage 2: Continuous Delivery (CD - DEV Stage)
- **Deployment Trigger**: Promotes built container artifact to the DEV environment.
- **Staging Probes**: Executes live health and version verification probes.

### Stage 3: Governance Approval Gate
- **Human-in-the-Loop Sign-off**: Halts pipeline promotion until an authorized user/user group grants explicit approval in Harness UI.

### Stage 4: Continuous Delivery (CD - PROD Stage)
- **Production Promotion**: Deploys verified release to Production.
- **Resilient HTTPS Probes**: Verifies live `/health` and `/version` endpoints with cold-start fallback handling.

---

## ⚙️ Kubernetes Delegate & Infrastructure

The pipeline runs on a **Harness Kubernetes Delegate** deployed in the `harness-delegate-ng` namespace:

```bash
# 1. Start Kubernetes cluster
minikube start --cpus=2 --memory=3072

# 2. Deploy Harness Kubernetes Delegate
kubectl apply -f harness-k8s-delegate.yaml

# 3. Verify Delegate Status
kubectl get pods -n harness-delegate-ng
```

---

## 🛠️ Repository Structure

```text
├── app/                        # Python Flask Microservice
│   ├── app.py                  # Core Application Code (/health, /version)
│   └── __init__.py
├── tests/                      # Automated Test Suite
│   └── test_app.py             # Pytest Unit Tests
├── docs/                       # Project Documentation
│   ├── architecture.md         # Architecture & Design Specifications
│   ├── ci-cd.md                # Harness & CI/CD Pipeline Setup
│   ├── security.md             # DevSecOps & Hardening Audits
│   └── troubleshooting.md      # Kubernetes & Delegate Troubleshooting
├── harness-pipeline.yaml       # Harness NextGen 4-Stage Decoupled Pipeline
├── harness-k8s-delegate.yaml   # Kubernetes Delegate Deployment Manifest
├── Dockerfile                  # Non-root Production Container Specification
└── requirements.txt            # Microservice Dependencies
```

---

## 🧪 Local Testing & Verification

```bash
# Install dependencies
pip install -r requirements.txt

# Run pytest unit tests
export PYTHONPATH=.
python -m pytest -v

# Run Bandit security scan
bandit -r app/ -s B104
```

---

## 🔐 Security & Governance

- **Non-Root Execution**: Container runs under dedicated non-root `appuser` (UID `10001`).
- **Zero-Trust Firewalling**: Harness Delegate connects outbound-only via TLS 1.3 to `app.harness.io`.
- **Resource Constraints**: Pod step limits capped at `cpu: 100m`, `memory: 256Mi` for cluster optimization.
