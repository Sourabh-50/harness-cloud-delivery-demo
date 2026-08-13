# Troubleshooting Guide & FDE Customer Scenario Playbook

## Common Operational Issues & Remediation

| Symptom | Root Cause | Resolution |
| :--- | :--- | :--- |
| **`Permission denied: '/home/appuser'`** | Gunicorn v26 worker control socket requires non-root home directory ownership. | Update `Dockerfile` to `useradd -m` and `chown -R appuser:appgroup /app /home/appuser`. |
| **`unauthorized: incorrect username or password`** | Docker Hub login used incorrect username handle or unescaped secret reference. | Use exact Docker Hub username (`sourabh5050`) and reference secret via `<+secrets.getValue("account.docker_hub_pat")>`. |
| **`pip3: command not found` on Delegate** | Delegate execution container missing Python package manager. | Add package installation check: `if ! command -v python3; then microdnf install -y python3 python3-pip git; fi`. |
| **`ModuleNotFoundError: No module named 'app'`** | Python PATH missing repository root during `pytest`. | Run tests using `export PYTHONPATH=. && python -m pytest -v`. |

---

## Forward Deployed Engineer (FDE) Customer Incident Playbook

### Scenario
> *"An enterprise customer reports that their production deployment pipeline is stuck at the Executive Approval Gate stage during a critical release window."*

### Troubleshooting Playbook

1. **Acknowledge & Validate Impact**:
   * Inform the customer immediately: *"I am investigating the pipeline execution state for build #X right now."*

2. **Inspect Pipeline State**:
   * Open Harness UI -> **Pipelines** -> **Execution History**.
   * Locate the blocked execution step (**Executive Approval Gate**).
   * Verify if the approval notification reached the designated user group (`account._account_all_users`).

3. **Diagnose Permission / Policy Block**:
   * Check if `disallowPipelineExecutor: true` is active. If the user attempting to approve is the same user who initiated the execution, Harness intentionally blocks the action to preserve compliance.
   * Have an authorized secondary approver execute the sign-off inside Harness UI.

4. **Post-Incident Action Item**:
   * Configure Slack/Teams webhook notifications for Approval step entry to eliminate approval latency in future releases.
