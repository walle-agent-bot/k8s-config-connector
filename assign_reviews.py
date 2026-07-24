import subprocess
import json
import re
import sys

TEAM = ['acpana', 'anfernee', 'anhdle-sso', 'barney-s', 'gemmahou', 'maqiuyujoyce']

def fetch_open_prs():
    prs = []
    page = 1
    while True:
        print(f"Fetching page {page} of open PRs from GitHub...")
        cmd = ["gh", "api", f"repos/GoogleCloudPlatform/k8s-config-connector/pulls?state=open&per_page=100&page={page}"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running gh api: {result.stderr}", file=sys.stderr)
            sys.exit(1)
        page_prs = json.loads(result.stdout)
        if not page_prs:
            break
        prs.extend(page_prs)
        if len(page_prs) < 100:
            break
        page += 1
    return prs

def extract_issue_ids(title, body):
    text = f"{title}\n{body or ''}"
    matches = re.findall(r'#(\d+)', text)
    return sorted(list(set(int(m) for m in matches)))

def main():
    print("=== Step 1: Auditing Current Team Workloads & Multilevel Workflow Mapping ===")
    prs = fetch_open_prs()
    print(f"Total open PRs: {len(prs)}")

    # Audit current workload (C_user) based on requested_reviewers
    workload = {member: 0 for member in TEAM}
    for pr in prs:
        for r in pr.get('requested_reviewers', []):
            login = r.get('login')
            if login in workload:
                workload[login] += 1

    print("\nCurrent Team Workloads:")
    for member, count in workload.items():
        print(f"  - {member}: {count} open reviews")

    # Build tracking_issue_to_reviewer map
    tracking_issue_to_reviewer = {}
    for pr in prs:
        reviewers = [r['login'] for r in pr.get('requested_reviewers', []) if r.get('login') in TEAM]
        if reviewers:
            issue_ids = extract_issue_ids(pr.get('title', ''), pr.get('body', ''))
            for issue_id in issue_ids:
                if issue_id not in tracking_issue_to_reviewer:
                    tracking_issue_to_reviewer[issue_id] = reviewers[0]

    print(f"\nMapped {len(tracking_issue_to_reviewer)} tracking issues to existing reviewers.")

    print("\n=== Step 2: Fetching Unassigned Candidate PRs (labeled 'ready-for-human') ===")
    candidates = []
    for pr in prs:
        labels = [l['name'] for l in pr.get('labels', [])]
        if 'ready-for-human' in labels:
            reviewers = [r['login'] for r in pr.get('requested_reviewers', [])]
            has_team_reviewer = any(r in TEAM for r in reviewers)
            if not has_team_reviewer:
                candidates.append(pr)

    print(f"Found {len(candidates)} unassigned 'ready-for-human' candidate PRs:")
    for c in candidates:
        print(f"  - PR #{c['number']}: {c['title']}")

    print("\n=== Step 3: Running Assignment Algorithm ===")
    queued_assignments = []

    for pr in candidates:
        # Check termination condition: every team member has reached hard ceiling of 10
        if all(workload[m] >= 10 for m in TEAM):
            print("Hard ceiling of 10 reviews reached for all team members. Stopping assignments.")
            break

        issue_ids = extract_issue_ids(pr.get('title', ''), pr.get('body', ''))
        
        selected_user = None
        priority_reason = ""

        # Priority 1: Workflow Affinity (matching issue ID and workload < 10)
        for issue_id in issue_ids:
            if issue_id in tracking_issue_to_reviewer:
                rev = tracking_issue_to_reviewer[issue_id]
                if workload[rev] < 10:
                    selected_user = rev
                    priority_reason = f"Workflow Affinity (matching issue #{issue_id})"
                    break

        # Priority 2: Underloaded Balancing (any workload < 5, select lowest)
        if not selected_user:
            underloaded = [m for m in TEAM if workload[m] < 5]
            if underloaded:
                selected_user = min(underloaded, key=lambda m: workload[m])
                priority_reason = f"Underloaded Balancing (lowest workload {workload[selected_user]} < 5)"

        # Priority 3: Capacity Absorption (5 <= workload < 10, select lowest)
        if not selected_user:
            available = [m for m in TEAM if workload[m] < 10]
            if available:
                selected_user = min(available, key=lambda m: workload[m])
                priority_reason = f"Capacity Absorption (lowest workload {workload[selected_user]} < 10)"

        if selected_user:
            # Update state
            workload[selected_user] += 1
            for issue_id in issue_ids:
                tracking_issue_to_reviewer[issue_id] = selected_user
            
            # Queue assignment
            queued_assignments.append({
                'pr_number': pr['number'],
                'pr_title': pr['title'],
                'user': selected_user,
                'reason': priority_reason
            })
            print(f"Queued PR #{pr['number']} -> {selected_user} via {priority_reason}")
        else:
            print(f"Could not assign PR #{pr['number']} (no available reviewer under the hard ceiling).")

    print("\n=== Step 4: Executing Assignments & Printing Summary ===")
    if not queued_assignments:
        print("No new assignments to execute.")
    else:
        for assign in queued_assignments:
            pr_num = assign['pr_number']
            user = assign['user']
            reason = assign['reason']
            print(f"Assigning PR #{pr_num} ('{assign['pr_title']}') to {user} ({reason})...")
            
            # Run the command to edit PR on GitHub
            cmd = [
                "gh", "pr", "edit", str(pr_num),
                "--repo", "GoogleCloudPlatform/k8s-config-connector",
                "--add-reviewer", user
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"  Error assigning PR #{pr_num}: {result.stderr}", file=sys.stderr)
            else:
                print(f"  Successfully assigned PR #{pr_num} to {user}.")

    print("\nFinal Workloads:")
    for member, count in workload.items():
        print(f"  - {member}: {count} open reviews")

if __name__ == "__main__":
    main()
