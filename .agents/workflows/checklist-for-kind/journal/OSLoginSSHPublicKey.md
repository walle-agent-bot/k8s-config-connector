# Migration Progress for OSLoginSSHPublicKey

### Current Step
- **Step 3: Create a Round-Trip KRM Fuzzer**

### Migration Progress Tracking

| Step | Step Name | GitHub Issue | GitHub Pull Request | Status | Date Started | Date Completed |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Implement direct KRM types and generate.sh | [#13822](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/13822) | [#13828](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13828) | Completed | 2026-10-08 | 2026-10-08 |
| 2 | Move OSLoginSSHPublicKey to identity and refs pattern | [#13839](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/13839) | [#13844](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13844) | Completed | 2026-10-08 | 2026-10-09 |
| 3 | Implement round-trip KRM fuzzer | [#13881](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/13881) | - | Open | 2026-10-09 | - |
| 4 | Match real GCP behavior in MockGCP | - | - | Pending | - | - |
| 5 | Implement direct controller and test fixtures | - | - | Pending | - | - |
| 6 | Validate direct promotion for OSLoginSSHPublicKey | - | - | Pending | - | - |

### Status Update Notes
- **2026-10-08**: Initiated migration workflow for OSLoginSSHPublicKey. Created child issue #13822 for Step 1: Implement direct KRM types and generate.sh for OSLoginSSHPublicKey.
- **2026-10-08**: Step 1 completed. PR #13828 merged and child issue #13822 closed.
- **2026-10-08**: Initiated Step 2. Created child issue #13839 for Move OSLoginSSHPublicKey to identity and refs pattern.
- **2026-10-09**: Step 2 completed. PR #13844 merged and child issue #13839 closed.
- **2026-10-09**: Initiated Step 3. Created child issue #13881 for Implement round-trip KRM fuzzer for OSLoginSSHPublicKey.
