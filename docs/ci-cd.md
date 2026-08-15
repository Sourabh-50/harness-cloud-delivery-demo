# 🔄 Decoupled CI/CD Pipeline Specification (Harness NextGen)

This document details the configuration, governance model, and delegate setup for the **Decoupled CI/CD Platform**.

---

## 📌 4-Stage Pipeline Architecture

```yaml
stages:
  - Stage 1: Continuous Integration (CI)       # Build, test, security audit
  - Stage 2: Continuous Delivery (CD - DEV)    # Deploy to staging & verify
  - Stage 3: Governance Approval Gate          # RBAC human sign-off
  - Stage 4: Continuous Delivery (CD - PROD)   # Production release & HTTPS probes
```

### Stage 1: Continuous Integration (CI)
* **Type**: `CI` (`cloneCodebase: true`)
* **Infrastructure**: `KubernetesDirect` (`namespace: harness-delegate-ng`, `connectorRef: k8s_delegate`)
* **Steps**:
  1. `run_unit_tests`: Executes `pytest` unit test suite in `python:3.11-slim` container.
  2. `dependency_audit`: Audits Python packages using `pip-audit`.
  3. `bandit_sast_scan`: Scans code for static vulnerabilities with `bandit`.
  4. `build_and_push_image`: Builds and packages immutable Docker container image.
  5. `container_hardening_audit`: Audits non-root `USER appuser` isolation in Dockerfile.

### Stage 2: Continuous Delivery (CD - DEV)
* **Type**: `CI` (`cloneCodebase: false`)
* **Steps**:
  1. `dev_deployment_trigger`: Promotes commit SHA artifact to DEV environment.
  2. `dev_live_verification`: Executes live staging health verification probe.

### Stage 3: Approval Gate
* **Type**: `Approval` (`HarnessApproval`)
* **Approvers**: `account._account_all_users` (minimum count: 1)
* **Behavior**: Halts execution until authorized user approves promotion to Production.

### Stage 4: Continuous Delivery (CD - PROD)
* **Type**: `CI` (`cloneCodebase: false`)
* **Steps**:
  1. `prod_health_probe`: Executes `curl -s -k --max-time 15 https://harness-demo-dev.onrender.com/health`.
  2. `prod_version_probe`: Executes `curl -s -k --max-time 15 https://harness-demo-dev.onrender.com/version`.

---

## 🔌 Connector Configuration

| Connector Name | Identifier | Scope | Type | Details |
|---|---|---|---|---|
| **GitHub Connector** | `account.CICD_Connector` | Account | Git Repository | Connects to `Sourabh-50/harness-cloud-delivery-demo` |
| **Kubernetes Cluster Connector** | `k8s_delegate` | Project | Kubernetes Cluster | Inherits credentials from active `k8s-delegate` |

---

## 💻 Kubernetes Delegate Deployment

Deploy the single-container Harness Delegate to your cluster:

```bash
kubectl apply -f harness-k8s-delegate.yaml
```

Verify pod health:

```bash
kubectl get pods -n harness-delegate-ng
```

Expected Output:
```text
NAME                           READY   STATUS    RESTARTS   AGE
k8s-delegate-b78489f9b-rjzbw   1/1     Running   0          5m
```
