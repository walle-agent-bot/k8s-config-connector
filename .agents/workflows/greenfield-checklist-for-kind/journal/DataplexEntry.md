# Greenfield Migration Journal: DataplexEntry

Current Step: Step 2 - Direct Controller, E2E fixtures and Fuzzer

## Migration Progress

| Step | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|---|---|---|---|---|---|
| Step 1a: Prepopulate Direct API Types, Identity, and Judgement Queue | N/A | N/A | Completed (Bulk Prepopulated) | 2026-10-29 | 2026-10-29 |
| Step 1b: Triage Judgement Queue and Finalize Direct API Types, Identity, and Reference Types | [#14667](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14667) | [#14685](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14685) | Completed | 2026-10-29 | 2026-10-30 |
| Step 2: Direct Controller, E2E fixtures and Fuzzer | [#14700](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14700) | [#14714](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14714) | PR Created | 2026-10-30 | - |
| Step 3: mockGCP generation | - | - | Pending | - | - |
| Step 4: MockGCP Alignment with RealGCP | - | - | Pending | - | - |

## Status Updates
- 2026-10-29: Verified `DataplexEntry` was bulk-prepopulated in `apis/dataplex/judgement_queue.yaml` on `master`. Marked Step 1a as Completed (Bulk Prepopulated).
- 2026-10-29: Created Step 1b issue #14667 to triage the judgement queue and finalize direct KRM types and identity for DataplexEntry.
- 2026-10-30: PR #14685 created for Step 1b.
- 2026-10-30: PR #14685 merged into master. Step 1b completed.
- 2026-10-30: Created Step 2 child issue #14700 to implement direct controller, E2E fixtures, and fuzzer for DataplexEntry.
- 2026-10-30: PR #14714 created for Step 2.
