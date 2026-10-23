# Migration Progress: BeyondCorpAppGateway

## Current Step
Step 1: Direct API Types

## Progress Tracking

| Step | Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Direct API Types | [#14347](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14347) | - | Open | 2026-10-23 | - |
| 2 | Identity and Reference Types Pattern | - | - | Pending | - | - |
| 3 | Create a Round-Trip KRM Fuzzer | - | - | Pending | - | - |
| 4 | Ensure MockGCP matches real gcp behavior | - | - | Pending | - | - |
| 5 | Implement Direct Controller & E2E Fixtures | - | - | Pending | - | - |
| 6 | Validate Direct Promotion | - | - | Pending | - | - |

## Status Updates
- **2026-10-23**: Initialized direct migration tracking for `BeyondCorpAppGateway`. Verified existing CRD is at `v1alpha1` managed by Terraform controller. Created Step 1 issue [#14347](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/14347) to implement direct KRM types and update `generate.sh`.
