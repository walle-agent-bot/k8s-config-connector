# Migration Journal: ComputeDisk

## Current Step
Step 5: Implement Direct Controller & E2E Fixtures

## Migration Progress

| Step Number & Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|---|---|---|---|---|---|
| Step 1: Direct API Types | [#9822](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/9822) | [#10045](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10045) | Merged | 2026-06-13 | 2026-06-13 |
| Step 2: Identity and Reference Types Pattern | [#10188](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10188) | [#10189](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10189) | Merged | 2026-06-13 | 2026-06-13 |
| Step 3: Create a Round-Trip KRM Fuzzer | [#10437](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10437) | [#10438](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10438) | Merged | 2026-06-18 | 2026-06-18 |
| Step 4: Ensure MockGCP matches real gcp behavior | N/A | [#1189](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/1189) | Merged | N/A | 2026-06-10 |
| Step 5: Implement Direct Controller & E2E Fixtures | [#10508](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10508) | [#10511](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10511) | PR Created | 2026-06-19 | |

## Status Updates
* **2026-06-21**: PR #10511 is currently open with changes requested by reviewer `justinsb`. Re-assigned PR to `codebot-robot` to implement specialized update methods (Resize, SetLabels, etc.) and add update.yaml tests to zonalcomputedisk.
