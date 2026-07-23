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
import subprocess
import re
import sys

# Team Definition
TEAM_MEMBERS = [
    'acpana',
    'anfernee',
    'anhdle-sso',
    'barney-s',
    'gemmahou',
    'maqiuyujoyce'
]

def run_gh_api(endpoint):
    """Executes a command using the GitHub CLI API."""
    cmd = ["gh", "api", endpoint]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"Error running gh api {endpoint}: {res.stderr}", file=sys.stderr)
        return None
    try:
        return json.loads(res.stdout)
    except Exception as e:
        print(f"Failed to parse JSON response from {endpoint}: {e}", file=sys.stderr)
        return None

def main():
    print("=== Step 1: Audit Current Team Workloads & Multilevel Workflow Mapping ===")
    workload = {member: 0 for member in TEAM_MEMBERS}
    tracking_issue_to_reviewer = {}
    
    # Track which PRs are already being reviewed by which team members
    pr_to_reviewers = {}

    for member in TEAM_MEMBERS:
        # Search for open PRs where this team member is a requested reviewer
        query = f"search/issues?q=repo:GoogleCloudPlatform/k8s-config-connector+is:pr+is:open+review-requested:{member}&per_page=100"
        data = run_gh_api(query)
        if not data or 'items' not in data:
            print(f"Could not fetch reviews for {member}", file=sys.stderr)
            continue
        
        pr_items = data['items']
        workload[member] = len(pr_items)
        print(f"Member '{member}' currently has {len(pr_items)} open review requests.")
        
        for item in pr_items:
            pr_num = item['number']
            if pr_num not in pr_to_reviewers:
                pr_to_reviewers[pr_num] = []
            pr_to_reviewers[pr_num].append(member)
            
            # Extract tracking issues from title and body
            title = item.get('title', '')
            body = item.get('body', '') or ''
            
            # Extract all #<NUMBER> patterns
            issue_ids = re.findall(r'#(\d+)', title + " " + body)
            for issue_id in issue_ids:
                tracking_issue_to_reviewer[int(issue_id)] = member

    print(f"\nInitial workload map: {workload}")

    print("\n=== Step 2: Fetch Unassigned Candidate PRs ===")
    # Query open PRs labeled 'ready-for-human'
    cand_query = "search/issues?q=repo:GoogleCloudPlatform/k8s-config-connector+is:pr+is:open+label:ready-for-human&per_page=100"
    cand_data = run_gh_api(cand_query)
    if not cand_data or 'items' not in cand_data:
        print("Could not fetch candidate PRs", file=sys.stderr)
        sys.exit(1)
        
    all_candidates = cand_data['items']
    print(f"Found {len(all_candidates)} open PRs labeled 'ready-for-human'.")
    
    unassigned_candidates = []
    for cand in all_candidates:
        pr_num = cand['number']
        
        # Check if any team member is already assigned to this PR based on our previous audit
        if pr_num in pr_to_reviewers and len(pr_to_reviewers[pr_num]) > 0:
            print(f"PR #{pr_num} already has team reviewer(s) in active reviews search: {pr_to_reviewers[pr_num]}. Skipping.")
            continue
            
        # Verify requested reviewers of the PR via individual pull API
        pull_details = run_gh_api(f"repos/GoogleCloudPlatform/k8s-config-connector/pulls/{pr_num}")
        if not pull_details:
            print(f"Could not retrieve details for PR #{pr_num}. Skipping.")
            continue
            
        req_reviewers = pull_details.get('requested_reviewers', [])
        req_logins = [r['login'] for r in req_reviewers if 'login' in r]
        
        has_team_reviewer = any(m in req_logins for m in TEAM_MEMBERS)
        if has_team_reviewer:
            print(f"PR #{pr_num} already has team reviewer(s) in pulls API: {req_logins}. Skipping.")
            continue
            
        unassigned_candidates.append(cand)

    print(f"\nUnassigned candidate PRs count: {len(unassigned_candidates)}")
    for c in unassigned_candidates:
        print(f"  - PR #{c['number']}: {c['title']}")

    print("\n=== Step 3: Assignment Algorithm ===")
    queued_assignments = []
    
    for cand in unassigned_candidates:
        pr_num = cand['number']
        title = cand.get('title', '')
        body = cand.get('body', '') or ''
        
        # Extract all issue IDs referenced in title/body
        issue_ids = [int(x) for x in re.findall(r'#(\d+)', title + " " + body)]
        
        selected_user = None
        
        # Priority 1: Workflow Affinity
        for issue_id in issue_ids:
            if issue_id in tracking_issue_to_reviewer:
                reviewer = tracking_issue_to_reviewer[issue_id]
                if workload[reviewer] < 10:
                    selected_user = reviewer
                    print(f"Priority 1 match: PR #{pr_num} references issue #{issue_id} which is reviewed by {reviewer} (current workload: {workload[reviewer]}).")
                    break
        
        # Priority 2: Underloaded Balancing (C_user < 5)
        if not selected_user:
            underloaded = [m for m in TEAM_MEMBERS if workload[m] < 5]
            if underloaded:
                selected_user = min(underloaded, key=lambda m: workload[m])
                print(f"Priority 2 match: Assigning PR #{pr_num} to underloaded member '{selected_user}' (current workload: {workload[selected_user]} < 5).")
        
        # Priority 3: Capacity Absorption (5 <= C_user < 10)
        if not selected_user:
            available = [m for m in TEAM_MEMBERS if workload[m] < 10]
            if available:
                selected_user = min(available, key=lambda m: workload[m])
                print(f"Priority 3 match: Assigning PR #{pr_num} to available member '{selected_user}' (current workload: {workload[selected_user]} < 10).")
                
        if selected_user:
            # Update in-memory state
            workload[selected_user] += 1
            for issue_id in issue_ids:
                tracking_issue_to_reviewer[issue_id] = selected_user
            
            queued_assignments.append((pr_num, selected_user))
        else:
            print(f"PR #{pr_num} could not be assigned (everyone is at the hard ceiling of 10 open reviews).")
            
        if all(workload[m] == 10 for m in TEAM_MEMBERS):
            print("Termination Condition met: Every team member has reached the hard ceiling of 10 assigned open reviews.")
            break

    print("\n=== Step 4: Execute Assignments ===")
    if not queued_assignments:
        print("No new assignments queued.")
    else:
        for pr_num, user in queued_assignments:
            print(f"Assigning {user} to review PR #{pr_num}...")
            cmd = ["gh", "pr", "edit", str(pr_num), "--repo", "GoogleCloudPlatform/k8s-config-connector", "--add-reviewer", user]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if res.returncode != 0:
                print(f"Failed to assign {user} to PR #{pr_num}: {res.stderr}", file=sys.stderr)
            else:
                print(f"Successfully assigned {user} to PR #{pr_num}")

    print("\n=== Final Review Workloads Summary ===")
    for m in TEAM_MEMBERS:
        print(f"  {m:15}: {workload[m]} reviews")

if __name__ == '__main__':
    main()
