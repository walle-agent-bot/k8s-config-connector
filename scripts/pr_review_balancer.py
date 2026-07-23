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

import json
import re
import subprocess
import sys

# Define the k8s-config-connector-team
TEAM = {
    "acpana",
    "anfernee",
    "anhdle-sso",
    "barney-s",
    "gemmahou",
    "maqiuyujoyce"
}

def extract_issue_numbers(text):
    if not text:
        return set()
    # Find all issue/PR numbers e.g. #1234
    matches = re.findall(r'#(\d+)', text)
    return {int(m) for m in matches}

def fetch_all_open_prs():
    print("Fetching open pull requests from GitHub REST API...")
    prs = []
    page = 1
    while True:
        url = f"repos/GoogleCloudPlatform/k8s-config-connector/pulls?state=open&per_page=100&page={page}"
        res = subprocess.run(["gh", "api", url], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Error fetching page {page}: {res.stderr}", file=sys.stderr)
            sys.exit(1)
        page_prs = json.loads(res.stdout)
        if not page_prs:
            break
        prs.extend(page_prs)
        if len(page_prs) < 100:
            break
        page += 1
    print(f"Successfully fetched {len(prs)} open PRs.")
    return prs

def balance_reviews():
    open_prs = fetch_all_open_prs()

    # Step 1: Audit workloads and build issue mapping
    workload = {member: 0 for member in TEAM}
    tracking_issue_to_reviewer = {}

    for pr in open_prs:
        reviewers = [r["login"] for r in pr.get("requested_reviewers", [])]
        team_reviewers = [r for r in reviewers if r in TEAM]
        if team_reviewers:
            issue_ids = extract_issue_numbers(pr.get("title", "")) | extract_issue_numbers(pr.get("body", ""))
            for reviewer in team_reviewers:
                workload[reviewer] += 1
                for issue_id in issue_ids:
                    tracking_issue_to_reviewer[issue_id] = reviewer

    print("\n--- Current Workloads (Open Assigned Reviews) ---")
    for member in sorted(TEAM):
        print(f"  {member}: {workload[member]}")

    # Step 2: Fetch and filter candidate PRs
    # A candidate is an open PR with 'ready-for-human' label and no team requested reviewers.
    candidate_prs = []
    for pr in open_prs:
        labels = [l["name"] for l in pr.get("labels", [])]
        if "ready-for-human" not in labels:
            continue
        
        reviewers = [r["login"] for r in pr.get("requested_reviewers", [])]
        team_reviewers = [r for r in reviewers if r in TEAM]
        if not team_reviewers:
            candidate_prs.append(pr)

    print(f"\nFound {len(candidate_prs)} unassigned candidate ready-for-human PRs.")

    # Step 3: Run the Assignment Algorithm
    assignments = [] # list of (pr_num, reviewer)

    for pr in candidate_prs:
        pr_num = pr["number"]
        pr_title = pr["title"]
        pr_body = pr.get("body") or ""
        extracted_issue_ids = extract_issue_numbers(pr_title) | extract_issue_numbers(pr_body)

        # Priority 1: Workflow Affinity
        selected_reviewer = None
        affinity_reviewers = []
        for issue_id in extracted_issue_ids:
            if issue_id in tracking_issue_to_reviewer:
                rev = tracking_issue_to_reviewer[issue_id]
                if workload[rev] < 10:
                    affinity_reviewers.append(rev)
        
        if affinity_reviewers:
            # Select the reviewer with the lowest workload for fairness among affinity matches
            selected_reviewer = min(affinity_reviewers, key=lambda r: (workload[r], r))
            reason = "Workflow Affinity"
        
        # Priority 2: Underloaded Balancing (C_user < 5)
        if not selected_reviewer:
            underloaded = [m for m in TEAM if workload[m] < 5]
            if underloaded:
                selected_reviewer = min(underloaded, key=lambda r: (workload[r], r))
                reason = "Underloaded Balancing (<5)"

        # Priority 3: Capacity Absorption (5 <= C_user < 10)
        if not selected_reviewer:
            capacitated = [m for m in TEAM if 5 <= workload[m] < 10]
            if capacitated:
                selected_reviewer = min(capacitated, key=lambda r: (workload[r], r))
                reason = "Capacity Absorption (<10)"

        if selected_reviewer:
            # Commit the assignment
            workload[selected_reviewer] += 1
            for issue_id in extracted_issue_ids:
                tracking_issue_to_reviewer[issue_id] = selected_reviewer
            assignments.append((pr_num, pr_title, selected_reviewer, reason))
        else:
            print(f"Skipping assignment for PR #{pr_num} ('{pr_title}') - all team members are at maximum capacity.")

    # Step 4: Execute Assignments & Print Summary
    if not assignments:
        print("\nNo new assignments to make.")
        return

    print("\n--- Scheduled Assignments ---")
    for pr_num, pr_title, reviewer, reason in assignments:
        print(f"  PR #{pr_num}: '{pr_title}' -> {reviewer} ({reason})")

    print("\nExecuting assignments...")
    for pr_num, pr_title, reviewer, reason in assignments:
        cmd = ["gh", "pr", "edit", str(pr_num), "--repo", "GoogleCloudPlatform/k8s-config-connector", "--add-reviewer", reviewer]
        print(f"Running: {' '.join(cmd)}")
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Failed to assign {reviewer} to PR #{pr_num}: {res.stderr}", file=sys.stderr)
        else:
            print(f"Successfully assigned {reviewer} to PR #{pr_num}")

    print("\n--- Updated Workloads ---")
    for member in sorted(TEAM):
        print(f"  {member}: {workload[member]}")

if __name__ == "__main__":
    balance_reviews()
