import sqlite3
import os
from datetime import datetime
from datetime import datetime, timezone

DB_PATH = "devradar.db"

def init_db():
    """Create tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS github_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            captured_at TEXT,
            commits_this_week INTEGER,
            prs_opened INTEGER,
            repo_count INTEGER,
            repos_active TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leetcode_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            captured_at TEXT,
            total_solved INTEGER,
            easy_solved INTEGER,
            medium_solved INTEGER,
            hard_solved INTEGER,
            streak INTEGER,
            total_active_days INTEGER
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialized.")


def save_github_snapshot(data: dict):
    """Save a GitHub activity snapshot."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO github_snapshots 
        (captured_at, commits_this_week, prs_opened, repo_count, repos_active)
        VALUES (?, ?, ?, ?, ?)
    """, (
        datetime.now(timezone.utc).isoformat(),
        data.get("commits_this_week", 0),
        data.get("prs_opened", 0),
        data.get("repo_count", 0),
        ", ".join(data.get("repos_active", []))
    ))

    conn.commit()
    conn.close()
    print("GitHub snapshot saved.")


def save_leetcode_snapshot(data: dict):
    """Save a LeetCode stats snapshot."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO leetcode_snapshots
        (captured_at, total_solved, easy_solved, medium_solved, hard_solved, streak, total_active_days)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now(timezone.utc).isoformat(),
        data.get("total_solved", 0),
        data.get("easy_solved", 0),
        data.get("medium_solved", 0),
        data.get("hard_solved", 0),
        data.get("streak", 0),
        data.get("total_active_days", 0)
    ))

    conn.commit()
    conn.close()
    print("LeetCode snapshot saved.")


def get_github_history():
    """Get last 8 weeks of GitHub snapshots."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT captured_at, commits_this_week, prs_opened, repo_count
        FROM github_snapshots
        ORDER BY captured_at DESC
        LIMIT 8
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_leetcode_history():
    """Get last 8 weeks of LeetCode snapshots."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT captured_at, total_solved, easy_solved, medium_solved, hard_solved, streak
        FROM leetcode_snapshots
        ORDER BY captured_at DESC
        LIMIT 8
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    from github_fetcher import get_github_activity
    from leetcode_fetcher import get_leetcode_activity

    init_db()

    github_data = get_github_activity()
    save_github_snapshot(github_data)

    leetcode_data = get_leetcode_activity()
    save_leetcode_snapshot(leetcode_data)

    print("\nGitHub history:")
    for row in get_github_history():
        print(f"  {row[0][:10]} — {row[1]} commits, {row[2]} PRs, {row[3]} repos")

    print("\nLeetCode history:")
    for row in get_leetcode_history():
        print(f"  {row[0][:10]} — {row[1]} solved ({row[2]}E/{row[3]}M/{row[4]}H), streak: {row[5]}")