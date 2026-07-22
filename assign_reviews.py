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

import subprocess
import json
import re
import sys

# Team Definition
TEAM = ["acpana", "anfernee", "anhdle-sso", "barney-s", "gemmahou", "maqiuyujoyce"]

def fetch_open_prs():
    """Fetches all open pull requests from the repository using the GitHub API."""
    prs = []
    page = 1
    while True:
        print(f"Fetching page {page} of open PRs...", flush=True)
        cmd = ["gh", "api", f"repos/GoogleCloudPlatform/k8s-config-connector/pulls?state=open&per_page=100&page={page}"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error fetching page {page}: {result.stderr}", file=sys.stderr)
            break
        
        page_prs = json.loads(result.stdout)
        if not page_prs:
            break
        
        prs.extend(page_prs)
        if len(page_prs) < 100:
            break
        page += 1
    return prs

def select_reviewer(candidate, workload, tracking_issue_to_reviewer):
    """
    Applies the prioritized selection algorithm to find the best reviewer for a PR.
    """
    # Priority 1: Workflow Affinity (Soft Rule)
    # If any issue ID referenced in the candidate matches a key in tracking_issue_to_reviewer,
    # and that reviewer's count < 10, select them.
    affinity_reviewers = []
    for issue in candidate["issues"]:
        rev = tracking_issue_to_reviewer.get(issue)
        if rev and workload[rev] < 10:
            affinity_reviewers.append(rev)
            
    if affinity_reviewers:
        # Pick the one with the lowest workload, breaking ties alphabetically
        affinity_reviewers = sorted(affinity_reviewers, key=lambda r: (workload[r], r))
        return affinity_reviewers[0], "Priority 1 (Workflow Affinity)"
        
    # Priority 2: Underloaded Balancing (C_user < 5)
    underloaded = [m for m in TEAM if workload[m] < 5]
    if underloaded:
        # Select the member with the lowest C_user (breaking ties alphabetically)
        underloaded = sorted(underloaded, key=lambda r: (workload[r], r))
        return underloaded[0], "Priority 2 (Underloaded Balancing)"
        
    # Priority 3: Capacity Absorption (5 <= C_user < 10)
    absorbers = [m for m in TEAM if 5 <= workload[m] < 10]
    if absorbers:
        # Select the member with the lowest C_user (breaking ties alphabetically)
        absorbers = sorted(absorbers, key=lambda r: (workload[r], r))
        return absorbers[0], "Priority 3 (Capacity Absorption)"
        
    # Ceiling Reached: All team members have C_user >= 10
    return None, "Ceiling Reached (All members at >= 10)"

def main():
    print("=== Config Connector PR Review Workload Balancer ===", flush=True)
    
    prs = fetch_open_prs()
    print(f"Total open PRs fetched: {len(prs)}\n", flush=True)
    
    # Audit current workloads and workflow mappings
    workload = {member: 0 for member in TEAM}
    tracking_issue_to_reviewer = {}
    candidates = []
    
    # Regex for matching issue IDs (#12345)
    issue_pattern = re.compile(r'#(\d+)')
    
    for pr in prs:
        number = pr.get("number")
        title = pr.get("title", "")
        body = pr.get("body") or ""
        labels = [l.get("name") for l in pr.get("labels", [])]
        reviewers = [r.get("login") for r in pr.get("requested_reviewers", [])]
        
        # Identify if any team member is a requested reviewer
        team_reviewers_on_pr = [r for r in reviewers if r in workload]
        
        for r in team_reviewers_on_pr:
            workload[r] += 1
            
        # Extract issues from title and body
        issues = set(issue_pattern.findall(title + " " + body))
        
        # If there are team reviewers already assigned, map the referenced issues to them
        if team_reviewers_on_pr:
            for r in team_reviewers_on_pr:
                for issue in issues:
                    tracking_issue_to_reviewer[issue] = r
                    
        # Check if the PR is a candidate: has label "ready-for-human" and is not already assigned to any team member
        if "ready-for-human" in labels:
            if not team_reviewers_on_pr:
                candidates.append({
                    "number": number,
                    "title": title,
                    "body": body,
                    "issues": list(issues)
                })
                
    print("Initial Reviewer Workloads:")
    for member, count in workload.items():
        status = "UNDERLOADED" if count < 5 else ("ABSORBING" if count < 10 else "AT CEILING")
        print(f"  {member}: {count} open reviews ({status})", flush=True)
        
    print(f"\nUnassigned 'ready-for-human' candidates found: {len(candidates)}", flush=True)
    
    # Sort candidates by number (oldest first) for deterministic behavior
    candidates = sorted(candidates, key=lambda c: c["number"])
    
    assignments_to_make = []
    
    for candidate in candidates:
        reviewer, reason = select_reviewer(candidate, workload, tracking_issue_to_reviewer)
        if reviewer:
            assignments_to_make.append({
                "pr_number": candidate["number"],
                "title": candidate["title"],
                "reviewer": reviewer,
                "reason": reason
            })
            # Update local state immediately
            workload[reviewer] += 1
            for issue in candidate["issues"]:
                tracking_issue_to_reviewer[issue] = reviewer
        else:
            print(f"  Cannot assign PR #{candidate['number']}: {reason}", flush=True)
            
    # Execute Assignments
    if assignments_to_make:
        print("\nExecuting Assignments:", flush=True)
        for assignment in assignments_to_make:
            pr_num = assignment["pr_number"]
            reviewer = assignment["reviewer"]
            reason = assignment["reason"]
            title = assignment["title"]
            
            print(f"  Assigning PR #{pr_num} to {reviewer} via {reason}: {title}", flush=True)
            cmd = [
                "gh", "pr", "edit", str(pr_num),
                "--repo", "GoogleCloudPlatform/k8s-config-connector",
                "--add-reviewer", reviewer
            ]
            print(f"    Running: {' '.join(cmd)}", flush=True)
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"    Successfully assigned #{pr_num} to {reviewer}.", flush=True)
            else:
                print(f"    FAILED to assign #{pr_num}: {res.stderr}", file=sys.stderr, flush=True)
                
        print("\nFinal Reviewer Workloads after balancing:")
        for member, count in workload.items():
            print(f"  {member}: {count}", flush=True)
    else:
        print("\nNo assignments needed at this time.", flush=True)

if __name__ == "__main__":
    main()
