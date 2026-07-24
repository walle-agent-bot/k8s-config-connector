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

TEAM = ["acpana", "anfernee", "anhdle-sso", "barney-s", "gemmahou", "maqiuyujoyce"]

def parse_concatenated_json(text):
    text = text.strip()
    decoder = json.JSONDecoder()
    index = 0
    results = []
    while index < len(text):
        while index < len(text) and text[index].isspace():
            index += 1
        if index >= len(text):
            break
        try:
            obj, size = decoder.raw_decode(text[index:])
            results.append(obj)
            index += size
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON at index {index}: {e}", file=sys.stderr)
            break
    return results

def get_open_prs():
    print("Fetching all open PRs from GoogleCloudPlatform/k8s-config-connector...", flush=True)
    cmd = [
        "gh", "api",
        "repos/GoogleCloudPlatform/k8s-config-connector/pulls?state=open&per_page=100",
        "--paginate"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    pages = parse_concatenated_json(res.stdout)
    prs = []
    for page in pages:
        if isinstance(page, list):
            prs.extend(page)
        else:
            prs.append(page)
    return prs

def select_reviewer(candidate_issues, workload, tracking_issue_to_reviewer):
    # Priority 1 (Workflow Affinity)
    for issue_id in candidate_issues:
        reviewer = tracking_issue_to_reviewer.get(issue_id)
        if reviewer and workload[reviewer] < 10:
            return reviewer, f"Workflow Affinity (matches issue #{issue_id} reviewed by {reviewer})"

    # Priority 2 (Underloaded Balancing, C_user < 5)
    underloaded = [m for m in TEAM if workload[m] < 5]
    if underloaded:
        selected_user = min(underloaded, key=lambda m: workload[m])
        return selected_user, f"Underloaded Balancing (workload={workload[selected_user]} < 5)"

    # Priority 3 (Capacity Absorption, 5 <= C_user < 10)
    absorb = [m for m in TEAM if 5 <= workload[m] < 10]
    if absorb:
        selected_user = min(absorb, key=lambda m: workload[m])
        return selected_user, f"Capacity Absorption (workload={workload[selected_user]} < 10)"

    return None, "Ceiling Reached"

def main():
    try:
        prs = get_open_prs()
    except Exception as e:
        print(f"Error fetching open PRs from GitHub: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Total open PRs fetched: {len(prs)}")

    # Step 1: Audit Current Team Workloads & Multilevel Workflow Mapping
    workload = {member: 0 for member in TEAM}
    tracking_issue_to_reviewer = {}

    for pr in prs:
        title = pr.get("title", "")
        body = pr.get("body", "") or ""
        reviewers = [r.get("login") for r in pr.get("requested_reviewers", []) if r]

        team_reviewers = [r for r in reviewers if r in TEAM]
        for r in team_reviewers:
            workload[r] += 1
            issues = re.findall(r'#(\d+)', f"{title} {body}")
            for issue_id in issues:
                tracking_issue_to_reviewer[issue_id] = r

    print("\nCurrent Team Workloads:")
    for member in TEAM:
        print(f"  - {member}: {workload[member]} open PR reviews")

    # Step 2: Fetch Unassigned Candidate PRs
    candidates = []
    for pr in prs:
        labels = [l.get("name") for l in pr.get("labels", []) if l]
        reviewers = [r.get("login") for r in pr.get("requested_reviewers", []) if r]
        team_reviewers = [r for r in reviewers if r in TEAM]

        if "ready-for-human" in labels and len(team_reviewers) == 0:
            candidates.append(pr)

    print(f"\nFound {len(candidates)} unassigned candidate PR(s) labeled 'ready-for-human'")

    # Step 3: Assignment Algorithm
    assignments = []

    for pr in candidates:
        num = pr.get("number")
        title = pr.get("title", "")
        body = pr.get("body", "") or ""
        
        issues = re.findall(r'#(\d+)', f"{title} {body}")
        selected_user, reason = select_reviewer(issues, workload, tracking_issue_to_reviewer)

        if selected_user:
            workload[selected_user] += 1
            for issue_id in issues:
                tracking_issue_to_reviewer[issue_id] = selected_user
            assignments.append((num, selected_user, reason))
        else:
            print(f"  - PR #{num}: Skipping assignment, all team members are at maximum workload capacity of 10.")

    # Step 4: Execute Assignments & Exit
    if assignments:
        print("\nExecuting queued assignments...")
        for num, reviewer, reason in assignments:
            print(f"  - Assigning PR #{num} to {reviewer} due to: {reason}")
            edit_cmd = [
                "gh", "pr", "edit", str(num),
                "--repo", "GoogleCloudPlatform/k8s-config-connector",
                "--add-reviewer", reviewer
            ]
            res = subprocess.run(edit_cmd, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"    Successfully assigned reviewer {reviewer} to PR #{num}.")
            else:
                print(f"    Failed to assign reviewer to PR #{num}. Error: {res.stderr.strip()}", file=sys.stderr)
    else:
        print("\nNo assignments queued.")

    print("\nFinal Projected Team Workloads:")
    for member in TEAM:
        print(f"  - {member}: {workload[member]} open PR reviews")

if __name__ == "__main__":
    main()
