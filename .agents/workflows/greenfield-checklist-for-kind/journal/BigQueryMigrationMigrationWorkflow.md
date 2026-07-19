# Greenfield Migration Journal: BigQueryMigrationMigrationWorkflow

This journal tracks the progress of the greenfield migration for the `BigQueryMigrationMigrationWorkflow` resource kind.

## Current Status
* **Current Step:** Step 2: Direct Controller, E2E fixtures and Fuzzer
* **Current Step Status:** In Progress (PR #11727 under commit 6c8f1a4, CI checks running and passing)

## Progress Tracking Table

| Step Number & Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|---|---|---|---|---|---|
| Step 1: Direct API Types and Identity | [#9023](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/9023) | [#9029](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/9029) | Merged | 2026-06-03 | 2026-06-03 |
| Step 2: Direct Controller, E2E fixtures and Fuzzer | [#11720](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/11720) | [#11727](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11727) | PR Created | 2026-07-18 | N/A |
| Step 3: mockGCP generation | N/A | N/A | Planned | N/A | N/A |
| Step 4: MockGCP Alignment with RealGCP | N/A | N/A | Planned | N/A | N/A |

## History / Status Update Notes
* **2026-07-19:** Monitored PR #11727. Verified that `lovelace-coder-bot` resolved the second round of CI failures (specifically, `TestGoldenLogAlignment` and `presubmit-gatekeeper` by registering `BigQueryMigrationMigrationWorkflow` in `mockGCPSkipGroupKinds`). Commit `6c8f1a44771939983f4289b66b903facddd8dbfc` was pushed. Latest CI checks are currently running (19 success, 174 pending, 0 failures).
* **2026-07-19:** Monitored PR #11727. Observed failing CI checks (`unit-tests` and `presubmit-gatekeeper`). Assigned the PR to its author `lovelace-coder-bot` via GitHub REST API to trigger a diagnostic run and address the unit-test failures.
* **2026-07-19:** Monitored progress of Step 2. Confirmed that `lovelace-coder-bot` submitted Pull Request #11727. The coder bot successfully resolved initial CI failures (including deepcopy generation, alpha missing fields list, mock HTTP logs, and a regression in mockworkflows tests). Latest CI check-runs are currently pending but all completed checks are passing.
* **2026-07-19:** Monitored progress of Step 2. Confirmed that coder bot `lovelace-coder-bot` is working on the issue in a sandbox, and no Pull Request has been submitted yet.
* **2026-07-18:** Started tracking parent issue #11696. Confirmed Step 1 was already completed via issue #9023 / PR #9029. Created Issue #11720 for Step 2.
