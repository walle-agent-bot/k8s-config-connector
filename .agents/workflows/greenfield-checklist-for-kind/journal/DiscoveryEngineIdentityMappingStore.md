# Greenfield Migration Journal: DiscoveryEngineIdentityMappingStore

This journal tracks the migration process of the greenfield resource `DiscoveryEngineIdentityMappingStore` to a production-ready direct controller.

## Current Step
Step 2: Direct Controller, E2E fixtures and Fuzzer

## Progress Tracking

| Step Number & Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|---|---|---|---|---|---|
| Step 1: Direct API Types & Identity | [#8712](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/8712) | [#8775](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/8775) | Merged | 2026-05-27 | 2026-05-27 |
| Step 2: Direct Controller, E2E & Fuzzer | [#8883](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/8883) | [#11165](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11165) | PR Created | 2026-06-01 | - |
| Step 3: mockGCP Generation | - | - | - | - | - |
| Step 4: MockGCP Alignment | - | - | - | - | - |

## Status Update Notes

- **2026-07-02**: Monitored PR [#11165](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11165). Confirmed that the remaining E2E checks (`tests-e2e-fixtures-compute` and `tests-e2e-fixtures-bigquery`) are still in progress, while all other validations have successfully passed. Waiting for the PR to merge.
- **2026-07-02**: Checked CI status of PR [#11165](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11165). Verified that the previously failing checks (`unit-tests` and `fuzz-roundtrippers`) have now successfully passed, and the remaining E2E checks are in progress with no failures.
- **2026-07-02**: Checked CI status of Pull Request [#11165](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11165). Detected failing checks: `unit-tests` and `fuzz-roundtrippers`. Confirmed that the PR is currently assigned to `codebot-robot` for triage and resolution.
- **2026-07-02**: Detected failing CI check `fuzz-roundtrippers` on Pull Request [#11165](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11165). Assigned the PR back to the author bot `codebot-robot` to trigger triage and fixes.
- **2026-07-02**: Successfully re-triggered Step 2 controller implementation by re-assigning Issue #8883 to the developer bot. This initiated a brand-new Pull Request [#11165](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11165).
- **2026-07-02**: Step 2 controller implementation was previously attempted under PR #8889, but the PR was closed without being merged.
- **2026-07-02**: Initialized migration tracking journal for `DiscoveryEngineIdentityMappingStore`. Step 1 was successfully completed and merged on 2026-05-27.
