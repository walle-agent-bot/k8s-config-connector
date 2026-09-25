<!--
Copyright 2026 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Greenfield Migration Journal: NetworkSecurityAddressGroup

## Current Status
*   **Current Step:** Step 3: mockGCP generation
*   **Last Update:** 2026-09-25

## Progress Tracking

| Step | Name | Issue | PR | Status | Date Started | Date Completed |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | Direct API Types and Identity and Reference Types Pattern | [#8720](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/8720) | [#8755](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/8755) | Merged | 2026-05-27 | 2026-06-19 |
| **2** | Direct Controller, E2E fixtures and Fuzzer | [#13331](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/13331) | [#13332](https://github.com/GoogleCloudPlatform/k8s-config-connector/pull/13332) | Merged | 2026-09-19 | 2026-09-25 |
| **3** | mockGCP generation | [#13453](https://github.com/GoogleCloudPlatform/k8s-config-connector/issues/13453) | - | Open | 2026-09-25 | - |
| **4** | MockGCP Alignment with RealGCP | - | - | - | - | - |

## Step Notes & Updates

### 2026-09-25: Step 3 Started
*   Step 2 completed and merged under PR #13332.
*   Created Issue #13453 to track Step 3: Implementing MockGCP and Alignment for `NetworkSecurityAddressGroup`.

### 2026-09-19: Step 2 Started
*   Step 1 was previously completed and merged under Issue #8720 and PR #8755.
*   Created Issue #13331 to track Step 2: Implementing direct controller, E2E fixtures, and fuzzer for `NetworkSecurityAddressGroup`.
