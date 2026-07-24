#!/usr/bin/env python3
# Copyright 2026 Google LLC
#
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
from unittest.mock import patch, MagicMock
import dev.tasks.balance_reviews as br

class TestPRReviewWorkloadBalancer(unittest.TestCase):

    def test_extract_issue_ids(self):
        # Normal references in title and body
        self.assertEqual(br.extract_issue_ids("Fixes #1234", "Fixes #5678"), {1234, 5678})
        # Duplicate references
        self.assertEqual(br.extract_issue_ids("#1234 and #1234", "#1234"), {1234})
        # Empty inputs
        self.assertEqual(br.extract_issue_ids(None, None), set())
        # No numbers
        self.assertEqual(br.extract_issue_ids("No issues", "Just text"), set())

    def test_balance_reviews_underloaded_balancing(self):
        # All members underloaded (C_user < 5).
        # Should select the member with the lowest C_user. Ties broken alphabetically.
        prs = [
            # Open PRs with reviewers to establish workloads
            {"number": 1, "labels": [], "requested_reviewers": ["acpana"]}, # acpana: 1
            {"number": 2, "labels": [], "requested_reviewers": ["anfernee"]}, # anfernee: 1
            {"number": 3, "labels": [], "requested_reviewers": ["anhdle-sso"]}, # anhdle-sso: 1
            # Candidates to assign
            {"number": 10, "labels": ["ready-for-human"], "requested_reviewers": []},
            {"number": 11, "labels": ["ready-for-human"], "requested_reviewers": []},
        ]
        
        # Team order: ['acpana', 'anfernee', 'anhdle-sso', 'barney-s', 'gemmahou', 'maqiuyujoyce']
        # Initial workloads:
        # acpana: 1, anfernee: 1, anhdle-sso: 1, barney-s: 0, gemmahou: 0, maqiuyujoyce: 0
        # Candidates sorted by number ascending: 10, then 11
        # For PR 10:
        # Lowest workload underloaded: barney-s, gemmahou, maqiuyujoyce (all at 0)
        # Alphabetical tie-breaker: barney-s.
        # After PR 10: barney-s workload becomes 1.
        # For PR 11:
        # Lowest workload underloaded: gemmahou, maqiuyujoyce (both at 0)
        # Alphabetical tie-breaker: gemmahou.
        
        with patch('subprocess.run') as mock_run:
            br.balance_reviews(prs, br.TEAM, dry_run=False)
            
            # Assertions on subcommands executed
            self.assertEqual(mock_run.call_count, 2)
            # Call 1 should assign PR 10 to barney-s
            call_1_args = mock_run.call_args_list[0][0][0]
            self.assertIn("10", call_1_args)
            self.assertIn("barney-s", call_1_args)
            
            # Call 2 should assign PR 11 to gemmahou
            call_2_args = mock_run.call_args_list[1][0][0]
            self.assertIn("11", call_2_args)
            self.assertIn("gemmahou", call_2_args)

    def test_balance_reviews_workflow_affinity(self):
        # Workflow affinity check.
        # Candidate references an issue already reviewed by a team member.
        # That member is < 10, so they get preferred.
        prs = [
            # Open PR 1 references #1234, reviewed by anfernee (workload: 1)
            {"number": 1, "title": "Implement X #1234", "body": "", "labels": [], "requested_reviewers": ["anfernee"]},
            # Candidate references #1234
            {"number": 10, "title": "Align X #1234", "body": "", "labels": ["ready-for-human"], "requested_reviewers": []},
        ]
        
        with patch('subprocess.run') as mock_run:
            br.balance_reviews(prs, br.TEAM, dry_run=False)
            self.assertEqual(mock_run.call_count, 1)
            call_args = mock_run.call_args_list[0][0][0]
            self.assertIn("10", call_args)
            self.assertIn("anfernee", call_args) # Assigned to anfernee because of affinity to #1234

    def test_balance_reviews_capacity_absorption(self):
        # All members at least 5 workload, but some < 10.
        # Selection should use Priority 3: Lowest workload < 10.
        prs = []
        # Assign 5 reviews to everyone except maqiuyujoyce (who gets 6)
        for i, member in enumerate(br.TEAM):
            count = 6 if member == "maqiuyujoyce" else 5
            for j in range(count):
                prs.append({"number": i*10 + j, "labels": [], "requested_reviewers": [member]})
                
        # Candidate to assign
        prs.append({"number": 100, "labels": ["ready-for-human"], "requested_reviewers": []})
        
        # Initial workloads:
        # acpana: 5, anfernee: 5, anhdle-sso: 5, barney-s: 5, gemmahou: 5, maqiuyujoyce: 6
        # Underloaded (count < 5) is empty.
        # Candidate 100 should go to first in sorted assignable with lowest workload.
        # Lowest workload < 10 are acpana, anfernee, anhdle-sso, barney-s, gemmahou (all 5)
        # Sorted alphabetically: acpana.
        
        with patch('subprocess.run') as mock_run:
            br.balance_reviews(prs, br.TEAM, dry_run=False)
            self.assertEqual(mock_run.call_count, 1)
            call_args = mock_run.call_args_list[0][0][0]
            self.assertIn("100", call_args)
            self.assertIn("acpana", call_args)

    def test_balance_reviews_hard_ceiling_and_termination(self):
        # All members have reached 10 or more workload.
        # No more assignments should be made.
        prs = []
        for i, member in enumerate(br.TEAM):
            for j in range(10): # 10 reviews each
                prs.append({"number": i*10 + j, "labels": [], "requested_reviewers": [member]})
                
        # Candidate PR
        prs.append({"number": 200, "labels": ["ready-for-human"], "requested_reviewers": []})
        
        with patch('subprocess.run') as mock_run:
            br.balance_reviews(prs, br.TEAM, dry_run=False)
            mock_run.assert_not_called() # No assignments because everyone is at ceiling (10)

if __name__ == '__main__':
    unittest.main()
