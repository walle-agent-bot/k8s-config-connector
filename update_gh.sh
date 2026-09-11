#!/bin/bash
ISSUE_ID=10101

# Try to edit issue description first
if gh issue edit $ISSUE_ID --body "$(cat comment_body.txt)"; then
    echo "Issue description updated successfully."
else
    echo "Failed to edit issue description. Trying to update comment."
    URL=$(gh issue view $ISSUE_ID --json comments --jq '.comments[] | select(.body | contains("Migration Progress")) | .url' | tail -n 1)
    if [ -n "$URL" ]; then
        COMMENT_ID=$(echo $URL | awk -F'issuecomment-' '{print $2}')
        gh api --method PATCH repos/GoogleCloudPlatform/k8s-config-connector/issues/comments/$COMMENT_ID -f body="$(cat comment_body.txt)"
        echo "Comment updated."
    else
        gh issue comment create $ISSUE_ID --body "$(cat comment_body.txt)"
        echo "Comment created."
    fi
fi
