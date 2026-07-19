# Greenfield Migration Journal: VertexAICustomJob

Current Step: Step 1 - Direct API Types and Identity and Reference Types Pattern

## Progress Tracking

| Step | Step Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Direct API Types and Identity | [#11716](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/11716) | [#11724](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11724) | PR Created | 2026-07-18 | - |
| 2 | Direct Controller, E2E fixtures and Fuzzer | - | - | Pending | - | - |
| 3 | mockGCP generation | - | - | Pending | - | - |
| 4 | MockGCP Alignment with RealGCP | - | - | Pending | - | - |

## Status Update Notes

### 2026-07-19
* Pull Request [#11724](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11724) was created for Step 1.
* Detected unit-tests check failure on the PR.
* Assigned the PR to `ada-coder-bot` to investigate and resolve the unit-test failures.
* Re-assigned/pinged the PR to `ada-coder-bot` via REST API to re-trigger investigation of the ongoing unit-test failure related to missing reference exceptions (missingrefs.txt).

### 2026-07-18
* Initiated migration orchestration for VertexAICustomJob.
* Created GitHub issue #11716 for Step 1.
* AI Factory started working on Step 1 (issue #11716) in a sandbox.
