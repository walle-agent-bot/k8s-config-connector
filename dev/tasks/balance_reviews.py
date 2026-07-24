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

# Define the team members
TEAM_MEMBERS = [
    "acpana",
    "anfernee",
    "anhdle-sso",
    "barney-s",
    "gemmahou",
    "maqiuyujoyce"
]

def run_command(cmd):
    """Run a shell command and return stdout. Raises exception on failure."""
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error running command: {cmd}\nStdout: {res.stdout}\nStderr: {res.stderr}", file=sys.stderr)
        res.check_returncode()
    return res.stdout

def main():
    print("Fetching open PRs from GoogleCloudPlatform/k8s-config-connector...")
    # Use the REST API to fetch paginated open PRs with requested reviewers, labels, title, body, and number.
    # We output them as one JSON object per line using --jq so they are extremely easy to read.
    jq_query = '.[] | {number: .number, title: .title, body: .body, requested_reviewers: [.requested_reviewers[].login], labels: [.labels[].name]}'
    cmd = f'gh api --paginate "repos/GoogleCloudPlatform/k8s-config-connector/pulls?state=open&per_page=100" --jq \'{jq_query}\''
    
    stdout = run_command(cmd)
    
    prs = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            prs.append(json.loads(line))
        except Exception as e:
            print(f"Warning: failed to parse JSON line: {line}. Error: {e}", file=sys.stderr)

    print(f"Total open PRs retrieved: {len(prs)}")

    # 1. Audit current team workloads (C_user)
    # Target bounds: min 5, max 10.
    workload = {user: 0 for user in TEAM_MEMBERS}
    for pr in prs:
        for rev in pr.get("requested_reviewers", []):
            if rev in workload:
                workload[rev] += 1

    print("\nCurrent team workloads (active requested reviews):")
    for user, count in workload.items():
        print(f"  {user}: {count}")

    # 2. Build tracking_issue_to_reviewer map
    # Maps issue IDs (from #<NUMBER>) in open PRs currently assigned to a team member
    # to that team member.
    tracking_issue_to_reviewer = {}
    issue_re = re.compile(r'#(\d+)')

    for pr in prs:
        # Find if this PR has any active team member reviewer
        active_reviewers = [rev for rev in pr.get("requested_reviewers", []) if rev in workload]
        if active_reviewers:
            # Extract all issue IDs referenced in PR title and body
            content = f"{pr.get('title', '')}\n{pr.get('body', '') or ''}"
            issue_ids = set(issue_re.findall(content))
            for issue_id in issue_ids:
                # Map to the first reviewer or update
                # Since multiple active reviewers are possible, we map to the first one
                reviewer = active_reviewers[0]
                tracking_issue_to_reviewer[issue_id] = reviewer

    print(f"\nBuilt tracking_issue_to_reviewer mapping for {len(tracking_issue_to_reviewer)} issues.")

    # 3. Filter unassigned candidate PRs
    # Labeled with "ready-for-human" and does NOT have any member of the team in requested_reviewers
    candidates = []
    for pr in prs:
        labels = pr.get("labels", [])
        if "ready-for-human" not in labels:
            continue
        # Check if any team member is already requested
        has_team_reviewer = any(rev in workload for rev in pr.get("requested_reviewers", []))
        if has_team_reviewer:
            continue
        candidates.append(pr)

    print(f"\nFound {len(candidates)} unassigned 'ready-for-human' candidate PRs.")

    assignments_queued = [] # List of tuples: (pr_number, selected_user, reason, title)

    # 4. Assignment Algorithm
    for pr in candidates:
        pr_number = pr["number"]
        title = pr["title"]
        body = pr["body"] or ""
        
        # Check termination condition: Are all team members at the hard ceiling of 10?
        if all(workload[user] >= 10 for user in TEAM_MEMBERS):
            print("Hard ceiling (10 reviews) reached for all team members. Skipping remaining assignments.")
            break

        # Extract issue IDs referenced in this candidate PR
        content = f"{title}\n{body}"
        referenced_issue_ids = set(issue_re.findall(content))

        selected_user = None
        assignment_reason = ""

        # Priority 1: Workflow Affinity
        # If any referenced issue matches tracking_issue_to_reviewer, and that reviewer's count is < 10
        # If multiple match, we can pick the one with the lowest count < 10 (or alphabetical tie-break)
        affinity_users = []
        for issue_id in referenced_issue_ids:
            if issue_id in tracking_issue_to_reviewer:
                rev = tracking_issue_to_reviewer[issue_id]
                if workload[rev] < 10:
                    affinity_users.append(rev)
        
        if affinity_users:
            # Pick affinity user with lowest workload, alphabetical as tie-breaker
            affinity_users = sorted(list(set(affinity_users)), key=lambda u: (workload[u], u))
            selected_user = affinity_users[0]
            assignment_reason = f"Workflow Affinity (referenced issue/s matching review history)"

        # Priority 2: Underloaded Balancing (C_user < 5)
        if not selected_user:
            underloaded_users = [u for u in TEAM_MEMBERS if workload[u] < 5]
            if underloaded_users:
                # Pick member with the lowest workload, tie-break alphabetically
                underloaded_users = sorted(underloaded_users, key=lambda u: (workload[u], u))
                selected_user = underloaded_users[0]
                assignment_reason = f"Underloaded Balancing (workload < 5)"

        # Priority 3: Capacity Absorption (5 <= C_user < 10)
        if not selected_user:
            available_users = [u for u in TEAM_MEMBERS if workload[u] < 10]
            if available_users:
                # Pick member with lowest workload, tie-break alphabetically
                available_users = sorted(available_users, key=lambda u: (workload[u], u))
                selected_user = available_users[0]
                assignment_reason = f"Capacity Absorption (workload < 10)"

        if selected_user:
            # Update state
            workload[selected_user] += 1
            # Add mapping for every issue ID referenced in this PR
            for issue_id in referenced_issue_ids:
                tracking_issue_to_reviewer[issue_id] = selected_user
            
            assignments_queued.append((pr_number, selected_user, assignment_reason, title))
        else:
            print(f"Could not select a reviewer for PR #{pr_number} (all potential reviewers might have hit the limit).")

    # 5. Execute Assignments & Print Summary
    print(f"\n--- Assignments Queue ({len(assignments_queued)} PRs) ---")
    if not assignments_queued:
        print("No new assignments needed or possible.")
        return

    for pr_number, user, reason, title in assignments_queued:
        print(f"Assigning PR #{pr_number} ('{title}') to '{user}' because of {reason}")
        
    print("\nExecuting assignments on GitHub...")
    for pr_number, user, reason, title in assignments_queued:
        cmd = f"gh pr edit {pr_number} --repo GoogleCloudPlatform/k8s-config-connector --add-reviewer {user}"
        print(f"Running: {cmd}")
        run_command(cmd)

    print("\nNew workloads after assignment:")
    for user, count in workload.items():
        print(f"  {user}: {count}")

    print("\nSuccessfully finished PR review workload balancing!")

if __name__ == "__main__":
    main()
