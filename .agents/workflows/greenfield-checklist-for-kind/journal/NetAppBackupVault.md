# Greenfield Migration: NetAppBackupVault

Current Step: Step 3: mockGCP generation

## Progress Tracking

| Step | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
| --- | --- | --- | --- | --- | --- |
| Step 1a: Prepopulate Direct API Types, Identity, and Judgement Queue | N/A | [#4061](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/4061) | Completed (Legacy Step 1) | 2025-03-21 | 2025-03-21 |
| Step 1b: Triage Judgement Queue and Finalize Direct API Types, Identity, and Reference Types | N/A | N/A | Skipped (Legacy Step 1) | 2026-10-23 | 2026-10-23 |
| Step 2: Direct Controller, E2E fixtures and Fuzzer | [#14322](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14322) | [#14354](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14354) | Merged | 2026-10-23 | 2026-11-05 |
| Step 3: mockGCP generation | [#14957](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14957) | [#14959](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14959) | PR Created | 2026-11-05 | - |
| Step 4: MockGCP Alignment with RealGCP | - | - | Pending | - | - |

## Status Updates
* 2026-10-23: Initialized migration tracking for NetAppBackupVault. Verified types/identity/references/fuzzer were completed under legacy PR #4061. Step 1b skipped as legacy Step 1 is already complete without untriaged items.
* 2026-10-23: Created issue #14322 for Step 2 (Direct Controller, E2E fixtures, and fuzzer).
* 2026-10-23: PR #14354 created for Step 2. All CI checks passing and automated review completed. Waiting for PR to merge.
* 2026-11-05: PR #14354 for Step 2 merged successfully.
* 2026-11-05: Created issue #14957 for Step 3 (Implement MockGCP and Alignment).
* 2026-11-05: PR #14959 created for Step 3.
