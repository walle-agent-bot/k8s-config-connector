#!/usr/bin/env python3
import json
import re
import subprocess
import sys

TEAM = ["acpana", "anfernee", "anhdle-sso", "barney-s", "gemmahou", "maqiuyujoyce"]

def fetch_open_prs():
    page = 1
    all_prs = []
    print("Fetching open Pull Requests from GoogleCloudPlatform/k8s-config-connector...")
    while True:
        cmd = ["gh", "api", f"repos/GoogleCloudPlatform/k8s-config-connector/pulls?state=open&per_page=100&page={page}"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error fetching page {page}: {result.stderr}", file=sys.stderr)
            break
        try:
            prs = json.loads(result.stdout)
        except Exception as e:
            print(f"Error parsing JSON from page {page}: {e}", file=sys.stderr)
            break
        if not prs or not isinstance(prs, list):
            break
        all_prs.extend(prs)
        if len(prs) < 100:
            break
        page += 1
    return all_prs

def select_reviewer(candidate, workload, tracking_issue_to_reviewer):
    # Priority 1: Workflow Affinity
    for issue_id in candidate["issue_refs"]:
        if issue_id in tracking_issue_to_reviewer:
            reviewer = tracking_issue_to_reviewer[issue_id]
            if workload[reviewer] < 10:
                return reviewer, "Workflow Affinity (Issue #{})".format(issue_id)
                
    # Priority 2: Underloaded Balancing (C_user < 5)
    underloaded = [m for m in TEAM if workload[m] < 5]
    if underloaded:
        # Select the member with lowest C_user, tie-break alphabetically
        underloaded.sort(key=lambda m: (workload[m], m))
        return underloaded[0], "Underloaded Balancing (C_user = {})".format(workload[underloaded[0]])
        
    # Priority 3: Capacity Absorption (5 <= C_user < 10)
    absorbers = [m for m in TEAM if workload[m] < 10]
    if absorbers:
        # Select the member with lowest C_user, tie-break alphabetically
        absorbers.sort(key=lambda m: (workload[m], m))
        return absorbers[0], "Capacity Absorption (C_user = {})".format(workload[absorbers[0]])
        
    # Ceiling reached: All members have workload >= 10
    return None, "Ceiling Reached"

def main():
    prs = fetch_open_prs()
    print(f"\nSuccessfully fetched {len(prs)} open PRs.\n")
    
    workload = {member: 0 for member in TEAM}
    tracking_issue_to_reviewer = {}
    candidates = []
    
    for pr in prs:
        requested_reviewers = [r["login"] for r in pr.get("requested_reviewers", [])]
        team_reviewers = [r for r in requested_reviewers if r in TEAM]
        
        # Check if this PR has 'ready-for-human' label
        labels = [l["name"] for l in pr.get("labels", [])]
        has_ready_label = "ready-for-human" in labels
        
        # Extract all issue references from title and body
        body = pr.get("body") or ""
        title = pr.get("title") or ""
        issue_refs = [int(num) for num in re.findall(r'#(\d+)', f"{title}\n{body}")]
        issue_refs = list(set(issue_refs))
        
        if team_reviewers:
            # Increment workload for each reviewer from TEAM requested on this PR
            for r in team_reviewers:
                workload[r] += 1
                # Map tracking issues to this reviewer
                for issue_id in issue_refs:
                    tracking_issue_to_reviewer[issue_id] = r
        else:
            # If no team member is currently requested, and it has the ready-for-human label, it's a candidate
            if has_ready_label:
                candidates.append({
                    "number": pr["number"],
                    "title": title,
                    "body": body,
                    "issue_refs": issue_refs
                })
                
    # Sort candidates by number ascending (oldest first)
    candidates.sort(key=lambda c: c["number"])
    
    print("=== Current Team Workloads ===")
    for member, count in sorted(workload.items()):
        print(f"  {member}: {count} open reviews")
    
    print(f"\nFound {len(candidates)} unassigned 'ready-for-human' candidate PRs.")
    
    assignments = []
    for cand in candidates:
        reviewer_info = select_reviewer(cand, workload, tracking_issue_to_reviewer)
        if reviewer_info[0] is None:
            print(f"No reviewer could be selected for PR #{cand['number']} (Ceiling reached for all team members).")
            break
        selected_user, reason = reviewer_info
        workload[selected_user] += 1
        for issue_id in cand["issue_refs"]:
            tracking_issue_to_reviewer[issue_id] = selected_user
            
        assignments.append({
            "pr_number": cand["number"],
            "title": cand["title"],
            "reviewer": selected_user,
            "reason": reason
        })
        
    if not assignments:
        print("\nNo new assignments to perform.")
        print("Note: Team members are exempted from having 5 assigned PRs as the pool of unassigned 'ready-for-human' PRs is empty.")
    else:
        print("\n=== Executing Assignments ===")
        for assign in assignments:
            print(f"Assigning PR #{assign['pr_number']} -> {assign['reviewer']} ({assign['reason']})")
            # Run gh pr edit to add the reviewer
            cmd = [
                "gh", "pr", "edit", str(assign['pr_number']),
                "--repo", "GoogleCloudPlatform/k8s-config-connector",
                "--add-reviewer", assign['reviewer']
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0:
                print(f"  Error assigning PR #{assign['pr_number']}: {res.stderr.strip()}", file=sys.stderr)
            else:
                print(f"  Successfully assigned PR #{assign['pr_number']} to {assign['reviewer']}.")
        
        print("\n=== Updated Team Workloads ===")
        for member, count in sorted(workload.items()):
            print(f"  {member}: {count} open reviews")

if __name__ == "__main__":
    main()
