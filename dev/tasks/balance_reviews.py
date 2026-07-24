#!/usr/bin/env python3
# Copyright 2026 Google LLC
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
import subprocess
import json
import re
import sys

TEAM_MEMBERS = ["acpana", "anfernee", "anhdle-sso", "barney-s", "gemmahou", "maqiuyujoyce"]

def fetch_open_prs():
    """Fetches all open PRs with key fields via GitHub REST API."""
    cmd = [
        "gh", "api", "repos/GoogleCloudPlatform/k8s-config-connector/pulls",
        "--paginate",
        "-q", ".[] | {number: .number, title: .title, body: .body, requested_reviewers: [.requested_reviewers[].login], labels: [.labels[].name]}"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    prs = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        try:
            pr = json.loads(line)
            if pr.get("title") is None:
                pr["title"] = ""
            if pr.get("body") is None:
                pr["body"] = ""
            if pr.get("requested_reviewers") is None:
                pr["requested_reviewers"] = []
            if pr.get("labels") is None:
                pr["labels"] = []
            prs.append(pr)
        except Exception as e:
            print(f"Warning: Failed to parse line: {line}\nError: {e}")
    return prs

def extract_issue_ids(title, body):
    """Extracts referenced issue numbers from title and body."""
    text = (title or "") + " " + (body or "")
    matches = re.findall(r'#(\d+)', text)
    return sorted(list(set(matches)))

def run_assignments(prs, execute=False):
    """Main assignment algorithm logic."""
    dry_run = not execute

    # Step 1: Audit Current Team Workloads
    workload = {member: 0 for member in TEAM_MEMBERS}
    assigned_prs_by_member = {member: [] for member in TEAM_MEMBERS}

    for pr in prs:
        for reviewer in pr["requested_reviewers"]:
            if reviewer in TEAM_MEMBERS:
                workload[reviewer] += 1
                assigned_prs_by_member[reviewer].append(pr["number"])

    print("\n--- Current Workloads ---")
    for member in TEAM_MEMBERS:
        print(f"  {member}: {workload[member]} assigned open reviews {assigned_prs_by_member[member]}")

    # Build tracking_issue_to_reviewer map
    tracking_issue_to_reviewer = {}
    for pr in prs:
        assigned_team_reviewers = [r for r in pr["requested_reviewers"] if r in TEAM_MEMBERS]
        if assigned_team_reviewers:
            issue_ids = extract_issue_ids(pr["title"], pr["body"])
            for issue_id in issue_ids:
                tracking_issue_to_reviewer[issue_id] = assigned_team_reviewers[0]

    print(f"\nWorkflow tracking issue maps built: {len(tracking_issue_to_reviewer)} issues mapped to reviewers.")

    # Step 2: Fetch Unassigned Candidate PRs
    candidates = []
    for pr in prs:
        if "ready-for-human" not in pr["labels"]:
            continue
        has_team_reviewer = any(r in TEAM_MEMBERS for r in pr["requested_reviewers"])
        if has_team_reviewer:
            continue
        candidates.append(pr)

    candidates.sort(key=lambda x: x["number"])

    print(f"\n--- Unassigned Candidate PRs (labeled 'ready-for-human'): {len(candidates)} ---")
    for pr in candidates:
        print(f"  #{pr['number']}: \"{pr['title']}\" (labels: {pr['labels']})")

    # Step 3: Assignment Algorithm
    print("\n--- Running Assignment Algorithm ---")
    assignments = []
    initial_workload = workload.copy()

    for pr in candidates:
        if all(workload[m] >= 10 for m in TEAM_MEMBERS):
            print("  [Limit reached] All team members are at or above the hard ceiling of 10. Skipping remaining candidates.")
            break

        issue_ids = extract_issue_ids(pr["title"], pr["body"])
        selected_user = None
        reason = ""

        # Priority 1: Workflow Affinity
        for issue_id in issue_ids:
            reviewer = tracking_issue_to_reviewer.get(issue_id)
            if reviewer and workload[reviewer] < 10:
                selected_user = reviewer
                reason = f"Workflow Affinity with issue #{issue_id} (workload: {workload[selected_user]} -> {workload[selected_user]+1})"
                break

        # Priority 2: Underloaded Balancing (C_user < 5)
        if not selected_user:
            underloaded = [m for m in TEAM_MEMBERS if workload[m] < 5]
            if underloaded:
                underloaded.sort(key=lambda m: (workload[m], m))
                selected_user = underloaded[0]
                reason = f"Underloaded Balancing (workload: {workload[selected_user]} -> {workload[selected_user]+1})"

        # Priority 3: Capacity Absorption (5 <= C_user < 10)
        if not selected_user:
            available = [m for m in TEAM_MEMBERS if workload[m] < 10]
            if available:
                available.sort(key=lambda m: (workload[m], m))
                selected_user = available[0]
                reason = f"Capacity Absorption (workload: {workload[selected_user]} -> {workload[selected_user]+1})"

        if selected_user:
            workload[selected_user] += 1
            for issue_id in issue_ids:
                tracking_issue_to_reviewer[issue_id] = selected_user
            assignments.append((pr["number"], selected_user, reason))
            print(f"  PR #{pr['number']} -> {selected_user} ({reason})")
        else:
            print(f"  PR #{pr['number']} -> UNASSIGNED (No available reviewers under hard ceiling)")

    print("\n--- Workload Changes ---")
    for member in TEAM_MEMBERS:
        print(f"  {member}: {initial_workload[member]} -> {workload[member]} (diff: +{workload[member] - initial_workload[member]})")

    print("\n--- Scheduled Assignments ---")
    if not assignments:
        print("  No assignments to make.")
        return []

    for pr_num, user, reason in assignments:
        action = "DRY-RUN: Would assign" if dry_run else "Executing: Assigning"
        print(f"  {action} PR #{pr_num} to {user}")

    if dry_run:
        print("\n*** This is a DRY-RUN. Run with --execute to apply changes. ***")
    else:
        print("\n--- Executing gh assignments ---")
        for pr_num, user, reason in assignments:
            edit_cmd = [
                "gh", "pr", "edit", str(pr_num),
                "--repo", "GoogleCloudPlatform/k8s-config-connector",
                "--add-reviewer", user
            ]
            print(f"Running: {' '.join(edit_cmd)}")
            res = subprocess.run(edit_cmd, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"  Successfully assigned PR #{pr_num} to {user}")
            else:
                print(f"  Failed to assign PR #{pr_num} to {user}. Error: {res.stderr.strip()}", file=sys.stderr)

    return assignments

def main():
    parser = argparse.ArgumentParser(description="KCC PR Review Workload Balancer")
    parser.add_argument("--execute", action="store_true", help="Actually execute the assignments")
    args = parser.parse_args()

    prs = fetch_open_prs()
    print(f"Total open PRs fetched: {len(prs)}")
    run_assignments(prs, execute=args.execute)

if __name__ == "__main__":
    main()
