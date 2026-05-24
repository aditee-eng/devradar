import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

def get_github_activity():
    username = os.getenv("GITHUB_USERNAME")
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"}

    # get activity from last 7 days
    from datetime import timezone
    since = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    # fetch recent events
    url = f"https://api.github.com/users/{username}/events"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code} — {response.json().get('message')}")
        return {}

    events = response.json()

    # count what matters
    commits = 0
    prs_opened = 0
    repos_active = set()

    for event in events:
        # only count events from last 7 days
        event_date = event.get("created_at", "")
        if event_date < since:
            continue

        repo_name = event.get("repo", {}).get("name", "")
        event_type = event.get("type", "")

        if event_type == "PushEvent":
            commits += len(event.get("payload", {}).get("commits", []))
            repos_active.add(repo_name)

        elif event_type == "PullRequestEvent":
            action = event.get("payload", {}).get("action", "")
            if action == "opened":
                prs_opened += 1
                repos_active.add(repo_name)

    return {
        "username": username,
        "commits_this_week": commits,
        "prs_opened": prs_opened,
        "repos_active": list(repos_active),
        "repo_count": len(repos_active)
    }


if __name__ == "__main__":
    activity = get_github_activity()
    print(f"\nGitHub Activity (last 7 days)")
    print(f"================================")
    print(f"Username:     {activity['username']}")
    print(f"Commits:      {activity['commits_this_week']}")
    print(f"PRs opened:   {activity['prs_opened']}")
    print(f"Active repos: {activity['repo_count']}")
    for repo in activity['repos_active']:
        print(f"  → {repo}")