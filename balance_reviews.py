import sys
import re
import json
import subprocess

TEAM = ["acpana", "anfernee", "anhdle-sso", "barney-s", "gemmahou", "maqiuyujoyce"]
REPO = "GoogleCloudPlatform/k8s-config-connector"

def run_command(args):
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command {' '.join(args)}: {result.stderr}", file=sys.stderr)
        return None
    return result.stdout

def fetch_open_prs():
    print("Fetching open PRs from REST API...")
    open_prs = []
    page = 1
    while True:
        url = f"repos/{REPO}/pulls?state=open&per_page=100&page={page}"
        stdout = run_command(["gh", "api", url])
        if not stdout:
            break
        try:
            prs = json.loads(stdout)
        except Exception as e:
            print(f"Failed to parse JSON on page {page}: {e}")
            break
        if not prs:
            break
        open_prs.extend(prs)
        if len(prs) < 100:
            break
        page += 1
    print(f"Fetched {len(open_prs)} open PRs.")
    return open_prs

def main():
    open_prs = fetch_open_prs()
    
    # 1. Audit current workloads and multilevel workflow mapping
    workload = {member: 0 for member in TEAM}
    tracking_issue_to_reviewer = {}
    
    # Track which PR numbers each reviewer is on
    reviewer_to_prs = {member: [] for member in TEAM}
    
    for pr in open_prs:
        number = pr["number"]
        title = pr.get("title") or ""
        body = pr.get("body") or ""
        
        # Extract requested reviewers
        reviewers = [r["login"] for r in pr.get("requested_reviewers", [])]
        
        # Count team workloads
        for r in reviewers:
            if r in workload:
                workload[r] += 1
                reviewer_to_prs[r].append(number)
                
        # Find all issue IDs referenced in title/body
        issue_ids = re.findall(r'#(\d+)', title) + re.findall(r'#(\d+)', body)
        issue_ids = list(set(issue_ids))
        
        # Populate workflow affinity map
        for r in reviewers:
            if r in TEAM:
                for issue_id in issue_ids:
                    tracking_issue_to_reviewer[issue_id] = r

    print("\nCurrent workloads:")
    for member in TEAM:
        print(f"  {member}: {workload[member]} open assigned PRs (PRs: {reviewer_to_prs[member]})")
        
    print(f"\nWorkflow affinity mapping has {len(tracking_issue_to_reviewer)} entries.")
    
    # 2. Filter candidate PRs (open PRs labeled "ready-for-human" and unassigned to team)
    candidates = []
    for pr in open_prs:
        labels = [l["name"] for l in pr.get("labels", [])]
        if "ready-for-human" not in labels:
            continue
            
        reviewers = [r["login"] for r in pr.get("requested_reviewers", [])]
        has_team_reviewer = any(r in workload for r in reviewers)
        if has_team_reviewer:
            continue
            
        candidates.append(pr)
        
    # Sort candidate PRs by number ascending (oldest first)
    candidates.sort(key=lambda x: x["number"])
    
    print(f"\nFound {len(candidates)} unassigned candidate 'ready-for-human' PRs:")
    for c in candidates:
        print(f"  PR #{c['number']}: {c['title']}")
        
    # 3. Assignment Algorithm
    queued_assignments = []
    for pr in candidates:
        number = pr["number"]
        title = pr.get("title") or ""
        body = pr.get("body") or ""
        
        # Extract issue IDs
        issue_ids = re.findall(r'#(\d+)', title) + re.findall(r'#(\d+)', body)
        issue_ids = list(set(issue_ids))
        
        selected_reviewer = None
        priority_reason = ""
        
        # Priority 1: Workflow Affinity
        for issue_id in issue_ids:
            if issue_id in tracking_issue_to_reviewer:
                reviewer = tracking_issue_to_reviewer[issue_id]
                if workload[reviewer] < 10:
                    selected_reviewer = reviewer
                    priority_reason = f"Workflow Affinity (referenced issue #{issue_id} reviewed by {reviewer})"
                    break
                    
        # Priority 2: Underloaded Balancing (< 5)
        if not selected_reviewer:
            underloaded = [m for m in TEAM if workload[m] < 5]
            if underloaded:
                # Select the one with the lowest workload, breaking ties stably
                underloaded.sort(key=lambda m: (workload[m], TEAM.index(m)))
                selected_reviewer = underloaded[0]
                priority_reason = f"Underloaded Balancing (workload={workload[selected_reviewer]} < 5)"
                
        # Priority 3: Capacity Absorption (5 <= workload < 10)
        if not selected_reviewer:
            available = [m for m in TEAM if workload[m] < 10]
            if available:
                available.sort(key=lambda m: (workload[m], TEAM.index(m)))
                selected_reviewer = available[0]
                priority_reason = f"Capacity Absorption (workload={workload[selected_reviewer]} < 10)"
                
        if selected_reviewer:
            # Update state
            workload[selected_reviewer] += 1
            for issue_id in issue_ids:
                tracking_issue_to_reviewer[issue_id] = selected_reviewer
            queued_assignments.append((number, selected_reviewer, priority_reason))
            print(f"Assigned PR #{number} to {selected_reviewer} via {priority_reason}")
        else:
            print(f"Could not assign PR #{number} (all team members are at maximum workload 10)")
            
    # 4. Execute Assignments
    print("\nExecuting Assignments:")
    if not queued_assignments:
        print("No new assignments to make.")
    else:
        for pr_number, reviewer, reason in queued_assignments:
            print(f"Executing: Add reviewer '{reviewer}' to PR #{pr_number}")
            edit_cmd = [
                "gh", "pr", "edit", str(pr_number),
                "--repo", REPO,
                "--add-reviewer", reviewer
            ]
            stdout = run_command(edit_cmd)
            if stdout is not None:
                print(f"Successfully assigned PR #{pr_number} to {reviewer}")
            else:
                print(f"Failed to assign PR #{pr_number} to {reviewer}")

if __name__ == "__main__":
    main()
