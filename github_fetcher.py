import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

load_dotenv()

def get_github_activity(username: str) -> dict:
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"}

    since = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")

    url = f"https://api.github.com/users/{username}/events"
    response = requests.get(url, headers=headers)

    if response.status_code == 404:
      return {"error": "user_not_found"}

    if response.status_code != 200:
      return {"error": "api_error", "commits_this_week": 0, "prs_opened": 0, "repos_active": [], "repo_count": 0, "username": username}
    events = response.json()

    commits = 0
    prs_opened = 0
    repos_active = set()

    for event in events:
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