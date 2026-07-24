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

# Define team members
TEAM = ['acpana', 'anfernee', 'anhdle-sso', 'barney-s', 'gemmahou', 'maqiuyujoyce']

def extract_issue_ids(title, body):
    """Extracts all referenced issue numbers prefixed with '#' from title and body."""
    title = title or ""
    body = body or ""
    issues = set()
    for match in re.findall(r'#(\d+)', title):
        issues.add(int(match))
    for match in re.findall(r'#(\d+)', body):
        issues.add(int(match))
    return issues

def fetch_open_prs():
    """Fetches all open PRs in the repository using GitHub REST API via gh cli."""
    cmd = [
        "gh", "api", "--paginate", 
        "repos/GoogleCloudPlatform/k8s-config-connector/pulls?state=open&per_page=100", 
        "--jq", ".[] | {number: .number, title: .title, body: .body, labels: [.labels[].name], requested_reviewers: [.requested_reviewers[].login]}"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    prs = []
    for line in result.stdout.strip().split('\n'):
        if line.strip():
            prs.append(json.loads(line))
    return prs

def balance_reviews(prs, team, dry_run=False):
    """Balances ready-for-human review assignments among team members."""
    # Step 1: Audit Current Team Workloads & Multilevel Workflow Mapping
    workload = {member: 0 for member in team}
    tracking_issue_to_reviewer = {}
    
    # Audit existing assignments
    for pr in prs:
        reviewers_from_team = [r for r in pr.get('requested_reviewers', []) if r in team]
        if reviewers_from_team:
            for r in reviewers_from_team:
                workload[r] += 1
            issue_ids = extract_issue_ids(pr.get('title', ''), pr.get('body', ''))
            for issue_id in issue_ids:
                if issue_id not in tracking_issue_to_reviewer:
                    tracking_issue_to_reviewer[issue_id] = reviewers_from_team[0]

    print("Current team workload:")
    for member, count in sorted(workload.items()):
        print(f"  {member}: {count}")

    # Step 2: Fetch Unassigned Candidate PRs
    candidate_prs = []
    for pr in prs:
        labels = pr.get('labels', [])
        if "ready-for-human" in labels:
            reviewers_from_team = [r for r in pr.get('requested_reviewers', []) if r in team]
            if not reviewers_from_team:
                candidate_prs.append(pr)
                
    # Sort candidate PRs by number ascending (oldest first)
    candidate_prs.sort(key=lambda x: x['number'])
    
    print(f"\nFound {len(candidate_prs)} unassigned 'ready-for-human' candidate PRs.")

    # Step 3: Assignment Algorithm
    assignments = []
    for pr in candidate_prs:
        pr_number = pr['number']
        issue_ids = extract_issue_ids(pr.get('title', ''), pr.get('body', ''))
        
        selected_reviewer = None
        
        # Priority 1: Workflow Affinity
        affinity_reviewers = []
        for issue_id in issue_ids:
            if issue_id in tracking_issue_to_reviewer:
                rev = tracking_issue_to_reviewer[issue_id]
                if workload[rev] < 10:
                    affinity_reviewers.append(rev)
        
        if affinity_reviewers:
            # Sort by workload first, then alphabetically for deterministic tie-breaker
            affinity_reviewers.sort(key=lambda r: (workload[r], r))
            selected_reviewer = affinity_reviewers[0]
            print(f"PR #{pr_number} matched affinity reviewer {selected_reviewer} (workflow affinity with issue(s) {issue_ids})")
            
        # Priority 2: Underloaded Balancing (C_user < 5)
        if not selected_reviewer:
            underloaded = [member for member, count in workload.items() if count < 5]
            if underloaded:
                underloaded.sort(key=lambda r: (workload[r], r))
                selected_reviewer = underloaded[0]
                print(f"PR #{pr_number} assigned to underloaded reviewer {selected_reviewer} (workload {workload[selected_reviewer]} < 5)")
                
        # Priority 3: Capacity Absorption (5 <= C_user < 10)
        if not selected_reviewer:
            assignable = [member for member, count in workload.items() if count < 10]
            if assignable:
                assignable.sort(key=lambda r: (workload[r], r))
                selected_reviewer = assignable[0]
                print(f"PR #{pr_number} assigned to reviewer {selected_reviewer} (capacity absorption, workload {workload[selected_reviewer]} < 10)")
                
        # Ceiling Reached
        if not selected_reviewer:
            print(f"PR #{pr_number} could not be assigned: all team members have reached their hard ceiling of 10 open reviews.")
            # Check termination condition: terminate if everyone is at ceiling
            all_at_ceiling = all(workload[m] >= 10 for m in team)
            if all_at_ceiling:
                print("All team members have reached the hard ceiling of 10. Terminating assignment algorithm.")
                break
            continue
            
        # Update State & Queue Assignment
        workload[selected_reviewer] += 1
        for issue_id in issue_ids:
            tracking_issue_to_reviewer[issue_id] = selected_reviewer
            
        assignments.append((pr_number, selected_reviewer))

    # Step 4: Execute Assignments
    if assignments:
        print("\nExecuting assignments:")
        for pr_number, reviewer in assignments:
            if not dry_run:
                print(f"Assigning PR #{pr_number} to {reviewer}...")
                cmd = ["gh", "pr", "edit", str(pr_number), "--repo", "GoogleCloudPlatform/k8s-config-connector", "--add-reviewer", reviewer]
                try:
                    subprocess.run(cmd, check=True, capture_output=True, text=True)
                    print(f"Successfully assigned PR #{pr_number} to {reviewer}.")
                except subprocess.CalledProcessError as e:
                    print(f"Error assigning PR #{pr_number} to {reviewer}: {e.stderr}", file=sys.stderr)
            else:
                print(f"[DRY RUN] Would assign PR #{pr_number} to {reviewer}.")
    else:
        print("\nNo new assignments made.")
            
    print("\nFinal team workload:")
    for member, count in sorted(workload.items()):
        print(f"  {member}: {count}")

def main():
    parser = argparse.ArgumentParser(description="PR Review Workload Balancer")
    parser.add_argument("--dry-run", action="store_true", help="Do not execute assignments")
    parser.add_argument("--prs-file", type=str, help="Read open PRs from a JSON lines file instead of fetching from GitHub API")
    args = parser.parse_args()

    if args.prs_file:
        prs = []
        with open(args.prs_file, 'r') as f:
            for line in f:
                if line.strip():
                    prs.append(json.loads(line))
    else:
        prs = fetch_open_prs()

    balance_reviews(prs, TEAM, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
