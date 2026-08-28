# Greenfield Migration Journal: NotebooksRuntime

## Current Step
Step 1: Direct API Types and Identity and Reference Types Pattern

## Progress Tracking

| Step | Step Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|------|-----------|--------------|---------------------|--------|--------------|----------------|
| 1 | Direct API Types and Identity | [#12617](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/12617) | [#12618](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/12618) | PR Created | 2026-08-27 | - |
| 2 | Direct Controller, E2E & Fuzzer | - | - | Pending | - | - |
| 3 | mockGCP Generation | - | - | Pending | - | - |
| 4 | mockGCP Alignment | - | - | Pending | - | - |

## Status Updates
- **2026-08-28**: Monitored Step 1 PR [#12618]. Identified failing CI checks: `presubmit-gatekeeper`, `validate-manifests`, `unit-tests-1-of-4`, `validate-generated-files`. Standing by for the coder bot to resolve failures before merging.
- **2026-08-27**: Initialized Greenfield migration workflow for NotebooksRuntime. Created Step 1 issue [#12617] to implement KRM types and identity.
