# Migration Journal: FilestoreInstance

## Current Step
Step 5a: Implement standardized label reconciliation (Addendum)

## Progress Tracking Table

| Step | Name | GitHub Issue | GitHub PR | Status | Date Started | Date Completed |
|------|------|--------------|-----------|--------|--------------|----------------|
| 1 | Implement direct KRM types and generate.sh | [#10732](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10732) | [#10734](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10734) | Completed | 2026-06-23 | 2026-06-24 |
| 2 | Move to identity and refs pattern | [#10769](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10769) | [#10776](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10776) | Completed | 2026-06-24 | 2026-06-25 |
| 3 | Implement round-trip KRM fuzzer | [#10841](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10841) | [#10843](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10843) | Completed | 2026-06-25 | 2026-06-25 |
| 4 | Match real gcp behavior in MockGCP | [#10849](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10849) | [#10914](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10914) | Completed | 2026-06-25 | 2026-07-09 |
| 5 | Implement direct controller and test fixtures | [#11564](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/11564) | [#11566](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11566) | Completed (Merged; also consolidated in PR #12788) | 2026-07-10 | 2026-09-10 |
| 5a | Implement standardized label reconciliation | [#12908](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12908) | [#12910](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12910) | PR Created (CI failing: presubmit-gatekeeper, unit-tests-3-of-4, fuzz-roundtrippers-5-of-8; overseer/stop attached) | 2026-09-11 | - |
| 6 | Validate Direct Promotion | [#12787](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12787) | [#12788](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12788) | PR Created (All 254 checks green, overseer/ready-for-human, overseer/stop attached) | 2026-09-06 | - |

## Status Updates
* **2026-10-19**: Monitored Step 5a and Step 6 progress.
  - Step 5a: PR [#12910](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12910) is linked to Issue [#12908](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12908). PR [#12910](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12910) has `overseer/stop` attached due to failing CI checks (`presubmit-gatekeeper`, `unit-tests-3-of-4`, `fuzz-roundtrippers-5-of-8`) reaching max automated retry attempts.
  - Step 6: PR [#12788](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12788) is linked to Issue [#12787](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12787). All 254/254 checks are 100% green; the PR has `overseer/ready-for-human` and `overseer/stop` (paused due to inactivity), awaiting human OWNER review and merge.
  - Following guardrails: respecting stop labels without modifications and waiting for open PRs to be merged before proceeding.
* **2026-09-11**: Identified that the direct controller is missing the new label reconciliation standard (see Issue #12869). Opened Issue [#12908](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12908) to address this. Step 6 (PR #12788) remains open and green, but we will wait for the label fix before proceeding or merging.
* **2026-09-11**: Monitored Step 6 progress. Checked Pull Request [#12788](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12788) status at 15:57 UTC. Re-verified via the GitHub REST API that all 250/250 CI check-runs remain successfully completed and are 100% green with zero failures on the latest commit (`df6c7b865c89d68082b22b82601ff8cc79378dec`). The PR remains healthy, open, and mergeable, currently awaiting manual review and final merge from a repository human OWNER.
* **2026-09-11**: Monitored Step 6 progress. Checked Pull Request [#12788](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12788) status at 12:32 UTC. Re-verified via the GitHub REST API that all 250/250 CI check-runs remain successfully completed and are 100% green with zero failures on the latest commit (`df6c7b865c89d68082b22b82601ff8cc79378dec`).
* **2026-07-02**: Monitored Step 4 progress. All 193/193 CI check-runs green on PR [#10914](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10914).
* **2026-06-30**: Monitored Step 4 progress. All 193/193 CI check-runs green on PR [#10914](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10914).
* **2026-06-28**: Monitored Step 4 progress. Checked PR [#10914](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10914).
* **2026-06-26**: Monitored Step 4 progress. Investigated CI failures on PR [#10914](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10914).
