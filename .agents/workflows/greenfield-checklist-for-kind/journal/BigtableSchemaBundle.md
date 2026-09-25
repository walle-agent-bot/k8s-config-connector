# Greenfield Migration Journal: BigtableSchemaBundle

**Current Step:** Step 3: mockGCP generation

## Migration Progress

| Step | Step Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|---|---|---|---|---|---|---|
| 1 | Direct API Types and Identity | [#13357](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/13357) | [#13359](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13359) | Merged | 2026-09-22 | 2026-09-23 |
| 2 | Direct Controller, E2E fixtures & Fuzzer | [#13419](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/13419) | [#13422](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13422) | Merged | 2026-09-24 | 2026-09-25 |
| 3 | mockGCP generation | [#13456](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/13456) | - | Open | 2026-09-25 | - |
| 4 | MockGCP Alignment with RealGCP | - | - | Pending | - | - |

## Status Update Notes
- **2026-09-25:** Step 2 completed (direct controller, E2E fixtures, and fuzzer merged in PR [#13422](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13422)). Initiated Step 3: created GitHub Issue [#13456](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/13456) for MockGCP and alignment.
- **2026-09-24:** Step 1 completed (types merged in PR [#13359](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13359)). Initiated Step 2: created GitHub Issue [#13419](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/13419) to implement the direct controller, E2E fixtures, and fuzzer.
- **2026-09-22:** Initiated Greenfield migration for BigtableSchemaBundle. Created Step 1 GitHub Issue [#13357](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/13357) to implement direct KRM types, identity, and generate.sh.
