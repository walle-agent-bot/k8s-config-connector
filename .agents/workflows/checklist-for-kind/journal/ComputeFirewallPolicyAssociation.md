# Migration Journal: ComputeFirewallPolicyAssociation

## Current Step
Step 2: Identity and Reference Types Pattern

## Migration Progress

| Step | Name | Issue | Pull Request | Status | Date Started | Date Completed |
|------|------|-------|--------------|--------|--------------|----------------|
| 1 | Direct API Types | [#9976](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/9976) | [#10068](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/10068) | Merged | 2026-06-13 | 2026-07-01 |
| 2 | Identity and Reference Types Pattern | [#11217](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/11217) | [#11239](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11239) | PR Created | 2026-07-02 | - |
| 3 | Create a Round-Trip KRM Fuzzer | - | - | Pending | - | - |
| 4 | Ensure MockGCP matches real gcp behavior | - | - | Pending | - | - |
| 5 | Implement Direct Controller & E2E Fixtures | - | - | Pending | - | - |
| 6 | Validate Direct Promotion | - | - | Pending | - | - |

## Status Updates
* **2026-07-31**: Checked Step 2 PR #11239. All CI checks are passing successfully. The PR is open and awaiting human review.
* **2026-07-30**: Checked Step 2 PR #11239. It remains open with all CI checks passing. Migration is currently blocked waiting for a human review and merge of this PR.
* **2026-07-29**: Initialized the migration tracking journal for `ComputeFirewallPolicyAssociation`. Verified that Step 1 is fully complete and merged (#10068).
* **2026-07-29**: Checked the status of Step 2 PR #11239 ("Move ComputeFirewallPolicyAssociation to identity and refs pattern"). All CI checks are successfully passing (SUCCESS). The PR is currently waiting for human approver review (`REVIEW_REQUIRED`).
