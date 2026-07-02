# Greenfield Migration Journal: MapsPlatformDatasetsDataset

Current Step: Step 1: Direct API Types and Identity and Reference Types Pattern

## Migration Progress

| Step | Name | Issue | Pull Request | Status | Date Started | Date Completed |
|------|------|-------|--------------|--------|--------------|----------------|
| 1 | Direct KRM types, identity, and generate.sh | [#10285](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/10285) | [#11167](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/11167) | PR Created | 2026-07-02 | |
| 2 | Direct controller, E2E fixtures, and fuzzer | | | Planned | | |
| 3 | mockGCP generation | | | Planned | | |
| 4 | MockGCP Alignment with RealGCP | | | Planned | | |

## Status Update Notes
- **2026-07-02**: Verified that PR #11167 has failed CI checks (validate-generated-files, unit-tests, unit-tests-operator, validations). Confirmed that argus-watcher-bot is actively investigating and working on the fixes in a sandbox, with the PR assigned to ada-coder-bot.
- **2026-07-02**: Detected active PR #11167 for Step 1 created by `ada-coder-bot`. Some CI checks failed (`validations`, `unit-tests-operator`, `validate-generated-files`). Assigned PR to the author bot `ada-coder-bot` to trigger automated troubleshooting/fixes.
- **2026-07-02**: Confirmed that sandbox bot actively restarted fixing the issue in a sandbox today at 06:30 UTC after previous PR #10296 was closed. Currently waiting for the new PR to be created.
- **2026-07-02**: Initialized migration journal. Verified Step 1 is active with issue #10285 and is currently being worked on by the sandbox bot.
