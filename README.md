# DevRadar

Track your developer activity across GitHub and LeetCode in one place.

## Features
- GitHub activity tracking (commits, PRs, active repos)
- LeetCode stats (problems solved, streak, difficulty breakdown)
- Weekly snapshots stored in SQLite
- AI-generated weekly digest

## Setup
1. Clone the repo
2. Create a virtual environment and install dependencies
3. Add your API keys to a .env file
4. Run python database.py to capture your first snapshot

## Tech Stack
- Python, Flask
- GitHub API, LeetCode GraphQL API
- SQLite, Groq API
- APScheduler
" > README.md