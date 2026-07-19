# Greenfield Migration Journal: VertexAICustomJob

Current Step: Step 1 - Direct API Types and Identity and Reference Types Pattern

## Progress Tracking

| Step | Step Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Direct API Types and Identity | [#11715](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/11715) | [#11733](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11733) | PR Created | 2026-07-18 | - |
| 2 | Direct Controller, E2E fixtures and Fuzzer | - | - | Pending | - | - |
| 3 | mockGCP generation | - | - | Pending | - | - |
| 4 | MockGCP Alignment with RealGCP | - | - | Pending | - | - |

## Status Update Notes

### 2026-07-19
* Identified that `ada-coder-bot` created a new Pull Request [#11733](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11733) to address the unit-test failures in [#11724](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11724) by correctly regenerating manifests and updating Golden exception files (`acronyms.txt`, `missingrefs.txt`, etc.).
* Assigned `ada-coder-bot` and added appropriate step labels (`overseer`, `step/gen-types`, `greenfield`) to PR [#11733](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11733) using the REST API to ensure proper orchestration tracking.
* Updated our local journal and parent issue tracking to focus on PR [#11733](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11733) as it undergoes a fresh CI run.
* Re-assigned/pinged the PR [#11724](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11724) to `ada-coder-bot` via REST API to re-trigger investigation of the ongoing unit-test failure related to missing reference exceptions (missingrefs.txt).

### 2026-07-18
* Initiated migration orchestration for VertexAICustomJob.
* Created GitHub issue #11716 for Step 1.
* AI Factory started working on Step 1 (issue #11716) in a sandbox.
