# Migration Progress: AccessContextManagerGCPUserAccessBinding

**Current Step:** Step 3: Create a Round-Trip KRM Fuzzer

## Progress Tracking

| Step Number and Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|---|---|---|---|---|---|
| Step 1: Direct API Types | [#14345](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14345) | [#14374](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14374) | Completed | 2026-10-23 | 2026-10-28 |
| Step 2: Identity and Reference Types Pattern | [#14539](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14539) | [#14545](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14545) | Completed | 2026-10-28 | 2026-10-29 |
| Step 3: Create a Round-Trip KRM Fuzzer | [#14558](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14558) | [#14562](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14562) | PR Created | 2026-10-29 | - |
| Step 4: Ensure MockGCP matches real gcp behavior | - | - | Pending | - | - |
| Step 5: Implement Direct Controller & E2E Fixtures | - | - | Pending | - | - |
| Step 6: Validate Direct Promotion | - | - | Pending | - | - |

## Status Updates
- **2026-10-29**: PR [#14562](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14562) created for Step 3 (Round-trip KRM fuzzer) and all CI checks passed. Waiting for PR review and merge.
- **2026-10-29**: Step 2 completed (PR [#14545](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14545) merged). Step 3 issue [#14558](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14558) created to implement round-trip KRM fuzzer for `AccessContextManagerGCPUserAccessBinding`.
- **2026-10-29**: PR [#14545](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14545) created for Step 2 (Identity and refs pattern) and all CI checks passed. Waiting for PR review and merge.
- **2026-10-28**: Step 1 completed (PR [#14374](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14374) merged). Step 2 issue [#14539](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14539) created to move `AccessContextManagerGCPUserAccessBinding` to identity and references pattern.
- **2026-10-24**: PR [#14374](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14374) created for Step 1 (Direct API types) and all CI checks passed. Waiting for PR review and merge.
- **2026-10-23**: Migration started for `AccessContextManagerGCPUserAccessBinding`. Step 1 issue #14345 created for direct KRM types and generate.sh configuration.
