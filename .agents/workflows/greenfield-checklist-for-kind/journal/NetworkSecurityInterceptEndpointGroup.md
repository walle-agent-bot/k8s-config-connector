# Migration Journal: NetworkSecurityInterceptEndpointGroup

## Current Step
Step 2: Direct Controller, E2E fixtures and Fuzzer

## Progress Tracking

| Step | Step Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|---|---|---|---|---|---|---|
| 1 | Direct API Types, Identity & Reference Types | [#8728](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/8728) | [#8757](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/8757) | Completed | 2026-05-27 | 2026-05-27 |
| 2 | Direct Controller, E2E fixtures & Fuzzer | [#11425](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/11425) | [#11437](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11437) | PR Created | 2026-07-07 | - |
| 3 | MockGCP Generation | - | - | Pending | - | - |
| 4 | MockGCP Alignment with RealGCP | - | - | Pending | - | - |

## Status Update Notes
* **2026-07-07**: Monitored progress of Step 2. Pull Request [#11437](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11437) remains open with checks continuing to progress. The key check-run `smoketest-with-kind` has now successfully completed and passed, in addition to previously passed checks. No failures have been reported, and we are waiting for the remaining pending checks (`unit-tests`, `fuzz-roundtrippers`, and `validations`) to complete.
* **2026-07-07**: Checked migration progress of Step 2. Pull Request [#11437](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11437) has been successfully re-assigned to trigger a fresh check run. The new checks are currently in progress, and initial results show key check jobs (including `tests-gcptracker`, `tests-preview`, `test-pause`, `capture-pprof`, `license-lint`, `validate-untested-fields`, `run-linters`, and `unit-tests-operator`) have completed successfully. No failures have been reported.
* **2026-07-07**: Monitored progress of Step 2. Pull Request [#11437](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11437) is open with checks in progress. Key presubmits (e.g., `tests-preview`, `tests-gcptracker`, `test-pause`, `capture-pprof`, `license-lint`, `validate-untested-fields`, `run-linters`) have passed successfully. No failures have been detected.
* **2026-07-07**: Monitored progress of Step 2. Pull Request [#11437](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11437) has merge conflicts (`CONFLICTING`/`DIRTY`). Noted that `argus-watcher-bot` has started resolving the conflicts and rebasing the PR in a sandbox. We will wait for the rebase to complete.
* **2026-07-07**: Checked migration progress. Detected open Pull Request [#11437](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11437) with a failed `unit-tests` check caused by a transient runner interruption in `setup-gcloud`. Re-assigned the author bot `lovelace-coder-bot` via the GitHub CLI to trigger a fresh check run.
* **2026-07-07**: Monitored Step 2. Pull Request [#11437](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11437) was still blocked by a failing `unit-tests` check-run due to a transient cancellation during `setup-gcloud`. Reset the PR assignment for author bot `lovelace-coder-bot` using the GitHub REST API to trigger a fresh retry of the checks.
* **2026-07-07**: Checked migration progress. Detected open Pull Request [#11437](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11437) with a failed `unit-tests` check caused by a transient runner interruption in `setup-gcloud`. Reset the PR assignment to author bot `lovelace-coder-bot` via the GitHub REST API to trigger a fresh retry.
* **2026-07-07**: Monitored progress of Step 2. Pull Request [#11437](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11437) remains open due to `unit-tests` failing on transient runner cancellation. Reset the PR assignment for author bot `lovelace-coder-bot` using the REST API to trigger a fresh check run.
* **2026-07-07**: Re-verified the migration status. Found that PR [#11437](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11437) is still blocked by the transient `unit-tests` setup-gcloud action cancellation. Re-assigned the author bot `lovelace-coder-bot` via the GitHub REST API to trigger a fresh check run.
* **2026-07-07**: Verified that PR [#11437](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11437) was blocked by a transient infrastructure failure in `unit-tests` (setup-gcloud action cancellation). Re-assigned the author bot `lovelace-coder-bot` using the GitHub REST API to trigger a fresh check run.
* **2026-07-07**: Monitored progress of Step 2. Pull Request [#11437](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11437) remains open with a failing `unit-tests` check-run. Investigated the logs and found the failure was due to a GitHub Actions runner cancellation ("The runner has received a shutdown signal"). Re-assigned the author bot `lovelace-coder-bot` to trigger a fresh check run.
* **2026-07-07**: Checked migration progress. Detected open Pull Request [#11437](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11437) for Step 2. Noted failing `unit-tests` check-run. Assigned the PR author bot `lovelace-coder-bot` to the PR to address the failure.
* **2026-07-07**: Detected open Pull Request [#11437](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11437) for Step 2. Noted failing `validate-generated-files` check-run. Assigned the PR author bot `lovelace-coder-bot` to the PR to address the failure and regenerate files.
* **2026-07-07**: Re-verified the status of the migration. Step 2 issue #11425 is still open and actively being processed by coder bots in the sandbox. No pull request has been opened yet.
* **2026-07-07**: Monitored the migration progress. Confirmed that Step 2 issue #11425 is open and currently in progress by coder bots in the sandbox. No Pull Request has been opened yet.
* **2026-07-07**: Detected closed previous stale issue #8817 and closed stale PR #8835. A new clean step 2 issue #11425 was opened. Assigned issue #11425 to coder bot `ada-coder-bot` to trigger a clean, fresh attempt.
* **2026-05-27**: Step 1 types and identity implemented and merged in PR #8757.
