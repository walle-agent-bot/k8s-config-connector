# Greenfield Migration Journal: ComposerUserWorkloadsConfigMap

**Current Step:** Step 2: Controller, Fixtures & Fuzzer

## Migration Progress

| Step | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|---|---|---|---|---|---|
| Step 1a: Prepopulate | - | - | Completed (Bulk Prepopulated) | 2026-10-29 | 2026-10-29 |
| Step 1b: Judgement Triage | [#14617](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14617) | [#14625](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14625) | Merged | 2026-10-29 | 2026-10-30 |
| Step 2: Controller, Fixtures & Fuzzer | [#14710](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14710) | - | Open | 2026-10-30 | - |
| Step 3: MockGCP Implementation | - | - | Pending | - | - |
| Step 4: MockGCP Alignment | - | - | Pending | - | - |

## Updates Log

- [2026-10-29] Step 1a completed via bulk prepopulation on master (`ComposerUserWorkloadsConfigMap` in `apis/composer/judgement_queue.yaml`).
- [2026-10-29] Step 1b issue [#14617](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14617) created to triage judgement queue and finalize direct KRM types and identity.
- [2026-10-29] Pull request [#14625](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14625) created for Step 1b.
- [2026-10-30] Step 1b PR [#14625](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14625) merged.
- [2026-10-30] Step 2 issue [#14710](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14710) created to implement direct controller, E2E fixtures, and fuzzer.
