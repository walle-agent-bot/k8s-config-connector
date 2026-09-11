import sys

with open('.agents/workflows/checklist-for-kind/journal/BillingBudgetsBudget.md', 'r') as f:
    lines = f.readlines()

table_lines = []
in_table = False
status_lines = []
in_status = False

for line in lines:
    if line.startswith("| Step"):
        in_table = True
    
    if in_table:
        if line.startswith("|"):
            table_lines.append(line)
        elif line.strip() == "":
            in_table = False
            
    if line.strip() == "## Status Updates":
        in_status = True
        continue
        
    if in_status:
        if line.startswith("*"):
            status_lines.append(line)

recent_status = status_lines[:3]

body = "## Migration Progress for BillingBudgetsBudget\n\n**Current Step:** Step 4: Ensure MockGCP matches real gcp behavior & Step 6: Validate Direct Promotion\n\n### Progress Tracking\n\n"
body += "".join(table_lines)
body += "\n### Status Updates\n"
body += "".join(recent_status)

with open('comment_body.txt', 'w') as f:
    f.write(body)

print("Body prepared.")
