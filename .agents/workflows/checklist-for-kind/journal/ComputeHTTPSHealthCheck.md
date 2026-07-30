# Migration Progress: ComputeHTTPSHealthCheck

This journal tracks the migration progress of the `ComputeHTTPSHealthCheck` resource to a direct controller.

## Current Status
*   **Current Step:** Step 6: Validate Direct Promotion
*   **Status:** Open - GitHub Issue #12072 created to validate the direct promotion of ComputeHTTPSHealthCheck.

## Migration Progress Table

| Step | Step Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|---|---|---|---|---|---|---|
| 1 | Direct API Types | [#9982](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/9982) | [#10927](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10927) | Completed | 2026-06-25 | 2026-06-28 |
| 2 | Identity and Reference Types Pattern | [#9982](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/9982) | [#10927](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10927) | Completed | 2026-06-25 | 2026-06-28 |
| 3 | Create a Round-Trip KRM Fuzzer | [#10929](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10929) | [#10931](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10931) | Completed | 2026-06-28 | 2026-06-28 |
| 4 | Ensure MockGCP matches real gcp behavior | [#10936](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10936) | [#10937](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10937) | Completed | 2026-06-28 | 2026-06-28 |
| 5 | Implement Direct Controller & E2E Fixtures | [#10923](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10923) | [#10937](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10937) | Completed | 2026-06-28 | 2026-06-28 |
| 6 | Validate Direct Promotion | [#12072](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12072) | - | Open | 2026-07-29 | - |

## Updates Log
*   **2026-07-30:** Step 6 in progress. AI Factory sandbox is working on direct promotion validation under issue #12072.
*   **2026-07-29:** Step 6 initialized. Created GitHub Issue #12072 for direct promotion validation.
