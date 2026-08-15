# 🛠️ CI/CD & Kubernetes Troubleshooting Guide

This guide documents common errors encountered during Harness CI/CD execution and their resolution.

---

## 1. Issue: `0/1 nodes are available: 1 Insufficient cpu`

### Symptom:
Stage initialization fails with Kubernetes pod scheduling error:
```text
0/1 nodes are available: 1 Insufficient cpu. no new claims to deallocate
```

### Cause:
The Kubernetes cluster (Minikube with 2 CPUs) cannot accommodate default container resource requests across 6 step containers + `lite-engine` ($400\text{m} \times 6 + 500\text{m} = 2.9\text{ CPUs} > 2.0\text{ CPUs}$).

### Solution:
Explicitly define lightweight CPU resource limits on every step in `harness-pipeline.yaml`:
```yaml
resources:
  limits:
    cpu: "100m"
    memory: "256Mi"
```

---

## 2. Issue: `Connector not found for identifier : [k8s_delegate] with scope: [ACCOUNT]`

### Symptom:
Pipeline initialization fails with scope resolution error:
```text
Connector not found for identifier : [k8s_delegate] with scope: [ACCOUNT]
```

### Cause:
Prefixing a connector ID with `account.` instructs Harness to resolve the connector at Account level. Connectors created under **Project Settings ➔ Connectors** must be referenced without `account.`.

### Solution:
Update `connectorRef` to `k8s_delegate` (Project scope).

---

## 3. Issue: `Following delegate(s) failed to complete validation check : [[]]`

### Symptom:
Harness CI fails during initialization before any step runs.

### Cause:
1. Referenced connector did not exist in Harness Connectors.
2. Delegate lacked required CI runner capability checks.

### Solution:
Deploy standard single-container Harness Kubernetes Delegate (`harness-k8s-delegate.yaml`) into `harness-delegate-ng` namespace and link via `k8s_delegate` connector.

---

## 4. Cleaning Up Ephemeral Step Pods

To clear completed or stuck runner pods from Minikube:

```bash
kubectl delete pods -n harness-delegate-ng --field-selector=status.phase!=Running
```
