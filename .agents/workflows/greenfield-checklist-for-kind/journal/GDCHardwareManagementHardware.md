# Migration Journal: GDCHardwareManagementHardware

## Current Step
**Step 1: Direct API Types and Identity and Reference Types Pattern**

## Migration Progress

| Step | Name | Issue | Pull Request | Status | Date Started | Date Completed |
| :--- | :--- | :---: | :----------: | :----: | :----------: | :------------: |
| 1 | Direct API Types and Identity | [#10269](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10269) | [#11270](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11270) | `Open` (Assigned `hopper-coder-bot`) | 2026-07-02 | |
| 2 | Direct Controller and E2E fixtures | | | | | |
| 3 | mockGCP generation | | | | | |
| 4 | MockGCP Alignment | | | | | |

## Status Updates
* **2026-07-03**: Monitored PR #11270 CI checks. Identified multiple failing checks (`tests-preview`, `unit-tests`, `unit-tests-operator`, `validations`). Re-assigned the PR to its author bot `hopper-coder-bot` to investigate and fix these failures.
* **2026-07-03**: Monitored CI checks on updated PR #11270. Detected a failure in `unit-tests-operator` (`TestGoldenConfigConnector/simple`) due to missing Operator RBAC configurations for the new `gdchardwaremanagement.cnrm.cloud.google.com` API group. Assigned the PR back to `hopper-coder-bot` to resolve the golden file diff.
* **2026-07-03**: Detected active Pull Request #11270 created by `hopper-coder-bot` for Step 1. CI checks showed a failure in `unit-tests-operator`. Assigned the PR back to the author bot `hopper-coder-bot` to investigate and resolve the failing CI checks.
* **2026-07-03**: Monitored Step 1 progress. No active Pull Request has been created yet. The assigned coder bots (ada-coder-bot, lovelace-coder-bot, hopper-coder-bot) are currently active on other tasks. Continuing to monitor.
* **2026-07-03**: Checked migration status. Since no active PR has been created yet and the previous PR #10330 was closed, assigned `lovelace-coder-bot` as an additional assignee to issue #10269 and posted a comment to help accelerate the Direct API types implementation.
* **2026-07-02**: Initialized migration tracking journal. Observed that the initial PR #10330 was closed without being merged. Issue #10269 is still open. Assigned `ada-coder-bot` to issue #10269 and commented to request a fresh PR.
