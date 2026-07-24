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

import argparse
import json
import re
import subprocess
import sys

TEAM = [
    'acpana',
    'anfernee',
    'anhdle-sso',
    'barney-s',
    'gemmahou',
    'maqiuyujoyce'
]

def fetch_open_prs():
    print("Fetching all open PRs...", file=sys.stderr)
    prs = []
    page = 1
    while True:
        cmd = [
            'gh', 'api',
            f'repos/GoogleCloudPlatform/k8s-config-connector/pulls?state=open&per_page=100&page={page}'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        page_prs = json.loads(result.stdout)
        if not page_prs:
            break
        prs.extend(page_prs)
        page += 1
    print(f"Fetched {len(prs)} open PRs.", file=sys.stderr)
    return prs

def extract_issue_ids(title, body):
    text = f"{title or ''}\n{body or ''}"
    # Matches patterns like #1234
    issues = re.findall(r'#(\d+)', text)
    return sorted(list(set(int(issue) for issue in issues)))

def main():
    parser = argparse.ArgumentParser(description="PR Review Workload Balancer")
    parser.add_argument("--dry-run", action="store_true", help="Do not execute assignment commands, only show plan")
    args = parser.parse_args()

    try:
        open_prs = fetch_open_prs()
    except subprocess.CalledProcessError as e:
        print(f"Error fetching PRs: {e.stderr}", file=sys.stderr)
        sys.exit(1)

    # Step 1: Audit Current Team Workloads & Multilevel Workflow Mapping
    workload = {member: 0 for member in TEAM}
    tracking_issue_to_reviewer = {}

    for pr in open_prs:
        requested_reviewers = [r['login'] for r in pr.get('requested_reviewers', [])]
        # Count workloads for each team member
        for reviewer in requested_reviewers:
            if reviewer in workload:
                workload[reviewer] += 1
                # Build workflow affinity mapping
                issue_ids = extract_issue_ids(pr.get('title', ''), pr.get('body', ''))
                for issue_id in issue_ids:
                    tracking_issue_to_reviewer[issue_id] = reviewer

    print("\nCurrent Team Workloads:")
    for member in TEAM:
        print(f"  {member}: {workload[member]} assigned reviews")

    # Step 2: Fetch Unassigned Candidate PRs
    # Filter candidates: labeled "ready-for-human" and has NO team members in requested_reviewers
    candidates = []
    for pr in open_prs:
        labels = [label['name'] for label in pr.get('labels', [])]
        if 'ready-for-human' not in labels:
            continue
        
        requested_reviewers = [r['login'] for r in pr.get('requested_reviewers', [])]
        has_team_reviewer = any(r in TEAM for r in requested_reviewers)
        if not has_team_reviewer:
            candidates.append(pr)

    print(f"\nFound {len(candidates)} unassigned 'ready-for-human' candidate PRs.")

    # Sort candidates by number to keep assignments deterministic (oldest first)
    candidates.sort(key=lambda x: x['number'])

    # Step 3: Assignment Algorithm
    assignments = [] # list of (pr_number, pr_title, reviewer, reason)

    for pr in candidates:
        # Check if all team members reached hard ceiling of 10
        if all(workload[m] >= 10 for m in TEAM):
            print("All team members have reached the hard ceiling of 10 assigned reviews. Skipping remaining candidates.")
            break

        issue_ids = extract_issue_ids(pr.get('title', ''), pr.get('body', ''))
        
        selected_reviewer = None
        assignment_reason = ""

        # Priority 1: Workflow Affinity
        for issue_id in issue_ids:
            if issue_id in tracking_issue_to_reviewer:
                reviewer = tracking_issue_to_reviewer[issue_id]
                if workload[reviewer] < 10:
                    selected_reviewer = reviewer
                    assignment_reason = f"Workflow Affinity (matching issue #{issue_id})"
                    break

        # Priority 2: Underloaded Balancing (C_user < 5)
        if not selected_reviewer:
            underloaded_members = [m for m in TEAM if workload[m] < 5]
            if underloaded_members:
                # Select the member with the lowest C_user
                underloaded_members.sort(key=lambda m: (workload[m], m))
                selected_reviewer = underloaded_members[0]
                assignment_reason = f"Underloaded Balancing (workload {workload[selected_reviewer]} < 5)"

        # Priority 3: Capacity Absorption (5 <= C_user < 10)
        if not selected_reviewer:
            capacity_members = [m for m in TEAM if workload[m] < 10]
            if capacity_members:
                # Select the member with the lowest C_user
                capacity_members.sort(key=lambda m: (workload[m], m))
                selected_reviewer = capacity_members[0]
                assignment_reason = f"Capacity Absorption (workload {workload[selected_reviewer]} < 10)"

        if selected_reviewer:
            workload[selected_reviewer] += 1
            # Update workflow affinity for all issues in this PR
            for issue_id in issue_ids:
                tracking_issue_to_reviewer[issue_id] = selected_reviewer
            assignments.append((pr['number'], pr['title'], selected_reviewer, assignment_reason))

    # Step 4: Execute Assignments & Exit
    if not assignments:
        print("\nNo new assignments to make.")
        sys.exit(0)

    print("\nPlanned Assignments:")
    for pr_number, pr_title, reviewer, reason in assignments:
        print(f"  PR #{pr_number} ('{pr_title}') -> {reviewer} [{reason}]")

    if args.dry_run:
        print("\nDry-run mode. No commands executed.")
    else:
        print("\nExecuting assignments...")
        for pr_number, pr_title, reviewer, reason in assignments:
            cmd = [
                'gh', 'pr', 'edit', str(pr_number),
                '--repo', 'GoogleCloudPlatform/k8s-config-connector',
                '--add-reviewer', reviewer
            ]
            print(f"Running: {' '.join(cmd)}")
            try:
                subprocess.run(cmd, check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                print(f"Error assigning reviewer {reviewer} to PR #{pr_number}: {e.stderr}", file=sys.stderr)

        print("\nAssignments execution completed successfully.")
        print("\nUpdated Team Workloads:")
        for member in TEAM:
            print(f"  {member}: {workload[member]} assigned reviews")

if __name__ == "__main__":
    main()
