#!/usr/bin/env python3
# Copyright 2026 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
from dev.tasks.balance_reviews import extract_issue_ids, run_assignments, TEAM_MEMBERS

class TestBalanceReviews(unittest.TestCase):

    def test_extract_issue_ids(self):
        self.assertEqual(extract_issue_ids("Fixes #12345", ""), ["12345"])
        self.assertEqual(extract_issue_ids("chore: #111 and #222", "Workflow: #333"), ["111", "222", "333"])
        self.assertEqual(extract_issue_ids("No issues here", None), [])

    def test_run_assignments_workflow_affinity(self):
        # acpana already reviews issue #12345 on an open PR
        prs = [
            {
                "number": 1001,
                "title": "PR 1 addressing #12345",
                "body": "",
                "requested_reviewers": ["acpana"],
                "labels": []
            },
            # Candidate PR referencing #12345
            {
                "number": 1002,
                "title": "PR 2 addressing #12345",
                "body": "",
                "requested_reviewers": [],
                "labels": ["ready-for-human"]
            }
        ]
        assignments = run_assignments(prs, execute=False)
        self.assertEqual(len(assignments), 1)
        pr_num, user, reason = assignments[0]
        self.assertEqual(pr_num, 1002)
        self.assertEqual(user, "acpana")
        self.assertIn("Workflow Affinity", reason)

    def test_run_assignments_underloaded_balancing(self):
        # Everybody has 6 reviews, except 'anfernee' who has 2
        prs = []
        # Populate workloads:
        # acpana: 6, anhdle-sso: 6, barney-s: 6, gemmahou: 6, maqiuyujoyce: 6
        # anfernee: 2
        for i in range(6):
            prs.append({"number": 2000 + i, "title": "A", "body": "", "requested_reviewers": ["acpana"], "labels": []})
            prs.append({"number": 2100 + i, "title": "B", "body": "", "requested_reviewers": ["anhdle-sso"], "labels": []})
            prs.append({"number": 2200 + i, "title": "C", "body": "", "requested_reviewers": ["barney-s"], "labels": []})
            prs.append({"number": 2300 + i, "title": "D", "body": "", "requested_reviewers": ["gemmahou"], "labels": []})
            prs.append({"number": 2400 + i, "title": "E", "body": "", "requested_reviewers": ["maqiuyujoyce"], "labels": []})
        for i in range(2):
            prs.append({"number": 2500 + i, "title": "F", "body": "", "requested_reviewers": ["anfernee"], "labels": []})

        # One candidate
        prs.append({
            "number": 3000,
            "title": "Unassigned candidate",
            "body": "",
            "requested_reviewers": [],
            "labels": ["ready-for-human"]
        })

        assignments = run_assignments(prs, execute=False)
        self.assertEqual(len(assignments), 1)
        pr_num, user, reason = assignments[0]
        self.assertEqual(pr_num, 3000)
        self.assertEqual(user, "anfernee")
        self.assertIn("Underloaded Balancing", reason)

    def test_run_assignments_hard_ceiling(self):
        # All members have 10 reviews
        prs = []
        for member in TEAM_MEMBERS:
            for i in range(10):
                prs.append({"number": 4000 + i, "title": "X", "body": "", "requested_reviewers": [member], "labels": []})

        # Candidate
        prs.append({
            "number": 5000,
            "title": "Ready for human but all at ceiling",
            "body": "",
            "requested_reviewers": [],
            "labels": ["ready-for-human"]
        })

        assignments = run_assignments(prs, execute=False)
        self.assertEqual(len(assignments), 0)

if __name__ == "__main__":
    unittest.main()
