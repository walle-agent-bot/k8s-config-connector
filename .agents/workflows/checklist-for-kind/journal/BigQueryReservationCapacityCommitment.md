# Migration Progress Journal: BigQueryReservationCapacityCommitment

## Current Step
**Step 6: Validate Direct Promotion**

## Progress Tracking

| Step | Step Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 1 | Direct API Types | [#9425](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/9425) | [#9431](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/9431) | Merged | 2026-06-07 | 2026-06-07 |
| 2 | Identity and Reference Types Pattern | [#9507](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/9507) | [#9510](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/9510) | Merged | 2026-06-07 | 2026-06-07 |
| 3 | Create a Round-Trip KRM Fuzzer | [#9524](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/9524) | [#9528](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/9528) | Merged | 2026-06-07 | 2026-06-07 |
| 4 | Ensure MockGCP matches real gcp behavior | N/A | N/A | Completed | 2026-07-02 | 2026-07-02 |
| 5 | Implement Direct Controller & E2E Fixtures | [#9562](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/9562) | [#9577](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/9577) | Merged | 2026-07-02 | 2026-07-02 |
| 6 | Validate Direct Promotion | [#12070](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12070) | [#12107](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12107) | Open (Checks Passing) | 2026-07-29 | |

## Migration Notes
- **2026-07-31 (16:16 UTC)**: Monitored progress. Verified that all 201 CI check-runs for PR [#12107](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12107) remain fully successful (all green). The PR is pending human OWNER review and approval.
- **2026-07-31 (15:32 UTC)**: Monitored progress. Verified that all 201 CI check-runs for PR [#12107](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12107) remain fully successful (all green). The PR is pending human OWNER review and approval.
- **2026-07-31 (12:38 UTC)**: Monitored progress. Verified that all CI check-runs for PR [#12107](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12107) remain fully successful (all green). The PR is pending human OWNER review and approval.
- **2026-07-31 (10:06 UTC)**: Monitored progress. Verified that all 201 CI check-runs on PR [#12107](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12107) remain fully successful (all green). The direct promotion validation is complete and remains open pending human OWNER review and approval.
- **2026-07-31 (07:42 UTC)**: Monitored progress. Verified that all 201 CI check-runs on PR [#12107](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12107) remain fully successful (all green). The direct promotion validation is complete and remains open pending human OWNER review and approval.
- **2026-07-31 (05:15 UTC)**: Monitored progress. Verified that all 201 CI check-runs on PR [#12107](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12107) remain fully successful (all green). The direct promotion validation is complete and remains open pending human OWNER review and approval.
- **2026-07-31 (02:53 UTC)**: Monitored progress. Verified that all 201 CI check-runs on PR [#12107](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12107) remain fully successful (all green). The direct promotion validation is complete and remains open pending human OWNER review and approval.
- **2026-07-31 (00:38 UTC)**: Monitored progress. Verified that all 201 CI check-runs on PR [#12107](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12107) remain fully successful (all green). The direct promotion validation is complete and remains open pending human OWNER review and approval.
- **2026-07-30 (22:27 UTC)**: Monitored progress. Verified that all 145 CI check-runs on PR [#12107](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12107) remain fully successful (all green). The direct promotion validation is complete and remains open pending human OWNER review and approval.
- **2026-07-30 (20:10 UTC)**: Monitored progress. Verified that all 145 CI check-runs on PR [#12107](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12107) remain fully successful (all green). The direct promotion validation is complete and remains open pending human OWNER review and approval.
- **2026-07-30 (17:52 UTC)**: Monitored progress. Verified that all CI check-runs for PR [#12107](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12107) remain fully successful (all green). The validation for `BigQueryReservationCapacityCommitment` direct promotion is complete, and the PR remains open pending human OWNER review and approval.
- **2026-07-30 (15:26 UTC)**: Monitored progress. Verified that PR [#12107](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12107) remains open with all CI checks successfully passing (all green). The direct promotion validation is ready and pending human OWNER review and approval.
- **2026-07-30 (12:55 UTC)**: Monitored progress. All CI check-runs on PR [#12107](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12107) are passing successfully (all green). The direct promotion validation remains open, pending human OWNER review and approval.
- **2026-07-30 (10:44 UTC)**: Monitored progress. Verified that all CI check-runs for PR [#12107](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12107) have now passed successfully (all green). The direct promotion validation for `BigQueryReservationCapacityCommitment` is fully validated and ready for human OWNER review and approval.
- **2026-07-30 (07:45 UTC)**: Monitored progress. Verified that `ada-coder-bot` successfully resolved the previous CI failures (missing default-controller label in CRD and outdated golden files). However, a new failure was detected in `crd-equivalence-check` because the newly added `cnrm.cloud.google.com/default-controller: direct` label was flagged as a non-equivalent change. Re-assigning the PR to `ada-coder-bot` to resolve the check failure.
- **2026-07-30 (05:30 UTC)**: Identified that `ada-coder-bot` opened PR [#12107](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12107). Found CI check failures in `validate-generated-files` (missing default-controller label in CRD) and `tests-e2e-fixtures-bigqueryreservation` (old-controller golden files need to be deleted). Assigning the PR to `ada-coder-bot` for automated fixing.
- **2026-07-30 (02:30 UTC)**: Monitored progress. Verified that the automated sandbox run (assigned to `ada-coder-bot`) is currently active and in progress for validating the direct promotion of `BigQueryReservationCapacityCommitment`.
- **2026-07-29**: Step 6 initiated. Issue #12070 created to validate direct promotion.
- **2026-07-02**: Controller and mock logic verified and merged under PR #9577.
- **2026-06-07**: Initial types and references implemented and fuzzer created under PR #9431, PR #9510, and PR #9528.
