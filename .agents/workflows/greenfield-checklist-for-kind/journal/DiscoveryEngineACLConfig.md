# Migration Journal: DiscoveryEngineACLConfig

**Current Step:** Step 1 (Direct API Types and Identity and Reference Types Pattern)

## Progress Tracking

| Step | Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
| :--- | :--- | :----------- | :------------------ | :----- | :----------- | :------------- |
| 1 | Direct API Types and Identity and Reference Types Pattern | [#12020](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12020) | [#12043](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12043) | PR Created (Failing CI) | 2026-07-29 | - |
| 2 | Direct Controller, E2E fixtures and Fuzzer | - | - | Pending | - | - |
| 3 | MockGCP Generation | - | - | Pending | - | - |
| 4 | MockGCP Alignment with RealGCP | - | - | Pending | - | - |

## Update Logs
- **2026-07-29**: Diagnosed unit-tests failures on PR [#12043](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12043):
  - `TestCRDFieldPresenceInTestsForAlpha`: Missing field exceptions need to be added to `tests/apichecks/testdata/exceptions/alpha-missingfields.txt` for `discoveryengineaclconfigs`.
  - `TestCRDObjectTypes`: `discoveryengineaclconfigs.discoveryengine.cnrm.cloud.google.com` needs to be added to `knownInvalidCRDs` in `tests/apichecks/crds_test.go` because `status.observedState` is an empty object.
  The PR remains assigned to `hopper-coder-bot` to resolve these failures.
- **2026-07-29**: Initialized checklist and created Step 1 GitHub Issue [#12020](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12020) for generating DiscoveryEngineACLConfig types, identity, and generate.sh.
