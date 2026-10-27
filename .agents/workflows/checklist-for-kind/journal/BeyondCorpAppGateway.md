# Migration Progress: BeyondCorpAppGateway

## Current Step
Step 2: Identity and Reference Types Pattern

## Progress Tracking

| Step | Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Direct API Types | [#14347](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14347) | [#14365](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14365) | Merged | 2026-10-23 | 2026-10-27 |
| 2 | Identity and Reference Types Pattern | [#14466](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14466) | [#14467](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14467) | PR Created | 2026-10-27 | - |
| 3 | Create a Round-Trip KRM Fuzzer | - | - | Pending | - | - |
| 4 | Ensure MockGCP matches real gcp behavior | - | - | Pending | - | - |
| 5 | Implement Direct Controller & E2E Fixtures | - | - | Pending | - | - |
| 6 | Validate Direct Promotion | - | - | Pending | - | - |

## Status Updates
- **2026-10-27**: Pull Request [#14467](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14467) created for Step 2. All CI checks and automated review passed; waiting for human review and merge.
- **2026-10-27**: Step 1 PR [#14365](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14365) merged and Issue [#14347](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14347) closed. Created Step 2 issue [#14466](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14466) to implement canonical identity and reference types for `BeyondCorpAppGateway`.
- **2026-10-24**: Pull Request [#14365](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/14365) created for Step 1. All CI checks and automated review passed; waiting for human review and merge.
- **2026-10-23**: Initialized direct migration tracking for `BeyondCorpAppGateway`. Verified existing CRD is at `v1alpha1` managed by Terraform controller. Created Step 1 issue [#14347](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14347) to implement direct KRM types and update `generate.sh`.
