# Troubleshooting Guide & FDE Customer Scenario Playbook

## Common Operational Issues & Remediation

| Symptom | Root Cause | Resolution |
| :--- | :--- | :--- |
| **`Failed to connect to /127.0.0.1:3000`** | Docker Delegate missing socket mount or host networking. | Run delegate with `-v /var/run/docker.sock:/var/run/docker.sock --net=host -e RUNNER_URL="http://127.0.0.1:3000" -e CI_MOUNT_DOCKER_SOCKET="true"`. |
| **`Delegate(s) don't have selectors [linux-amd64]`** | Pipeline stage specifies platform tag missing on Delegate. | Add tag `linux-amd64` to Delegate under Project Settings -> Delegates -> Tags. |
| **`NullPointerException: Platform.getOs()`** | Missing `platform: os: Linux, arch: Amd64` block in YAML. | Include explicit `platform:` spec in stage definition. |
| **`ModuleNotFoundError: No module named 'app'`** | Python PATH missing repository root during `pytest`. | Run tests using `export PYTHONPATH=. && python -m pytest -v`. |

---

## Forward Deployed Engineer (FDE) Customer Incident Playbook

### Scenario
> *"A customer enterprise customer reports that their production deployment pipeline is stuck at the Executive Approval Gate stage for over 4 hours during a critical release window. The customer's VP of Engineering is demanding immediate resolution."*

### Troubleshooting Playbook

1. **Acknowledge & Validate Impact**:
   * Inform the customer immediately: *"I am investigating the pipeline execution state for build #X right now."*

2. **Inspect Pipeline State**:
   * Open Harness UI -> **Pipelines** -> **Execution History**.
   * Locate the blocked execution step (**Executive Approval Gate**).
   * Verify if the approval notification reached the designated user group (`_project_all_users` or SecOps).

3. **Diagnose Permission / Policy Block**:
   * Check if `disallowPipelineExecutor: true` is active. If the user attempting to approve is the same user who initiated the execution, Harness intentionally blocks the action to preserve compliance.
   * Have an authorized secondary approver execute the signoff inside Harness UI.

4. **Post-Incident Action Item**:
   * Configure Slack/Teams webhook notifications for Approval step entry to eliminate approval latency in future releases.
