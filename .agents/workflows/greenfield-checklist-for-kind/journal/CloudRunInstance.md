# Greenfield Migration Journal: CloudRunInstance

## Current Step
Step 1: Direct API Types and Identity and Reference Types Pattern

## Migration Progress

| Step Number & Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
|---|---|---|---|---|---|
| Step 1: Direct API Types, Identity, Reference | [#8718](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/8718), [#9005](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/9005) | [#9008](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/9008) | PR Created | 2026-06-02 | |
| Step 2: Direct Controller, E2E fixtures & Fuzzer | | | Pending | | |
| Step 3: mockGCP generation | | | Pending | | |
| Step 4: MockGCP Alignment with RealGCP | | | Pending | | |

## Status Notes
- **2026-07-26**: Monitored issue #11935. Verified `ada-coder-bot` is currently assigned to resolve the merge conflict in PR #9008 and is actively working on it in a sandbox. PR #9008 remains open in conflict (`mergeable: CONFLICTING`) and unassigned, awaiting automated conflict resolution by the coder bot to proceed.
- **2026-07-26**: Checked PR #9008 status. Verified the PR is open but remains in conflict (`mergeable: CONFLICTING`) and unassigned. Automated rebase attempts by `codebot-robot` have been failing immediately. Opened a new child issue #11935 for a coder bot to checkout the branch, resolve the merge conflicts in `pkg/gcpurls/registry_test.go`, and rebase/push to unblock Step 1.
- **2026-07-26**: Confirmed all 21/21 CI checks on the head commit (`02fb32f`) of PR #9008 remain 100% green and passing.
- **2026-07-26**: Checked PR #9008 status. Verified the PR is open but remains in conflict (`mergeable_state: dirty`) and unassigned after `codebot-robot` completed previous rebase attempt. Successfully re-assigned author bot `codebot-robot` to re-trigger automated conflict resolution. Re-verified all CI checks on head commit `02fb32f` remain 100% green.
- **2026-07-26**: Re-assigned author bot `codebot-robot` to PR #9008 via the GitHub REST API to re-trigger the automated merge conflict resolution and rebase workflow, as the PR remains open and in a conflicting state (`mergeable_state: dirty`).
- **2026-07-26**: Re-verified PR #9008 status. Confirmed `codebot-robot` is now assigned to the PR to trigger automatic conflict resolution and a rebase. Awaiting the automated rebase and subsequent human OWNER review.
- **2026-07-26**: Checked PR #9008 status. Verified the PR is open but remains in conflict (`mergeable: CONFLICTING`) and unassigned. Successfully assigned the author bot `codebot-robot` via the GitHub REST API to trigger automatic merge conflict resolution and a rebase.
- **2026-07-10**: Monitored PR #9008 status. Checked and re-verified all completed and paginated CI checks on the latest head commit (`02fb32f`) are 100% green. The PR remains open, unassigned, and awaiting human OWNER review and merge.
- **2026-07-09**: Monitored PR #9008 status. Re-verified all completed and paginated CI checks remain 100% green and successful on the latest head commit (`02fb32f`). The PR remains open and is awaiting human OWNER review and merge.
- **2026-07-08**: Monitored PR #9008 status. Re-verified all completed and paginated CI checks remain 100% green and successful on the head commit (`02fb32f`) with no failures or merge conflicts. The PR is open, unassigned, and currently awaiting human OWNER review and merge.
- **2026-07-07**: Checked PR #9008 status. Re-verified all completed and paginated CI checks remain 100% green and successful on the head commit (`02fb32f`) with no failures or merge conflicts. The PR is open, unassigned, and currently awaiting human OWNER review and merge.
- **2026-06-02**: Initialized migration tracking for CloudRunInstance. Opened follow-up issue #9005 and PR #9008 to address deferred technical debt and feedback on direct types, identity implementation, and acronym casing.
