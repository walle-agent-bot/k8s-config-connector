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
from balance_reviews import select_reviewer, TEAM

class TestSelectReviewer(unittest.TestCase):

    def test_priority1_workflow_affinity(self):
        # A team member 'barney-s' is already reviewing issue 123.
        # Candidate PR also references issue 123.
        # 'barney-s' has under 10 reviews.
        # Should select 'barney-s'.
        workload = {member: 5 for member in TEAM}
        workload['barney-s'] = 6
        tracking_issue_to_reviewer = {"123": "barney-s"}
        
        selected, reason = select_reviewer(["123"], workload, tracking_issue_to_reviewer)
        self.assertEqual(selected, "barney-s")
        self.assertTrue("Workflow Affinity" in reason)

    def test_priority1_workflow_affinity_ceiling(self):
        # 'barney-s' is reviewing issue 123 but is at maximum capacity (10).
        # It should fall back to underloaded balancing.
        workload = {member: 3 for member in TEAM}
        workload['barney-s'] = 10
        workload['anhdle-sso'] = 1  # Lowest workload
        tracking_issue_to_reviewer = {"123": "barney-s"}
        
        selected, reason = select_reviewer(["123"], workload, tracking_issue_to_reviewer)
        self.assertEqual(selected, "anhdle-sso")
        self.assertTrue("Underloaded Balancing" in reason)

    def test_priority2_underloaded_balancing(self):
        # No workflow affinity matches.
        # Some members have < 5 reviews.
        # Select member with the lowest workload (gemmahou has 1).
        workload = {member: 4 for member in TEAM}
        workload['gemmahou'] = 1
        workload['anfernee'] = 2
        tracking_issue_to_reviewer = {}
        
        selected, reason = select_reviewer(["999"], workload, tracking_issue_to_reviewer)
        self.assertEqual(selected, "gemmahou")
        self.assertTrue("Underloaded Balancing" in reason)

    def test_priority3_capacity_absorption(self):
        # All members have >= 5 reviews.
        # No workflow affinity matches.
        # Select member with lowest workload who is < 10 (anfernee has 6).
        workload = {member: 8 for member in TEAM}
        workload['anfernee'] = 6
        workload['gemmahou'] = 10  # At ceiling
        tracking_issue_to_reviewer = {}
        
        selected, reason = select_reviewer(["999"], workload, tracking_issue_to_reviewer)
        self.assertEqual(selected, "anfernee")
        self.assertTrue("Capacity Absorption" in reason)

    def test_ceiling_reached(self):
        # All members are at maximum workload capacity of 10.
        # Should return None.
        workload = {member: 10 for member in TEAM}
        tracking_issue_to_reviewer = {}
        
        selected, reason = select_reviewer(["999"], workload, tracking_issue_to_reviewer)
        self.assertIsNone(selected)
        self.assertEqual(reason, "Ceiling Reached")

if __name__ == '__main__':
    unittest.main()
