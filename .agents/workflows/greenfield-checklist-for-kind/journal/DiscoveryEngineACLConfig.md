# Migration Journal: DiscoveryEngineACLConfig

**Current Step:** Step 1 (Direct API Types and Identity and Reference Types Pattern)

## Progress Tracking

| Step | Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
| :--- | :--- | :----------- | :------------------ | :----- | :----------- | :------------- |
| 1 | Direct API Types and Identity and Reference Types Pattern | [#12020](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12020) | [#12043](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12043) | PR Created (Passing CI) | 2026-07-29 | - |
| 2 | Direct Controller, E2E fixtures and Fuzzer | - | - | Pending | - | - |
| 3 | MockGCP Generation | - | - | Pending | - | - |
| 4 | MockGCP Alignment with RealGCP | - | - | Pending | - | - |

## Update Logs
- **2026-07-29**: Checked status of PR [#12043](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12043). All 150+ CI check-runs remain fully passing. The PR is open and awaiting human OWNER review and merge to complete Step 1.
- **2026-07-29**: Verified PR [#12043](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12043) is still open and all CI checks are completed and passing. The PR is awaiting human OWNER review and merge to complete Step 1.
- **2026-07-29**: Monitored PR [#12043](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12043). Confirmed that all CI checks are fully passing. The PR remains open and is awaiting human review and merge from OWNERS to complete Step 1.
- **2026-07-29**: Re-checked PR [#12043](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12043). Verified that all 150+ CI check-runs have completed successfully and are passing. The PR remains open, awaiting human OWNER review and merge before we can proceed to Step 2.
- **2026-07-29**: Re-verified PR [#12043](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12043). All 150+ CI checks continue to pass. The PR is still open and awaiting human OWNER review and merge before we can proceed to Step 2.
- **2026-07-29**: Monitored PR [#12043](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12043). All 150+ CI checks continue to pass. The PR is open and awaiting human OWNER review and merge to complete Step 1.
- **2026-07-29**: Re-verified PR [#12043](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12043). All 150+ CI check-runs have successfully completed and are passing. The PR is still open and currently awaiting human OWNER review and merge to complete Step 1.
- **2026-07-29**: Re-checked PR [#12043](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12043). All CI checks are still fully passing. The PR remains open and is awaiting human review and merge from OWNERS before we can proceed to Step 2.
- **2026-07-29**: Re-checked PR [#12043](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12043). All CI check-runs have fully completed and are passing. The PR is still open and awaiting human review/approval from OWNERS to proceed to Step 2.
- **2026-07-29**: Monitored the progress of PR [#12043](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12043). All CI checks remain passing. The PR is currently open and awaiting human OWNER review and merge before we can proceed to Step 2.
- **2026-07-29**: Re-verified the status of PR [#12043](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12043). Confirmed that all completed CI checks continue to pass. The PR is currently awaiting human OWNER review and merge before we can proceed to Step 2.
- **2026-07-29**: Verified that all CI checks (including unit-tests, golangci-lint, tests-e2e-fixtures-discoveryengine, and validate-generated-files) are passing on PR [#12043](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12043). The PR is now ready for review and merge.
- **2026-07-29**: Diagnosed unit-tests failures on PR [#12043](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12043):
  - `TestCRDFieldPresenceInTestsForAlpha`: Missing field exceptions need to be added to `tests/apichecks/testdata/exceptions/alpha-missingfields.txt` for `discoveryengineaclconfigs`.
  - `TestCRDObjectTypes`: `discoveryengineaclconfigs.discoveryengine.cnrm.cloud.google.com` needs to be added to `knownInvalidCRDs` in `tests/apichecks/crds_test.go` because `status.observedState` is an empty object.
  The PR remains assigned to `hopper-coder-bot` to resolve these failures.
- **2026-07-29**: Initialized checklist and created Step 1 GitHub Issue [#12020](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12020) for generating DiscoveryEngineACLConfig types, identity, and generate.sh.
