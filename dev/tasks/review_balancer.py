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

TEAM_MEMBERS = ['acpana', 'anfernee', 'anhdle-sso', 'barney-s', 'gemmahou', 'maqiuyujoyce']

def main():
    print("Fetching open Pull Requests from GitHub REST API...")
    cmd = [
        "gh", "api", "-X", "GET",
        "repos/GoogleCloudPlatform/k8s-config-connector/pulls?state=open&per_page=100",
        "--paginate", "--slurp"
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"Error calling GitHub API: {res.stderr}", file=sys.stderr)
        sys.exit(1)

    try:
        pages = json.loads(res.stdout)
    except Exception as e:
        print(f"Error parsing JSON output: {e}\nRaw output length: {len(res.stdout)}", file=sys.stderr)
        sys.exit(1)

    # Flatten paginated results
    all_prs = []
    for page in pages:
        if isinstance(page, list):
            all_prs.extend(page)
        elif isinstance(page, dict):
            # Fallback if somehow it's a single page (not slurp-nested)
            all_prs.append(page)

    print(f"Retrieved {len(all_prs)} open Pull Requests.")

    # Step 1: Audit Current Team Workloads & Multilevel Workflow Mapping
    workload = {member: 0 for member in TEAM_MEMBERS}
    tracking_issue_to_reviewer = {}

    for pr in all_prs:
        title = pr.get("title") or ""
        body = pr.get("body") or ""
        requested_reviewers = pr.get("requested_reviewers") or []
        
        assigned_team_members = []
        for rev in requested_reviewers:
            login = rev.get("login")
            if login in TEAM_MEMBERS:
                assigned_team_members.append(login)
                workload[login] += 1

        # Extract issue IDs matching `#<NUMBER>`
        issue_ids = set(re.findall(r'#(\d+)', title + " " + body))
        
        # If the PR is already requested of a team reviewer, map the issue IDs to them
        if assigned_team_members:
            for issue_id in issue_ids:
                # Map to the first assigned team member
                tracking_issue_to_reviewer[issue_id] = assigned_team_members[0]

    print("\nCurrent Team Workloads:")
    for member, count in sorted(workload.items()):
        print(f"  - {member}: {count} open assigned review(s)")

    # Step 2: Fetch Unassigned Candidate PRs Labeled "ready-for-human"
    candidate_prs = []
    for pr in all_prs:
        requested_reviewers = pr.get("requested_reviewers") or []
        assigned_team_reviewers = [rev.get("login") for rev in requested_reviewers if rev.get("login") in TEAM_MEMBERS]
        
        if assigned_team_reviewers:
            continue  # Already assigned to a team member

        # Check for label "ready-for-human"
        labels = [l.get("name") for l in pr.get("labels", []) if isinstance(l, dict)]
        if "ready-for-human" in labels:
            candidate_prs.append(pr)

    # Sort candidates by PR number ascending (oldest first)
    candidate_prs.sort(key=lambda pr: pr.get("number", 0))

    print(f"\nFound {len(candidate_prs)} unassigned PR(s) labeled 'ready-for-human'.")

    if not candidate_prs:
        print("No eligible candidate PRs to assign. Exiting.")
        sys.exit(0)

    # Step 3: Assignment Algorithm
    queued_assignments = []
    
    for pr in candidate_prs:
        pr_number = pr.get("number")
        pr_title = pr.get("title")
        pr_body = pr.get("body") or ""
        
        # Extract all referenced issues
        issue_ids = set(re.findall(r'#(\d+)', pr_title + " " + pr_body))
        
        selected_reviewer = None
        reason = ""
        
        # Priority 1: Workflow Affinity
        for issue_id in sorted(issue_ids, key=int):
            if issue_id in tracking_issue_to_reviewer:
                rev = tracking_issue_to_reviewer[issue_id]
                if workload[rev] < 10:
                    selected_reviewer = rev
                    reason = f"Priority 1 (Workflow Affinity via issue #{issue_id})"
                    break
                    
        # Priority 2: Underloaded Balancing (C_user < 5)
        if not selected_reviewer:
            underloaded = [m for m in TEAM_MEMBERS if workload[m] < 5]
            if underloaded:
                underloaded.sort(key=lambda m: (workload[m], m))
                selected_reviewer = underloaded[0]
                reason = "Priority 2 (Underloaded Balancing)"
                
        # Priority 3: Capacity Absorption (5 <= C_user < 10)
        if not selected_reviewer:
            absorbers = [m for m in TEAM_MEMBERS if 5 <= workload[m] < 10]
            if absorbers:
                absorbers.sort(key=lambda m: (workload[m], m))
                selected_reviewer = absorbers[0]
                reason = "Priority 3 (Capacity Absorption)"
                
        if selected_reviewer:
            # Update state
            workload[selected_reviewer] += 1
            for issue_id in issue_ids:
                tracking_issue_to_reviewer[issue_id] = selected_reviewer
                
            queued_assignments.append((pr_number, pr_title, selected_reviewer, reason))
        else:
            print(f"Skipping PR #{pr_number} - Hard ceiling (10 reviews) reached for all team members.")

    # Step 4: Execute Assignments & Exit
    if not queued_assignments:
        print("\nNo assignments queued. Exiting.")
        sys.exit(0)

    print("\nExecuting assignments:")
    for pr_number, title, reviewer, reason in queued_assignments:
        print(f"  Assigning PR #{pr_number} to {reviewer} ({reason})")
        print(f"    Title: {title}")
        
        # Call gh pr edit to add reviewer
        assign_cmd = [
            "gh", "pr", "edit", str(pr_number),
            "--repo", "GoogleCloudPlatform/k8s-config-connector",
            "--add-reviewer", reviewer
        ]
        res = subprocess.run(assign_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print(f"    Failed to assign PR #{pr_number} to {reviewer}: {res.stderr}", file=sys.stderr)
        else:
            print(f"    Successfully assigned PR #{pr_number} to {reviewer}.")

    print("\nSummary of Final Workloads:")
    for member, count in sorted(workload.items()):
        print(f"  - {member}: {count} open assigned review(s)")

if __name__ == "__main__":
    main()
